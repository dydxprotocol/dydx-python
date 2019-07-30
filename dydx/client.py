import requests
import six

from web3 import Web3, HTTPProvider

import dydx.util

class Client(object):

    BASE_API_URI = 'https://api.dydx.exchange/v1/dex/'

    def __init__(self, provider):
        self.W3 = Web3(provider)

    # Public API
    # -----------------------------------------------------------

    def get_orders(self, pair):
        pass

    def get_fills(self, pair):
        pass

    def create_order(self, order):
        pass

    def delete_order(self, order):
        pass
