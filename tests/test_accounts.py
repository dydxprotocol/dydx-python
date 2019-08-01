from web3 import Web3

from dydx.accounts import Accounts


class TestAccounts():

    def test_basic(self):
        accounts = Accounts(Web3.HTTPProvider('http://0.0.0.0:8445'))
        accounts
