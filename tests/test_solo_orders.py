import dydx.solo_orders as solo_orders
from decimal import Decimal

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


class TestSoloOrders():

    def test_solo_orders_get_order_hash(self):
        hash = solo_orders.get_order_hash(ORDER)
        assert hash == ORDER_HASH

    def test_solo_orders_get_cancel_order_hash(self):
        hash = solo_orders.get_cancel_order_hash(ORDER_HASH)
        assert hash == CANCEL_ORDER_HASH

    def test_solo_orders_sign_order(self):
        signature = solo_orders.sign_order(
            order=ORDER,
            private_key=PRIVATE_KEY_1
        )
        assert signature == ORDER_SIGNATURE

    def test_solo_orders_sign_cancel_order(self):
        signature = solo_orders.sign_cancel_order(
            order_hash=ORDER_HASH,
            private_key=PRIVATE_KEY_1
        )
        assert signature == CANCEL_ORDER_SIGNATURE
