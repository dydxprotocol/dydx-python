import random
import requests
import dydx.util as utils

from web3 import Web3


class Client(object):

    TAKER_ACCOUNT_OWNER = '0x0000000000000000000000000000000000000000'
    TAKER_ACCOUNT_NUMBER = '0'
    BASE_API_URI = 'https://api.dydx.exchange/v1/dex/'

    def __init__(self, private_key, public_address=None, account_number='0'):
        self.web3 = Web3()
        self.private_key = utils.normalize_private_key(private_key)
        self.account_number = account_number
        self.public_address = utils.private_key_to_address(self.private_key)
        if public_address and self.public_address != public_address.lower():
            raise ValueError('private_key/public_address mismatch')
        self.session = self._init_session()

    # ------------ Signing Methods ------------

    def sign_order(self, order):
        order_hash = utils.get_order_hash(order)
        signature = self.web3.eth.accounts.sign(
            order_hash,
            self.private_key
        )
        typedSignature = signature + '01'
        return typedSignature

    def sign_cancel_order(self, order_hash):
        cancel_order_hash = utils.get_cancel_order_hash(order_hash)
        signature = self.web3.eth.accounts.sign(
            cancel_order_hash,
            self.private_key
        )
        typedSignature = signature + '01'
        return typedSignature

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
            raise Exception(response)
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

    def get_pairs(self):
        '''
        Return all tradable pairs
        :returns: Array of trading pairs
        :raises: Exception
        '''
        return self._get('pairs')

    def get_balances(self, **params):
        '''
        Return all balances for an address and account number
        :param owner: required
        :type owner: string
        :param account_number: required
        :type account_number: string
        :returns: Array of balances
        :raises: Exception
        '''
        return self._get('balances', params=params)

    def get_orders(self, **params):
        '''
        Return all open orders for an address (paginated)
        :param makerAccountOwner: required
        :type makerAccountOwner: string
        :param limit: required
        :type limit: number
        :param startingAfter: required
        :type startingAfter: ISO-8601 string
        :returns: Array of existing orders
        :raises: Exception
        '''
        return self._get('orders', params=params)

    def get_fills(self, **params):
        '''
        Return all historical fills for an address (paginated)
        :param makerAccountOwner: required
        :type makerAccountOwner: string
        :param limit: required
        :type limit: number
        :param startingAfter: required
        :type startingAfter: ISO-8601 string
        :returns: Array of processed fills
        :raises: Exception
        '''
        return self._get('fills', params=params)

    def create_order(self, **data):
        '''
        Create an order
        :param fillOrKill: required e.g. false
        :type fillOrKill: bool
        :param order: required
        :type order: order
        :returns: None
        :raises: Exception
        '''
        order = data['order']

        if 'makerMarket' not in order:
            raise KeyError('makerMarket not specified in order')
        if 'takerMarket' not in order:
            raise KeyError('takerMarket not specified in order')
        if 'makerAmount' not in order:
            raise KeyError('makerAmount not specified in order')
        if 'takerAmount' not in order:
            raise KeyError('takerAmount not specified in order')

        order.makerAccountOwner = self.public_address
        order.makerAccountNumber = self.account_number
        order.takerAccountOwner = self.TAKER_ACCOUNT_OWNER
        order.takerAccountNumber = self.TAKER_ACCOUNT_NUMBER
        order.expiration = '0'
        order.salt = str(random.randInt(0, 2**256))
        order.typedSignature = self.sign_order(data['order'])
        return self._post('orders', data=data)

    def delete_order(self, orderHash):
        '''
        Delete an order
        :param orderHash: required
        :type orderHash: string
        :param typedSignature: required
        :type typedSignature: string
        :returns: None
        :raises: Exception
        '''
        typedSignature = self.sign_cancel_order(orderHash)
        return self._delete(
            'orders/' + orderHash,
            headers={'Authorization': typedSignature}
        )
