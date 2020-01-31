import datetime
import json
import pytest
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
ORDER_HASH = '0x444df3e619ce1865bb0138e89b3e92c29b1e57a6b35c4708822923bc60985c3d'  # noqa: E501
CANCEL_ORDER_HASH = '0x45170c4ba6a19e3c9e25a4f3b3d65b9f2d988ad80f7a270528c03a7c484e1774'  # noqa: E501
ORDER_SIGNATURE = '0x94c3e787666fa8d2611ce4543ced732e0f4591958d8a12feded84746bcde457f1dab3fc66cafc5eda9c6e755f0f82f4049353cad165a5187d4ec66d365c9c2991b01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0x3d29b75f6aad6db4cc02259bcaa98f465a164392b1c4743d7d0f53b73f64f29f00b495dc132b9a63b4aa613c15909878be1274b575549a959d9586eb7b5e520a1b01'  # noqa: E501
PAIRS = ['WETH-DAI', 'DAI-WETH']
MARKETS = ['WETH-DAI']
LOCAL_NODE = 'http://0.0.0.0:8545'


# ------------ Helper Functions ------------

def _create_additional_matcher(client, cancelId=None):

    def _additional_matcher(request):
        body = json.loads(request.body)
        assert not body['fillOrKill']
        assert not body['postOnly']
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
        if cancelId:
            assert body['cancelId'] == cancelId
        return True

    return _additional_matcher


# ------------ Tests ------------

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
        assert 'required positional argument: \'market\'' in str(error.value)

    def test_get_orders_no_market_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v2/orders' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number)
            rm.get(uri, json=json_obj)
            result = client.get_orders(
                accountOwner=client.public_address,
                accountNumber=client.account_number,
            )
            assert result == json_obj

    def test_get_my_orders_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v2/orders' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number) \
                + '&market=' + ','.join(MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_my_orders(
                market=MARKETS,
            )
            assert result == json_obj

    def test_get_my_orders_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v2/orders' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number) \
                + '&market=' + ','.join(MARKETS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_my_orders(
                market=MARKETS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_orders ------------

    def test_get_orders_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v2/orders' \
                + '?market=' + ','.join(MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_orders(
                market=MARKETS,
            )
            assert result == json_obj

    def test_get_orders_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v2/orders' \
                + '?market=' + ','.join(MARKETS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_orders(
                market=MARKETS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_order ---------------

    def test_get_order_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_order_json
            uri = 'https://api.dydx.exchange/v2/orders/' \
                + ORDER_HASH
            rm.get(uri, json=json_obj)
            result = client.get_order(
                ORDER_HASH
            )
            assert result == json_obj

    # ------------ get_my_fills ------------

    def test_get_my_fills_no_pairs_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_my_fills()
        assert 'required positional argument: \'market\'' in str(error.value)

    def test_get_my_fills_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v2/fills' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number) \
                + '&market=' + ','.join(MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_my_fills(
                market=MARKETS
            )
            assert result == json_obj

    def test_get_my_fills_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v2/fills' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number) \
                + '&market=' + ','.join(MARKETS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_my_fills(
                market=MARKETS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_fills ------------

    def test_get_fills_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v2/fills' \
                + '?market=' + ','.join(MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_fills(
                market=MARKETS,
            )
            assert result == json_obj

    def test_get_fills_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_fills_json
            uri = 'https://api.dydx.exchange/v2/fills' \
                + '?market=' + ','.join(MARKETS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_fills(
                market=MARKETS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_my_trades ------------

    def test_get_my_trades_no_pairs_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_my_trades()
        assert 'required positional argument: \'market\'' in str(error.value)

    def test_get_my_trades_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_trades_json
            uri = 'https://api.dydx.exchange/v2/trades' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number) \
                + '&market=' + ','.join(MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_my_trades(
                market=MARKETS,
            )
            assert result == json_obj

    def test_get_my_trades_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 99
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_trades_json
            uri = 'https://api.dydx.exchange/v2/trades' \
                + '?accountOwner=' + client.public_address \
                + '&accountNumber=' + str(client.account_number) \
                + '&market=' + ','.join(MARKETS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_my_trades(
                market=MARKETS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_trades ------------

    def test_get_trades_default_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_trades_json
            uri = 'https://api.dydx.exchange/v2/trades' \
                + '?market=' + ','.join(MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_trades(
                market=MARKETS,
            )
            assert result == json_obj

    def test_get_trades_specified_success(self):
        client = Client(PRIVATE_KEY_1)
        limit = 1234
        startingBefore = datetime.datetime.utcnow().isoformat()
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_trades_json
            uri = 'https://api.dydx.exchange/v2/trades' \
                + '?market=' + ','.join(MARKETS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_trades(
                market=MARKETS,
                limit=limit,
                startingBefore=startingBefore
            )
            assert result == json_obj

    # ------------ get_orderbook ------------

    def test_get_orderbook_success(self):
        client = Client(PRIVATE_KEY_1)
        market = MARKETS[0]
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_orders_json
            uri = 'https://api.dydx.exchange/v1/orderbook/' + market
            rm.get(uri, json=json_obj)
            result = client.get_orderbook(
                market=market,
            )
            assert result == json_obj

    # ------------ create_order ------------

    def test_create_order_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_create_order_json
            rm.post(
                'https://api.dydx.exchange/v1/dex/orders',
                additional_matcher=_create_additional_matcher(client),
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

    # ------------ replace_order ------------

    def test_replace_order_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_create_order_json
            rm.post(
                'https://api.dydx.exchange/v1/dex/orders/replace',
                additional_matcher=_create_additional_matcher(
                    client,
                    cancelId=ORDER_HASH
                ),
                json=json_obj
            )
            result = client.replace_order(
                makerMarket=1,
                takerMarket=0,
                makerAmount=2000,
                takerAmount=1000,
                cancelId=ORDER_HASH
            )
            assert result == json_obj
