import json
import random
import requests
import dydx.util as utils
from dydx.eth import Eth
from .exceptions import DydxAPIError


class Client(object):

    TAKER_ACCOUNT_OWNER = '0xf809e07870dca762B9536d61A4fBEF1a17178092'
    TAKER_ACCOUNT_NUMBER = 0
    BASE_API_URI = 'https://api.dydx.exchange/v1/'

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
        return self._get('dex/pairs')

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
        return self._get('accounts/' + address, params=utils.remove_nones({
            'number': number
        }))

    def get_my_orders(
        self,
        pairs,
        limit=None,
        startingBefore=None
    ):
        '''
        Return open orders for the loaded account

        :param pairs: required
        :type pairs: list of str

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of existing orders

        :raises: DydxAPIError
        '''
        return self.get_orders(
            pairs=pairs,
            makerAccountOwner=self.public_address,
            makerAccountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_orders(
        self,
        pairs,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None
    ):
        '''
        Return all open orders

        :param pairs: required
        :type pairs: list of str

        :param makerAccountOwner: optional, defaults to self.public_address
        :type makerAccountOwner: str (address)

        :param makerAccountNumber: optional, defaults to self.account_number
        :type makerAccountNumber: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of existing orders

        :raises: DydxAPIError
        '''
        return self._get('dex/orders', params=utils.remove_nones({
            'pairs': ','.join(pairs),
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore
        }))

    def get_order(
        self,
        orderId,
    ):
        '''
        Return an order by id

        :param id: required
        :type id: str

        :returns: existing order

        :raises: DydxAPIError
        '''
        return self._get('dex/orders/'+orderId)

    def get_my_fills(
        self,
        pairs,
        limit=None,
        startingBefore=None
    ):
        '''
        Return historical fills for the loaded account

        :param pairs: required
        :type pairs: list of str

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of processed fills

        :raises: DydxAPIError
        '''
        return self.get_fills(
            pairs=pairs,
            makerAccountOwner=self.public_address,
            makerAccountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_fills(
        self,
        pairs,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None
    ):
        '''
        Return all historical fills

        :param pairs: required
        :type pairs: list of str

        :param makerAccountOwner: optional
        :type makerAccountOwner: str (address)

        :param makerAccountNumber: optional
        :type makerAccountNumber: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of processed fills

        :raises: DydxAPIError
        '''
        return self._get('dex/fills', params=utils.remove_nones({
            'pairs': ','.join(pairs),
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore
        }))

    def get_my_trades(
        self,
        pairs,
        limit=None,
        startingBefore=None
    ):
        '''
        Return historical trades for the loaded account

        :param pairs: required
        :type pairs: list of str

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of processed trades

        :raises: DydxAPIError
        '''
        return self.get_trades(
            pairs=pairs,
            makerAccountOwner=self.public_address,
            makerAccountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_trades(
        self,
        pairs,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None
    ):
        '''
        Return all historical trades

        :param pairs: required
        :type pairs: list of str

        :param makerAccountOwner: optional
        :type makerAccountOwner: str (address)

        :param makerAccountNumber: optional
        :type makerAccountNumber: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of processed trades

        :raises: DydxAPIError
        '''
        return self._get('dex/trades', params=utils.remove_nones({
            'pairs': ','.join(pairs),
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore
        }))

    def create_order(
        self,
        makerMarket,
        takerMarket,
        makerAmount,
        takerAmount,
        expiration=None,
        fillOrKill=False,
        clientId=None,
    ):
        '''
        Create an order

        :param makerMarket: required
        :type makerMarket: number

        :param takerMarket: required
        :type takerMarket: number

        :param makerAmount: required
        :type makerAmount: number

        :param takerAmount: required
        :type takerAmount: number

        :param expiration: optional, defaults to 28 days from now
        :type expiration: number

        :param fillOrKill: optional, defaults to False
        :type fillOrKill: bool

        :param clientId: optional, defaults to None
        :type clientId: string

        :returns: Order

        :raises: DydxAPIError
        '''

        order = {
            'makerMarket': makerMarket,
            'takerMarket': takerMarket,
            'makerAmount': makerAmount,
            'takerAmount': takerAmount,
            'makerAccountOwner': self.public_address,
            'makerAccountNumber': self.account_number,
            'takerAccountOwner': self.TAKER_ACCOUNT_OWNER,
            'takerAccountNumber': self.TAKER_ACCOUNT_NUMBER,
            'expiration': expiration or utils.epoch_in_four_weeks(),
            'salt': random.randint(0, 2**256)
        }
        order['typedSignature'] = utils.sign_order(order, self.private_key)

        return self._post('dex/orders', data=json.dumps(utils.remove_nones({
            'fillOrKill': fillOrKill,
            'clientId': clientId,
            'order': {k: str(v) for k, v in order.items()}
        })))

    def cancel_order(
        self,
        hash
    ):
        '''
        Cancel an order

        :param hash: required
        :type hash: str

        :returns: Order

        :raises: DydxAPIError
        '''
        signature = utils.sign_cancel_order(hash, self.private_key)
        return self._delete(
            'dex/orders/' + hash,
            headers={'Authorization': 'Bearer ' + signature}
        )
