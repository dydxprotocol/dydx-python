import json
import random
import requests
import dydx.util as utils
import dydx.constants as consts
import dydx.solo_orders as solo_orders
import dydx.perp_orders as perp_orders
from decimal import Decimal
from dydx.eth import Eth
from .exceptions import DydxAPIError


class Client(object):
    BASE_API_URI = 'https://api.dydx.exchange'

    def __init__(
        self,
        private_key,
        account_number=0,
        node=None
    ):
        self.private_key = utils.normalize_private_key(private_key)
        self.account_number = account_number
        self.public_address = utils.private_key_to_address(self.private_key)
        self.session = self._init_session()
        self.eth = Eth(
            node=node,
            private_key=self.private_key,
            public_address=self.public_address,
            account_number=self.account_number
        )

    # -----------------------------------------------------------
    # Helper Methods
    # -----------------------------------------------------------

    def _init_session(self):
        session = requests.session()
        session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'dydx/python'
        })
        return session

    def _request(self, method, uri, **kwargs):
        complete_uri = self.BASE_API_URI + uri
        response = getattr(self.session, method)(complete_uri, **kwargs)
        if not str(response.status_code).startswith('2'):
            raise DydxAPIError(response)
        return response.json()

    def _get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request('put', *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request('delete', *args, **kwargs)

    def _make_solo_order(
        self,
        market,
        side,
        amount,
        price,
        expiration=None,
        limitFee=None,
        postOnly=False,
    ):
        '''
        Make an order object

        :param market: required
        :type market: str in list
            ["WETH-DAI", "WETH-USDC", "DAI-USDC"]

        :param side: required
        :type side: str in list ["BUY", "SELL"]

        :param amount: required
        :type amount: number

        :param price: required
        :type price: Decimal

        :param expiration: optional, defaults to 28 days from now
        :type expiration: number

        :param limitFee: optional, overrides the default limitFee
        :type limitFee: number

        :param postOnly: optional, defaults to False
        :type postOnly: bool

        :returns: Order

        :raises: DydxAPIError
        '''

        baseMarket, quoteMarket = utils.pair_to_base_quote_markets(market)
        isBuy = utils.get_is_buy(side)
        if limitFee is None:
            limitFee = utils.get_limit_fee(baseMarket, amount)

        order = {
            'salt': random.randint(0, 2**256),
            'isBuy': isBuy,
            'baseMarket': baseMarket,
            'quoteMarket': quoteMarket,
            'amount': int(float(amount)),
            'limitPrice': price,
            'triggerPrice': Decimal(0),
            'limitFee': limitFee,
            'makerAccountOwner': self.public_address,
            'makerAccountNumber': self.account_number,
            'expiration': expiration or utils.epoch_in_four_weeks(),
        }
        order['typedSignature'] = \
            solo_orders.sign_order(order, self.private_key)
        return order

    def _make_perp_order(
        self,
        market,
        side,
        amount,
        price,
        expiration=None,
        limitFee=None,
        postOnly=False,
    ):
        '''
        Make an order object

        :param market: required
        :type market: str in list
            ["PBTC-USDC"]

        :param side: required
        :type side: str in list ["BUY", "SELL"]

        :param amount: required
        :type amount: number

        :param price: required
        :type price: Decimal

        :param expiration: optional, defaults to 28 days from now
        :type expiration: number

        :param limitFee: optional, overrides the default limitFee
        :type limitFee: number

        :param postOnly: optional, defaults to False
        :type postOnly: bool

        :returns: Order

        :raises: DydxAPIError
        '''

        baseMarket, _ = utils.pair_to_base_quote_markets(market)
        isBuy = utils.get_is_buy(side)
        if limitFee is None:
            limitFee = utils.get_limit_fee(baseMarket, amount)

        order = {
            'salt': random.randint(0, 2**256),
            'isBuy': isBuy,
            'amount': int(float(amount)),
            'limitPrice': price,
            'triggerPrice': Decimal(0),
            'limitFee': limitFee,
            'maker': self.public_address,
            'taker': consts.TAKER_ACCOUNT_OWNER,
            'expiration': expiration or utils.epoch_in_four_weeks(),
        }
        order['typedSignature'] = \
            perp_orders.sign_order(order, self.private_key)
        return order

    # -----------------------------------------------------------
    # Public API
    # -----------------------------------------------------------

    def get_pairs(
        self
    ):
        '''
        Return all tradable pairs

        :returns: list of trading pairs

        :raises: DydxAPIError
        '''
        return self._get('/v2/markets')

    def get_my_balances(
        self
    ):
        '''
        Return balances for the loaded account

        :returns: list of balances

        :raises: DydxAPIError
        '''
        return self.get_balances(
            address=self.public_address,
            number=self.account_number
        )

    def get_balances(
        self,
        address,
        number=0
    ):
        '''
        Return balances for an address and account number

        :param address: required
        :type address: str (address)

        :param number: optional, defaults to 0
        :type number: number

        :returns: list of balances

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
            'number': number
        })
        return self._get('/v1/accounts/' + address + params)

    def get_my_perpetual_balances(
        self
    ):
        '''
        Return perpetual balances for the loaded account

        :returns: list of balances

        :raises: DydxAPIError
        '''
        return self.get_perpetual_balances(address=self.public_address)

    def get_perpetual_balances(
        self,
        address
    ):
        '''
        Return perpetual balances for an address

        :param address: required
        :type address: str (address)

        :returns: list of balances

        :raises: DydxAPIError
        '''
        return self._get('/v1/perpetual-accounts/' + address)

    def get_my_orders(
        self,
        market,
        limit=None,
        startingBefore=None,
        status=None
    ):
        '''
        Return open orders for the loaded account

        :param market: optional
        :type market: str[] of valid markets
            ["WETH-DAI", "DAI-USDC", "WETH-USDC", "PBTC-USDC"]

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :param status: optional
        :type status: str[] of valid statuses
            ["PENDING",
             "OPEN",
             "FILLED",
             "PARTIALLY_FILLED",
             "CANCELED",
             "UNTRIGGERED"]

        :returns: list of existing orders

        :raises: DydxAPIError
        '''
        return self.get_orders(
            market=market,
            status=status,
            accountOwner=self.public_address,
            accountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_orders(
        self,
        market=None,
        side=None,
        status=None,
        orderType=None,
        accountOwner=None,
        accountNumber=None,
        limit=None,
        startingBefore=None,
    ):
        '''
        Returns all open orders

        :param market: optional
        :type market: str[] of valid markets
            ["WETH-DAI", "DAI-USDC", "WETH-USDC", "PBTC-USDC"]

        :param side: optional
        :type side: str in list ["BUY", "SELL"]

        :param status: optional
        :type status: str[] of valid statuses
            ["PENDING",
             "OPEN",
             "FILLED",
             "PARTIALLY_FILLED",
             "CANCELED",
             "UNTRIGGERED"]

        :param orderType: optional
        :type orderType: str[] of valid order types
          ["LIMIT", "ISOLATED_MARKET", "STOP_LIMIT"]

        :param accountOwner: optional
        :type accountOwner: str (address)

        :param accountNumber: optional
        :type accountNumber: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :returns: list of existing orders

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
            'market': None if market is None else ','.join(market),
            'side': side,
            'status': None if status is None else ','.join(status),
            'orderType': None if orderType is None else ','.join(orderType),
            'accountOwner': accountOwner,
            'accountNumber': accountNumber,
            'limit': limit,
            'startingBefore': startingBefore
        })
        return self._get('/v2/orders' + params)

    def get_order(
        self,
        orderId,
    ):
        '''
        Return an order by id

        :param orderId: required
        :type id: str

        :returns: existing order

        :raises: DydxAPIError
        '''
        return self._get('/v2/orders/'+orderId)

    def get_my_fills(
        self,
        market,
        limit=None,
        startingBefore=None
    ):
        '''
        Return historical fills for the loaded account

        :param market: optional
        :type market: str[] of valid markets
            ["WETH-DAI", "DAI-USDC", "WETH-USDC", "PBTC-USDC"]

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :returns: list of processed fills

        :raises: DydxAPIError
        '''
        return self.get_fills(
            market=market,
            accountOwner=self.public_address,
            accountNumber=self.account_number,
            transactionHash=None,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_fills(
        self,
        market=None,
        side=None,
        accountOwner=None,
        accountNumber=None,
        transactionHash=None,
        limit=None,
        startingBefore=None,
    ):
        '''
        Returns all historical fills

        :param market: optional
        :type market: str[] of valid markets
            ["WETH-DAI", "DAI-USDC", "WETH-USDC", "PBTC-USDC"]

        :param side: optional
        :type side: str in list ["BUY", "SELL"]

        :param accountOwner: optional
        :type accountOwner: str (address)

        :param accountNumber: optional
        :type accountNumber: number

        :param transactionHash: optional
        :type transactionHash: str (hash)

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :returns: list of existing fills

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
            'market': None if market is None else ','.join(market),
            'side': side,
            'accountOwner': accountOwner,
            'accountNumber': accountNumber,
            'transactionHash': transactionHash,
            'limit': limit,
            'startingBefore': startingBefore
        })
        return self._get('/v2/fills' + params)

    def get_trades(
        self,
        market=None,
        side=None,
        accountOwner=None,
        accountNumber=None,
        transactionHash=None,
        limit=None,
        startingBefore=None,
    ):
        '''
        Returns all historical trades

        :param market: optional
        :type market: str[] of valid markets
            ["WETH-DAI", "DAI-USDC", "WETH-USDC", "PBTC-USDC"]

        :param side: optional
        :type side: str in list ["BUY", "SELL"]

        :param accountOwner: optional
        :type accountOwner: str (address)

        :param accountNumber: optional
        :type accountNumber: number

        :param transactionHash: optional
        :type transactionHash: str (hash)

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :returns: list of existing trades

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
            'market': None if market is None else ','.join(market),
            'side': side,
            'accountOwner': accountOwner,
            'accountNumber': accountNumber,
            'transactionHash': transactionHash,
            'limit': limit,
            'startingBefore': startingBefore,
        })
        return self._get('/v2/trades' + params)

    def get_my_trades(
        self,
        market,
        limit=None,
        startingBefore=None
    ):
        '''
        Return historical trades for the loaded account

        :param market: required
        :type market: list of str

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :returns: list of processed trades

        :raises: DydxAPIError
        '''
        return self.get_trades(
            market=market,
            accountOwner=self.public_address,
            accountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def place_order(
        self,
        market,
        side,
        amount,
        price,
        expiration=None,
        limitFee=None,
        fillOrKill=False,
        postOnly=False,
        clientId=None,
        cancelAmountOnRevert=None,
        cancelId=None,
    ):
        '''
        Create an order

        :param market: required
        :type market: str in list
            ["WETH-DAI", "WETH-USDC", "DAI-USDC", "PBTC-USDC"]

        :param side: required
        :type side: str in list ["BUY", "SELL"]

        :param amount: required
        :type amount: number

        :param price: required
        :type price: Decimal

        :param expiration: optional, defaults to 28 days from now
        :type expiration: number

        :param limitFee: optional, defaults to None
        :type limitFee: Decimal

        :param fillOrKill: optional, defaults to False
        :type fillOrKill: bool

        :param postOnly: optional, defaults to False
        :type postOnly: bool

        :param clientId: optional, defaults to None
        :type clientId: str

        :param cancelAmountOnRevert: optional, defaults to None
        :type cancelAmountOnRevert: bool

        :param cancelId: optional, defaults to None
        :type cancelId: str

        :returns: Order

        :raises: DydxAPIError
        '''

        if market == consts.PAIR_PBTC_USDC:

            order = self._make_perp_order(
                market,
                side,
                amount,
                price,
                expiration,
                limitFee,
                postOnly,
            )

            market_api_request = market

            order_api_request = {
                'isBuy': order['isBuy'],
                'isDecreaseOnly': False,
                'amount': str(order['amount']),
                'limitPrice': utils.decimalToStr(order['limitPrice']),
                'triggerPrice': utils.decimalToStr(order['triggerPrice']),
                'limitFee': utils.decimalToStr(order['limitFee']),
                'maker': order['maker'],
                'taker': order['taker'],
                'expiration': str(order['expiration']),
                'salt': str(order['salt']),
                'typedSignature': order['typedSignature'],
            }

        else:

            order = self._make_solo_order(
                market,
                side,
                amount,
                price,
                expiration,
                limitFee,
                postOnly,
            )

            market_api_request = None

            order_api_request = {
                'isBuy': order['isBuy'],
                'isDecreaseOnly': False,
                'baseMarket': str(order['baseMarket']),
                'quoteMarket': str(order['quoteMarket']),
                'amount': str(order['amount']),
                'limitPrice': utils.decimalToStr(order['limitPrice']),
                'triggerPrice': utils.decimalToStr(order['triggerPrice']),
                'limitFee': utils.decimalToStr(order['limitFee']),
                'makerAccountOwner': order['makerAccountOwner'],
                'makerAccountNumber': str(order['makerAccountNumber']),
                'expiration': str(order['expiration']),
                'salt': str(order['salt']),
                'typedSignature': order['typedSignature'],
            }

        return self._post('/v2/orders', data=json.dumps(
            utils.remove_nones({
                'fillOrKill': fillOrKill,
                'postOnly': postOnly,
                'clientId': clientId,
                'cancelAmountOnRevert': cancelAmountOnRevert,
                'cancelId': cancelId,
                'market': market_api_request,
                'order': order_api_request
            })
        ))

    def cancel_order(
        self,
        hash
    ):
        '''
        Cancel an order in a solo market.

        :param hash: required
        :type hash: str

        :returns: Order

        :raises: DydxAPIError
        '''
        signature = solo_orders.sign_cancel_order(hash, self.private_key)
        return self._delete(
            '/v2/orders/' + hash,
            headers={'Authorization': 'Bearer ' + signature}
        )

    def cancel_perpetual_order(
        self,
        hash
    ):
        '''
        Cancel an order in a perpetual market.

        :param hash: required
        :type hash: str

        :returns: Order

        :raises: DydxAPIError
        '''
        signature = perp_orders.sign_cancel_order(hash, self.private_key)
        return self._delete(
            '/v2/orders/' + hash,
            headers={'Authorization': 'Bearer ' + signature}
        )

    def get_orderbook(
        self,
        market
    ):
        '''
        Get the active orderbook for a market

        :param market: required, name of market (e.g. WETH-DAI)

        :returns: { asks: OrderOnOrderbook[], bids: OrderOnOrderbook[] }

        :raises: DydxAPIError
        '''
        return self._get('/v1/orderbook/' + market)

    def get_market(
        self,
        market
    ):
        '''
        Get market from market pair

        :param market: required
        :type market: str in list
            ["WETH-DAI", "WETH-USDC", "DAI-USDC"]

        :returns: { market: MarketMessageV2 }

        :raises: DydxAPIError
        '''
        return self._get('/v2/markets/' + market)

    def get_markets(
        self
    ):
        '''
        Get all markets

        :returns: { markets : { [market: str]: MarketMessageV2 } }

        :raises: DydxAPIError
        '''
        return self._get('/v2/markets')

    def get_perpetual_market(
        self,
        market
    ):
        '''
        Get market from market pair

        :param market: required
        :type market: str in list ["PBTC-USDC"]

        :returns: { market: PerpetualMarket }

        :raises: DydxAPIError
        '''
        return self._get('/v1/perpetual-markets/' + market)

    def get_perpetual_markets(
        self
    ):
        '''
        Get all markets

        :returns: { markets : [market: str]: PerpetualMarket } }

        :raises: DydxAPIError
        '''
        return self._get('/v1/perpetual-markets')

    def get_funding_rates(
        self,
        markets=None,
    ):
        '''
        Get the current and predicted funding rates.

        IMPORTANT: The `current` value returned by this function is not active
        until it has been mined on-chain, which may not happen for some period
        of time after the start of the hour. To get the funding rate that is
        currently active on-chain, use the get_perpetual_market() or
        get_perpetual_markets() function.

        The `current` rate is updated each hour, on the hour. The `predicted`
        rate is updated each minute, on the minute, and may be null if no
        premiums have been calculated since the last funding rate update.

        :param markets: optional, defaults to all Perpetual markets
        :type markets: str in list ["PBTC-USDC"]

        :returns: {
            [market: str]: { current: FundingRate, predicted: FundingRate }
        }

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
            'markets': None if markets is None else ','.join(markets),
        })
        return self._get('/v1/funding-rates' + params)

    def get_historical_funding_rates(
        self,
        markets=None,
        limit=None,
        startingBefore=None,
    ):
        '''
        Get historical funding rates.

        :param markets: optional, defaults to all Perpetual markets
        :type markets: str in list ["PBTC-USDC"]

        :param limit: optional, defaults to 100, which is the maximum
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str date and time (ISO-8601)

        :returns: { [market: str]: { history: FundingRate[] } }

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
                'markets': None if markets is None else ','.join(markets),
                'limit': limit,
                'startingBefore': startingBefore,
        })
        return self._get(
            '/v1/historical-funding-rates' + params,
        )

    def get_funding_index_price(
        self,
        markets=None,
    ):
        '''
        Get the index price used in the funding rate calculation.

        :param markets: optional, defaults to all Perpetual markets
        :type markets: str in list ["PBTC-USDC"]

        :returns: { [market: str]: { price: str } }

        :raises: DydxAPIError
        '''
        params = utils.dict_to_query_params({
            'markets': None if markets is None else ','.join(markets),
        })
        return self._get('/v1/index-price' + params)
