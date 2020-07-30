import datetime
import json
import pytest
import requests_mock
import tests.test_json
import dydx.util as utils
import dydx.constants as consts
import dydx.perp_orders as perp_orders
import dydx.solo_orders as solo_orders
from decimal import Decimal
from dydx.client import Client

PRIVATE_KEY_1 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PRIVATE_KEY_2 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'  # noqa: E501
ADDRESS_1 = '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1'
ADDRESS_2 = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
ADDRESS_1_NO_PREFIX = ADDRESS_1[2:]

ORDER_HASH = '0x50538cce27ddd08a8a3732aaedb90b5ef55fd92a6819f5798edc043833776405'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0xe760368bbdb904809d2383606e27b9ab8ed57f47ce37dc67d4f87e59bb9102c46447f7ce20f1751cd7d670f2b7e4dec61da3288f242d3a003cc70b13a8560f7c1b01'  # noqa: E501

PERP_ORDER_HASH = '0x581a3e51afe0e0842ed4964a23d961cdf421999460860f1ab1a5a85d59bf9144'  # noqa: E501
CANCEL_PERP_ORDER_SIGNATURE = '0x12ac3ffc41c59b5bfcb9fe440db74a533eacefcb09a7a5c4f41735ed9e8d1b4f4368984ef254bbe1c672d0b89226d21126d58dcc38e83ae3a2fdf22e4d7f89021b01'  # noqa: E501

MARKETS = ['WETH-DAI']
STATUS = ['PENDING']
PERPETUAL_MARKETS = ['PBTC-USDC']
LOCAL_NODE = 'http://0.0.0.0:8545'


# ------------ Helper Functions ------------

