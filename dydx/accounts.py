from web3 import Web3

from dydx.util import get_order_hash, get_cancel_order_hash


class Accounts(object):

    def __init__(self, provider):
        self.w3 = Web3(provider)

    def sign_order(self, order):
        order_hash = get_order_hash(order)
        signature = self.w3.eth.sign(
            order.maker_account_owner,
            order_hash
        )
        typedSignature = signature + '01'
        return typedSignature

    def sign_cancel_order(self, order):
        cancel_order_hash = get_cancel_order_hash(order)
        signature = self.w3.eth.sign(
            order.maker_account_owner,
            cancel_order_hash
        )
        typedSignature = signature + '01'
        return typedSignature
