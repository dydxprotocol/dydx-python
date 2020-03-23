import datetime
import json
import pytest
import requests_mock
import tests.test_json
import dydx.util as utils
import dydx.constants as consts
from decimal import Decimal
from dydx.client import Client

PRIVATE_KEY_1 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PRIVATE_KEY_2 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'  # noqa: E501
ADDRESS_1 = '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1'
ADDRESS_2 = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
ADDRESS_1_NO_PREFIX = ADDRESS_1[2:]
ADDRESS_2_NO_PREFIX = ADDRESS_2[2:]
ORDER = {
    'isBuy': True,
    'baseMarket': 0,
    'quoteMarket': 3,
    'amount': 10000,
    'limitPrice': Decimal('250.01'),
    'triggerPrice': Decimal(0),
    'limitFee':  Decimal('0.0050'),
    'makerAccountOwner': ADDRESS_1,
    'makerAccountNumber': 111,
    'expiration': 1234,
    'salt': 0,
}
ORDER_HASH = '0x50538cce27ddd08a8a3732aaedb90b5ef55fd92a6819f5798edc043833776405'  # noqa: E501
CANCEL_ORDER_HASH = '0xca25945c7cbc05dda130cff8f92acd555c464e22239e0864637aeec402e556c5'  # noqa: E501
ORDER_SIGNATURE = '0x229e6e1926aadea40b933dd6b12c9f4daac3267df5ca31041c72a9f6f2a057fe6257a664cca749be666f4452b1aa3587f5bc844c6b4fe7c835da8a4cabf9fa461b01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0xe760368bbdb904809d2383606e27b9ab8ed57f47ce37dc67d4f87e59bb9102c46447f7ce20f1751cd7d670f2b7e4dec61da3288f242d3a003cc70b13a8560f7c1b01'  # noqa: E501
MARKETS = ['WETH-DAI', 'DAI-WETH']
LOCAL_NODE = 'http://0.0.0.0:8545'


# ------------ Helper Functions ------------

def _create_additional_matcher(client, args):

    def _additional_matcher(request):
        body = json.loads(request.body)
        assert not body['fillOrKill']
        assert not body['postOnly']
        assert 'cancelAmountOnRevert' not in body
        assert 'cancelId' not in body
        assert 'clientId' not in body

        order = body['order']
        assert order['isBuy'] is args['isBuy']
        assert order['isDecreaseOnly'] is False
        assert order['baseMarket'] == str(args['baseMarket'])
        assert order['quoteMarket'] == str(args['quoteMarket'])
        assert order['amount'] == '10000'
        assert order['limitPrice'] == str(args['limitPrice'])
        assert order['triggerPrice'] == '0'
        assert order['limitFee'] == '0.005'
        assert order['makerAccountOwner'] == \
            client.public_address
        assert order['makerAccountNumber'] == \
            str(client.account_number)
        assert abs(
            int(order['expiration']) -
            utils.epoch_in_four_weeks()) <= 10
        assert order['salt'].isnumeric()

        expected_signature = utils.sign_order({
            'isBuy': order['isBuy'],
            'baseMarket': int(order['baseMarket']),
            'quoteMarket': int(order['quoteMarket']),
            'amount': int(order['amount']),
            'limitPrice': Decimal(order['limitPrice']),
            'triggerPrice': Decimal(order['triggerPrice']),
            'limitFee':  Decimal(order['limitFee']),
            'makerAccountOwner': order['makerAccountOwner'],
            'makerAccountNumber': int(order['makerAccountNumber']),
            'expiration': int(order['expiration']),
            'salt': int(order['salt'])
        }, client.private_key)
        assert body['order']['typedSignature'] == expected_signature
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

    # ------------ get_market ------------

    def test_get_market_success(self):
        client = Client(PRIVATE_KEY_1)
        market = MARKETS[0]
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_market_json
            uri = 'https://api.dydx.exchange/v2/markets/' + market
            rm.get(uri, json=json_obj)
            result = client.get_market(
                market=market,
            )
            assert result == json_obj

    def test_get_markets_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_markets_json
            uri = 'https://api.dydx.exchange/v2/markets'
            rm.get(uri, json=json_obj)
            result = client.get_markets()
            assert result == json_obj

    # ------------ place_order ------------

    def test_place_order_success_wethdai(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_place_order_json
            rm.post(
                'https://api.dydx.exchange/v2/orders',
                additional_matcher=_create_additional_matcher(
                    client,
                    {
                        'baseMarket': '0',
                        'quoteMarket': '3',
                        'isBuy': True,
                        'limitPrice': '250.01',
                    },
                ),
                json=json_obj
            )
            result = client.place_order(
                market='WETH-DAI',
                side='BUY',
                amount=10000,
                price=Decimal('250.01')
            )
            assert result == json_obj

    def test_place_order_success_daiusdc(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_place_order_json
            rm.post(
                'https://api.dydx.exchange/v2/orders',
                additional_matcher=_create_additional_matcher(
                    client,
                    {
                        'baseMarket': '0',
                        'quoteMarket': '2',
                        'isBuy': False,
                        'limitPrice': '0.00000000025001',
                    },
                ),
                json=json_obj
            )
            result = client.place_order(
                market='WETH-USDC',
                side='SELL',
                amount=10000,
                price=Decimal('0.00000000025001')
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
                'https://api.dydx.exchange/v2/orders/' + ORDER_HASH,
                additional_matcher=additional_matcher,
                json=json_obj
            )
            result = client.cancel_order(
                hash=ORDER_HASH
            )
            assert result == json_obj
