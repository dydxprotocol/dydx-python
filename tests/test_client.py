import json
import pytest
import requests_mock
import tests.test_json
import dydx.util as utils
from dydx.client import Client

PRIVATE_KEY_1 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PRIVATE_KEY_2 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'  # noqa: E501
ADDRESS_1 = '0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1'
ADDRESS_2 = '0xffcf8fdee72ac11b5c542428b35eef5769c409f0'
ADDRESS_1_NO_PREFIX = ADDRESS_1[2:]
ADDRESS_2_NO_PREFIX = ADDRESS_2[2:]
ORDER = {
    'maker_market': 0,
    'taker_market': 1,
    'maker_amount': 100,
    'taker_amount': 200,
    'maker_account_owner': ADDRESS_1,
    'maker_account_number': 111,
    'taker_account_owner': ADDRESS_2,
    'taker_account_number': 222,
    'expiration': 1234,
    'salt': 4321
}
ORDER_HASH = '0x998ec84efeb9d5b2e20820722d90a9430ec7085ad45bbd7b2cd6b312abe294c5'  # noqa: E501
CANCEL_ORDER_HASH = '0x54da43ec40e5ae61b2dac3d9068cd56d257459bc105ad0317857b7b4f66e101c'  # noqa: E501
ORDER_SIGNATURE = '0x342f7533477aff89c3d25facdecb3875a68ccb5271a79dca64d19c822a6a8d560dba1ce392a50d7cd0d76ee45cfd8e6627764b012970bf43f6f8fd61677cf2ba1c01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0xe1381f81b47132cc23809ddff717b40d52f3a4c7cbb49f85aadf2f893c6f433c05d5cc4143694630ac504429b1c325251dec3dde9fec6c02f95246663c0f4b7f1c01'  # noqa: E501


class TestClient():

    # ------------ Constructor ------------

    def test_constructor_string_private_key(self):
        client = Client(PRIVATE_KEY_1)
        assert(client.public_address == ADDRESS_1)
        assert(client.account_number == 0)

    def test_constructor_bytes_private_key(self):
        client = Client(bytearray.fromhex(PRIVATE_KEY_1[2:]))
        assert(client.public_address == ADDRESS_1)
        assert(client.account_number == 0)

    def test_constructor_public_address(self):
        client = Client(PRIVATE_KEY_1, public_address=ADDRESS_1)
        assert(client.public_address == ADDRESS_1)
        assert(client.account_number == 0)

    def test_constructor_account_number(self):
        client = Client(PRIVATE_KEY_1, account_number=1)
        assert(client.account_number == 1)

    def test_constructor_bad_private_key(self):
        with pytest.raises(TypeError):
            Client(1)

    def test_constructor_no_private_key(self):
        with pytest.raises(TypeError):
            Client()

    def test_constructor_bad_public_address(self):
        with pytest.raises(ValueError) as error:
            Client(PRIVATE_KEY_1, public_address=ADDRESS_2)
        assert 'private_key/public_address mismatch' in str(error.value)

    # ------------ get_pairs ------------

    def test_get_pairs_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_pairs_json
            rm.get('https://api.dydx.exchange/v1/dex/pairs', json=json_obj)
            result = client.get_pairs()
            assert result == json_obj

    def test_get_pairs_fail(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            rm.get('https://api.dydx.exchange/v1/dex/pairs', status_code=400)
            with pytest.raises(Exception) as error:
                client.get_pairs()
            assert '400' in str(error.value)

    # ------------ get_balances ------------

    def test_get_balances_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_balances_json
            uri = 'https://api.dydx.exchange/v1/accounts/' \
                + client.public_address \
                + '?number=' + str(client.account_number)
            rm.get(uri, json=json_obj)
            result = client.get_balances()
            assert result == json_obj

    def test_get_balances_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_balances_json
            uri = 'https://api.dydx.exchange/v1/accounts/' \
                + ADDRESS_2 \
                + '?number=' + str(1234)
            rm.get(uri, json=json_obj)
            result = client.get_balances(
                address=ADDRESS_2,
                number=1234
            )
            assert result == json_obj

    # ------------ get_orders ------------

    def test_get_orders_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/dex/orders' \
                + '?makerAccountOwner=' + client.public_address
            rm.get(uri, json=json_obj)
            result = client.get_orders()
            assert result == json_obj

    def test_get_orders_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/dex/orders' \
                + '?makerAccountOwner=' + ADDRESS_2
            rm.get(uri, json=json_obj)
            result = client.get_orders(
                makerAccountOwner=ADDRESS_2
            )
            assert result == json_obj

    # ------------ get_fills ------------

    def test_get_fills_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v1/dex/fills' \
                + '?makerAccountOwner=' + client.public_address
            rm.get(uri, json=json_obj)
            result = client.get_fills()
            assert result == json_obj

    def test_get_fills_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v1/dex/fills' \
                + '?makerAccountOwner=' + ADDRESS_2
            rm.get(uri, json=json_obj)
            result = client.get_fills(
                makerAccountOwner=ADDRESS_2
            )
            assert result == json_obj

    # ------------ create_order ------------

    def test_create_order_success(self):

        def additional_matcher(request):
            body = json.loads(request.body)
            assert body['fillOrKill'] is False
            assert body['order']['takerMarket'] == '0'
            assert body['order']['makerMarket'] == '1'
            assert body['order']['takerAmount'] == '1000'
            assert body['order']['makerAmount'] == '2000'
            assert body['order']['makerAccountOwner'] == \
                client.public_address
            assert body['order']['makerAccountNumber'] == \
                str(client.account_number)
            assert body['order']['takerAccountOwner'] == \
                client.TAKER_ACCOUNT_OWNER
            assert body['order']['takerAccountNumber'] == \
                str(client.TAKER_ACCOUNT_NUMBER)
            assert body['order']['expiration'] == '0'
            assert body['order']['salt'].isnumeric()
            sent_order = body['order']
            expected_signature = utils.sign_order({
                'makerMarket': int(sent_order['makerMarket']),
                'takerMarket': int(sent_order['takerMarket']),
                'makerAmount': int(sent_order['makerAmount']),
                'takerAmount': int(sent_order['takerAmount']),
                'makerAccountOwner': sent_order['makerAccountOwner'],
                'makerAccountNumber': int(sent_order['makerAccountNumber']),
                'takerAccountOwner': sent_order['takerAccountOwner'],
                'takerAccountNumber': int(sent_order['takerAccountNumber']),
                'expiration': int(sent_order['expiration']),
                'salt': int(sent_order['salt']),
            }, client.private_key)
            assert body['order']['typedSignature'] == expected_signature
            return True

        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_create_order_json
            rm.post(
                'https://api.dydx.exchange/v1/dex/orders',
                additional_matcher=additional_matcher,
                json=json_obj
            )
            result = client.create_order(
                makerMarket=1,
                takerMarket=0,
                makerAmount=2000,
                takerAmount=1000
            )
            assert result == json_obj

    # ------------ delete_order ------------

    def test_delete_order_success(self):

        def additional_matcher(request):
            return 'Bearer ' + CANCEL_ORDER_SIGNATURE == \
                request.headers['Authorization']

        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_delete_order_json
            rm.delete(
                'https://api.dydx.exchange/v1/dex/orders/' + ORDER_HASH,
                additional_matcher=additional_matcher,
                json=json_obj
            )
            result = client.delete_order(
                hash=ORDER_HASH
            )
            assert result == json_obj
