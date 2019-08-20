import datetime
import json
import pytest
import re
import requests_mock
import tests.test_json
import dydx.util as utils
import dydx.constants as consts
from dydx.client import Client

PRIVATE_KEY_1 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PRIVATE_KEY_2 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'  # noqa: E501
ADDRESS_1 = '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1'
ADDRESS_2 = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
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
PAIRS = ['WETH-DAI', 'DAI-WETH']
LOCAL_NODE = 'http://0.0.0.0:8545'


class TestClient():

    # ------------ Constructor ------------

    def test_constructor_string_private_key(self):
        client = Client(PRIVATE_KEY_1)
        assert client.public_address == ADDRESS_1
        assert client.account_number == 0

    def test_constructor_bytes_private_key(self):
        client = Client(bytearray.fromhex(PRIVATE_KEY_1[2:]))
        assert client.public_address == ADDRESS_1
        assert client.account_number == 0

    def test_constructor_account_number(self):
        client = Client(PRIVATE_KEY_1, account_number=consts.MAX_SOLIDITY_UINT)
        assert client.account_number == consts.MAX_SOLIDITY_UINT
        assert str(consts.MAX_SOLIDITY_UINT) == '115792089237316195423570985008687907853269984665640564039457584007913129639935'  # noqa: E501

    def test_constructor_bad_private_key(self):
        with pytest.raises(TypeError):
            Client(1)

    def test_constructor_no_private_key(self):
        with pytest.raises(TypeError):
            Client()

    # -----------------------------------------------------------
    # Public API
    # -----------------------------------------------------------

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

    # ------------ get_my_balances ------------

    def test_get_my_balances_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_balances_json
            uri = 'https://api.dydx.exchange/v1/accounts/' \
                + client.public_address \
                + '?number=' + str(client.account_number)
            rm.get(uri, json=json_obj)
            result = client.get_my_balances()
            assert result == json_obj

    # ------------ get_balances ------------

    def test_get_balances_no_address_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_balances()
        assert 'required positional argument: \'address\'' in str(error.value)

    def test_get_balances_address_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_balances_json
            uri = 'https://api.dydx.exchange/v1/accounts/' + ADDRESS_2
            rm.get(uri, json=json_obj)
            result = client.get_balances(
                address=ADDRESS_2
            )
            assert result == json_obj

    def test_get_balances_address_and_number_success(self):
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

    # ------------ get_my_orders ------------

    def test_get_my_orders_no_pairs_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_my_orders()
        assert 'required positional argument: \'pairs\'' in str(error.value)

    def test_get_my_orders_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/dex/orders' \
                + '?makerAccountOwner=' + client.public_address \
                + '&makerAccountNumber=' + str(client.account_number) \
                + '&pairs=' + ','.join(PAIRS)
            rm.get(uri, json=json_obj)
            result = client.get_my_orders(
                pairs=PAIRS
            )
            assert result == json_obj

    def test_get_my_orders_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/dex/orders' \
                + '?makerAccountOwner=' + client.public_address \
                + '&makerAccountNumber=' + str(client.account_number) \
                + '&pairs=' + ','.join(PAIRS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_my_orders(
                pairs=PAIRS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_orders ------------

    def test_get_orders_no_pairs_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_orders()
        assert 'required positional argument: \'pairs\'' in str(error.value)

    def test_get_orders_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/dex/orders' \
                + '?pairs=' + ','.join(PAIRS)
            rm.get(uri, json=json_obj)
            result = client.get_orders(
                pairs=PAIRS
            )
            assert result == json_obj

    def test_get_orders_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/dex/orders' \
                + '?pairs=' + ','.join(PAIRS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_orders(
                pairs=PAIRS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_my_fills ------------

    def test_get_my_fills_no_pairs_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_my_fills()
        assert 'required positional argument: \'pairs\'' in str(error.value)

    def test_get_my_fills_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v1/dex/fills' \
                + '?makerAccountOwner=' + client.public_address \
                + '&makerAccountNumber=' + str(client.account_number) \
                + '&pairs=' + ','.join(PAIRS)
            rm.get(uri, json=json_obj)
            result = client.get_my_fills(
                pairs=PAIRS
            )
            assert result == json_obj

    def test_get_my_fills_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v1/dex/fills' \
                + '?makerAccountOwner=' + client.public_address \
                + '&makerAccountNumber=' + str(client.account_number) \
                + '&pairs=' + ','.join(PAIRS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_my_fills(
                pairs=PAIRS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_fills ------------

    def test_get_fills_no_pairs_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_fills()
        assert 'required positional argument: \'pairs\'' in str(error.value)

    def test_get_fills_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v1/dex/fills' \
                + '?pairs=' + ','.join(PAIRS)
            rm.get(uri, json=json_obj)
            result = client.get_fills(
                pairs=PAIRS
            )
            assert result == json_obj

    def test_get_fills_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v1/dex/fills' \
                + '?pairs=' + ','.join(PAIRS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_fills(
                pairs=PAIRS,
                limit=limit,
                startingBefore=startingBefore
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
            assert abs(
                int(body['order']['expiration']) -
                utils.epoch_in_four_weeks()) <= 10
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

    # ------------ cancel_order ------------

    def test_cancel_order_no_hash_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.cancel_order()
        assert 'required positional argument: \'hash\'' in str(error.value)

    def test_cancel_order_success(self):

        def additional_matcher(request):
            return 'Bearer ' + CANCEL_ORDER_SIGNATURE == \
                request.headers['Authorization']

        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_cancel_order_json
            rm.delete(
                'https://api.dydx.exchange/v1/dex/orders/' + ORDER_HASH,
                additional_matcher=additional_matcher,
                json=json_obj
            )
            result = client.cancel_order(
                hash=ORDER_HASH
            )
            assert result == json_obj

    # -----------------------------------------------------------
    # Ethereum Transactions
    # -----------------------------------------------------------

    def _validate_tx_hash(self, client, tx_hash):
        assert re.compile("^0x[a-f0-9]{64}").match(tx_hash)
        receipt = client.get_receipt(tx_hash)
        assert receipt['transactionHash'].hex() == tx_hash

    # ------------ set_allowance ------------

    def test_set_allowance_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.set_allowance(market=0)
        self._validate_tx_hash(client, tx_hash)

    def test_set_allowance_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.set_allowance(market=1)
        self._validate_tx_hash(client, tx_hash)

    def test_set_allowance_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.set_allowance(market=3)
        assert 'Invalid market number' in str(error.value)

    # ------------ enable_limit_orders ------------

    def test_enable_limit_orders_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.enable_limit_orders()
        self._validate_tx_hash(client, tx_hash)

    # ------------ deposit ------------

    def test_deposit_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.deposit(
            market=0,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_deposit_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.deposit(
            market=1,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_deposit_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.deposit(
                market=3,
                wei=1000
            )
        assert 'Invalid market number' in str(error.value)

    # ------------ withdraw ------------

    def test_withdraw_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.withdraw(
            market=0,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.withdraw(
            market=1,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.withdraw(
                market=3,
                wei=1000
            )
        assert 'Invalid market number' in str(error.value)

    # ------------ withdraw_to_zero ------------

    def test_withdraw_to_zero_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.withdraw_to_zero(market=0)
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_to_zero_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.withdraw_to_zero(market=1)
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_to_zero_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.withdraw_to_zero(market=3)
        assert 'Invalid market number' in str(error.value)
