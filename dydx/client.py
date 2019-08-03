import json
import random
import requests
import dydx.util as utils
from web3 import Web3
from .exceptions import DydxAPIError


class Client(object):

    TAKER_ACCOUNT_OWNER = '0xf809e07870dca762B9536d61A4fBEF1a17178092'
    TAKER_ACCOUNT_NUMBER = 0
    BASE_API_URI = 'https://api.dydx.exchange/v1/'

    def __init__(self, private_key, public_address=None, account_number=0):
        self.web3 = Web3()
        self.private_key = utils.normalize_private_key(private_key)
        self.account_number = account_number
        self.public_address = utils.private_key_to_address(self.private_key)
        if public_address and self.public_address != public_address.lower():
            raise ValueError('private_key/public_address mismatch')
        self.session = self._init_session()

    # ------------ Helper Methods ------------

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

    # ------------ Public API ------------

    def get_pairs(
        self
    ):
        '''
        Return all tradable pairs

        :returns: Array of trading pairs

        :raises: DydxAPIError
        '''
        return self._get('dex/pairs')

    def get_balances(
        self,
        address=None,
        number=None
    ):
        '''
        Return all balances for an address and account number

        :param address: optional
        :type address: address string

        :param number: optional
        :type number: number

        :returns: Array of balances

        :raises: DydxAPIError
        '''
        if address is None:
            address = self.public_address
        if number is None:
            number = self.account_number

        return self._get('accounts/' + address, params=utils.remove_nones({
            'number': number
        }))

    def get_orders(
        self,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None,
    ):
        '''
        Return all open orders for an address

        :param makerAccountOwner: optional, defaults to self.public_address
        :type makerAccountOwner: address string

        :param makerAccountOwner: optional, defaults to self.account_number
        :type makerAccountOwner: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: ISO-8601 string

        :returns: Array of existing orders

        :raises: DydxAPIError
        '''
        if makerAccountOwner is None:
            makerAccountOwner = self.public_address
        if makerAccountNumber is None:
            makerAccountNumber = self.account_number

        return self._get('dex/orders', params=utils.remove_nones({
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore,
        }))

    def get_fills(
        self,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None,
    ):
        '''
        Return all historical fills for an address

        :param makerAccountOwner: optional, defaults to self.public_address
        :type makerAccountOwner: address string

        :param makerAccountOwner: optional, defaults to self.account_number
        :type makerAccountOwner: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: ISO-8601 string

        :returns: Array of processed fills

        :raises: DydxAPIError
        '''
        if makerAccountOwner is None:
            makerAccountOwner = self.public_address
        if makerAccountNumber is None:
            makerAccountNumber = self.account_number

        return self._get('dex/fills', params=utils.remove_nones({
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore,
        }))

    def create_order(
        self,
        makerMarket,
        takerMarket,
        makerAmount,
        takerAmount,
        fillOrKill=False
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

        :param fillOrKill: optional, defaults to False
        :type fillOrKill: bool

        :returns: None

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
            'expiration': 0,
            'salt': random.randint(0, 2**256)
        }
        order['typedSignature'] = utils.sign_order(order, self.private_key)

        return self._post('dex/orders', data=json.dumps({
            'fillOrKill': fillOrKill,
            'order': {k: str(v) for k, v in order.items()}
        }))

    def delete_order(
        self,
        hash
    ):
        '''
        Delete an order

        :param hash: required
        :type hash: string

        :returns: None

        :raises: DydxAPIError
        '''
        signature = utils.sign_cancel_order(hash, self.private_key)
        return self._delete(
            'dex/orders/' + hash,
            headers={'Authorization': 'Bearer ' + signature}
        )