def _create_solo_order_matcher(client, args):

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
        assert order['amount'] == str(args['amount'])
        assert order['limitPrice'] == str(args['limitPrice'])
        assert order['triggerPrice'] == '0'
        assert order['limitFee'] == '0.01'
        assert order['makerAccountOwner'] == \
            client.public_address
        assert order['makerAccountNumber'] == \
            str(client.account_number)
        assert abs(
            int(order['expiration']) -
            utils.epoch_in_four_weeks()) <= 10
        assert order['salt'].isnumeric()

        expected_signature = solo_orders.sign_order({
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


def _create_perp_order_matcher(client, args):

    def _additional_matcher(request):
        body = json.loads(request.body)
        assert not body['fillOrKill']
        assert not body['postOnly']
        assert 'cancelAmountOnRevert' not in body
        assert 'cancelId' not in body
        assert 'clientId' not in body
        assert body['market'] == args['market']

        order = body['order']
        assert order['isBuy'] is args['isBuy']
        assert order['isDecreaseOnly'] is False
        assert order['amount'] == str(args['amount'])
        assert order['limitPrice'] == str(args['limitPrice'])
        assert order['triggerPrice'] == '0'
        assert order['limitFee'] == '0.01'
        assert order['maker'] == client.public_address
        assert order['taker'] == consts.TAKER_ACCOUNT_OWNER
        assert abs(
            int(order['expiration']) -
            utils.epoch_in_four_weeks()) <= 10
        assert order['salt'].isnumeric()

        expected_signature = perp_orders.sign_order({
            'isBuy': order['isBuy'],
            'amount': int(order['amount']),
            'limitPrice': Decimal(order['limitPrice']),
            'triggerPrice': Decimal(order['triggerPrice']),
            'limitFee':  Decimal(order['limitFee']),
            'maker': order['maker'],
            'taker': order['taker'],
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
            rm.get('https://api.dydx.exchange/v2/markets', json=json_obj)
            result = client.get_pairs()
            assert result == json_obj

    def test_get_pairs_fail(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            rm.get('https://api.dydx.exchange/v2/markets', status_code=400)
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

    # ------------ get_my_perpetual_balances ------------

    def test_get_my_perpetual_balances_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_balances_json
            uri = 'https://api.dydx.exchange/v1/perpetual-accounts/' \
                + client.public_address
            rm.get(uri, json=json_obj)
            result = client.get_my_perpetual_balances()
            assert result == json_obj

    # ------------ get_perpetual_balances ------------

    def test_get_perpetual_balances_no_address_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.get_perpetual_balances()
        assert 'required positional argument: \'address\'' in str(error.value)

    def test_get_perpetual_balances_address_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_balances_json
            uri = 'https://api.dydx.exchange/v1/perpetual-accounts/' + \
                ADDRESS_2
            rm.get(uri, json=json_obj)
            result = client.get_perpetual_balances(address=ADDRESS_2)
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
                + '&status=' + ','.join(STATUS) \
                + '&limit=' + str(limit) \
                + '&startingBefore=' + startingBefore
            rm.get(uri, json=json_obj)
            result = client.get_my_orders(
                market=MARKETS,
                status=STATUS,
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

    # ------------ get_market / get_markets ------------

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

    # ------------ get_perpetual_market / get_perpetual_markets ------------

    def test_get_perpetual_market_success(self):
        client = Client(PRIVATE_KEY_1)
        market = 'PBTC-USDC'
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_market_json
            uri = 'https://api.dydx.exchange/v1/perpetual-markets/' + market
            rm.get(uri, json=json_obj)
            result = client.get_perpetual_market(
                market=market,
            )
            assert result == json_obj

    def test_get_perpetual_markets_success(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_get_markets_json
            uri = 'https://api.dydx.exchange/v1/perpetual-markets'
            rm.get(uri, json=json_obj)
            result = client.get_perpetual_markets()
            assert result == json_obj

    # ------------ place_order ------------

    def test_place_order_success_weth_dai(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_place_order_json
            rm.post(
                'https://api.dydx.exchange/v2/orders',
                additional_matcher=_create_solo_order_matcher(
                    client,
                    {
                        'baseMarket': '0',
                        'quoteMarket': '3',
                        'isBuy': True,
                        'limitPrice': '250.01',
                        'amount': '10000',
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

    def test_place_order_success_dai_usdc(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_place_order_json
            rm.post(
                'https://api.dydx.exchange/v2/orders',
                additional_matcher=_create_solo_order_matcher(
                    client,
                    {
                        'baseMarket': '0',
                        'quoteMarket': '2',
                        'isBuy': False,
                        'limitPrice': '0.00000000025001',
                        'amount': '10000',
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

    def test_place_order_success_pbtc_usdc(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_place_order_json
            rm.post(
                'https://api.dydx.exchange/v2/orders',
                additional_matcher=_create_perp_order_matcher(
                    client,
                    {
                        'market': 'PBTC-USDC',
                        'isBuy': False,
                        'limitPrice': '0.00000000025001',
                        'amount': '100000000',
                    },
                ),
                json=json_obj
            )
            result = client.place_order(
                market='PBTC-USDC',
                side='SELL',
                amount=100000000,
                price=Decimal('0.00000000025001')
            )
            assert result == json_obj

    # ------------ cancel_order / cancel_perpetual_order ------------

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

    def test_cancel_perpetual_order_no_hash_error(self):
        client = Client(PRIVATE_KEY_1)
        with pytest.raises(TypeError) as error:
            client.cancel_perpetual_order()
        assert 'required positional argument: \'hash\'' in str(error.value)

    def test_cancel_perpetual_order_success(self):

        def additional_matcher(request):
            return 'Bearer ' + CANCEL_PERP_ORDER_SIGNATURE == \
                request.headers['Authorization']

        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = tests.test_json.mock_cancel_order_json
            rm.delete(
                'https://api.dydx.exchange/v2/orders/' + PERP_ORDER_HASH,
                additional_matcher=additional_matcher,
                json=json_obj
            )
            result = client.cancel_perpetual_order(
                hash=PERP_ORDER_HASH
            )
            assert result == json_obj

    # ------------ get_funding_rates ------------

    def test_get_funding_rates_no_params(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_funding_rates response'}
            uri = 'https://api.dydx.exchange/v1/funding-rates'
            rm.get(uri, json=json_obj)
            result = client.get_funding_rates()
            assert result == json_obj

    def test_get_funding_rates_with_markets(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_funding_rates response'}
            uri = 'https://api.dydx.exchange/v1/funding-rates' \
                + '?markets=' + ','.join(PERPETUAL_MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_funding_rates(
                markets=PERPETUAL_MARKETS,
            )
            assert result == json_obj

    # ------------ get_historical_funding_rates ------------

    def test_get_historical_funding_rates_no_params(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_historical_funding response'}
            uri = 'https://api.dydx.exchange/v1/historical-funding-rates'
            rm.get(uri, json=json_obj)
            result = client.get_historical_funding_rates()
            assert result == json_obj

    def test_get_historical_funding_rates_with_markets(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_historical_funding response'}
            uri = 'https://api.dydx.exchange/v1/historical-funding-rates' \
                + '?markets=' + ','.join(PERPETUAL_MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_historical_funding_rates(
                markets=PERPETUAL_MARKETS,
            )
            assert result == json_obj

    def test_get_historical_funding_rates_with_limit_and_starting_before(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_historical_funding response'}
            limit = 50
            startingBefore = '2020-04-10T22:00:00.000Z'
            uri = 'https://api.dydx.exchange/v1/historical-funding-rates' \
                + '?limit=' + str(limit) \
                + '&startingBefore=' + str(startingBefore)
            rm.get(uri, json=json_obj)
            result = client.get_historical_funding_rates(
                limit=limit,
                startingBefore=startingBefore,
            )
            assert result == json_obj

    # ------------ get_funding_index_price ------------

    def test_get_funding_index_price_no_params(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_funding_index response'}
            uri = 'https://api.dydx.exchange/v1/index-price'
            rm.get(uri, json=json_obj)
            result = client.get_funding_index_price()
            assert result == json_obj

    def test_get_funding_index_price_with_markets(self):
        client = Client(PRIVATE_KEY_1)
        with requests_mock.mock() as rm:
            json_obj = {'key': 'mock get_funding_index response'}
            uri = 'https://api.dydx.exchange/v1/index-price' \
                + '?markets=' + ','.join(PERPETUAL_MARKETS)
            rm.get(uri, json=json_obj)
            result = client.get_funding_index_price(
                markets=PERPETUAL_MARKETS,
            )
            assert result == json_obj
