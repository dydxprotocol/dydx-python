import requests


class Client(object):

    BASE_API_URI = 'https://api.dydx.exchange/v1/dex/'

    def __init__(self):
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
        response = getattr(self.session, method)(uri, **kwargs)
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

    def get_orders(self, **params):
        """
        Return all open orders for an address
        :param makerAccountOwner: required
        :type makerAccountOwner: string
        :returns: Array of existing orders
        :raises: Exception
        """
        return self._get('orders', params=params)

    def get_fills(self, **params):
        """
        Return all historical fills for an address
        :param makerAccountOwner: required
        :type makerAccountOwner: string
        :returns: Array of processed fills
        :raises: Exception
        """
        return self._get('fills', params=params)

    def create_order(self, **data):
        """
        Create an order
        :param fillOrKill: required e.g. false
        :type fillOrKill: bool
        :param order: required
        :type order: order
        :returns: None
        :raises: Exception
        """
        return self._post('orders', data=data)

    def delete_order(self, orderHash, typedSignature):
        """
        Delete an order
        :param orderHash: required
        :type orderHash: string
        :param typedSignature: required
        :type typedSignature: string
        :returns: None
        :raises: Exception
        """
        return self._delete(
            'orders/' + orderHash,
            headers={'Authorization': typedSignature}
        )
