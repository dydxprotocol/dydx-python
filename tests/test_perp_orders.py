import dydx.perp_orders as perp_orders
from decimal import Decimal

PRIVATE_KEY_1 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PRIVATE_KEY_2 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'  # noqa: E501
ADDRESS_1 = '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1'
ADDRESS_2 = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
ADDRESS_1_NO_PREFIX = ADDRESS_1[2:]
ADDRESS_2_NO_PREFIX = ADDRESS_2[2:]
ORDER = {
    'isBuy': True,
    'amount': 10000,
    'limitPrice': Decimal('72.01'),
    'triggerPrice': Decimal(0),
    'limitFee':  Decimal('-0.00025'),
    'maker': ADDRESS_1,
    'taker': ADDRESS_2,
    'expiration': 1234,
    'salt': 0,
}
ORDER_HASH = '0x581a3e51afe0e0842ed4964a23d961cdf421999460860f1ab1a5a85d59bf9144'  # noqa: E501
CANCEL_ORDER_HASH = '0x4ae4ea46f1ede568682d3c69650d1411a6addaff8a13057901741bf9fae2fcc8'  # noqa: E501
ORDER_SIGNATURE = '0x49fb669e6e125cc4f41d84777a5fabfe3b5d32d4be23f744eb5054153545b76526ee0d025b9c017cf4cc6025d204ca1faae3c5fd90fb2a1a72dfa0791110ff991b01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0x12ac3ffc41c59b5bfcb9fe440db74a533eacefcb09a7a5c4f41735ed9e8d1b4f4368984ef254bbe1c672d0b89226d21126d58dcc38e83ae3a2fdf22e4d7f89021b01'  # noqa: E501


class TestPerpOrders():

    def test_perp_orders_get_order_hash(self):
        hash = perp_orders.get_order_hash(ORDER)
        assert hash == ORDER_HASH

    def test_perp_orders_get_cancel_order_hash(self):
        hash = perp_orders.get_cancel_order_hash(ORDER_HASH)
        assert hash == CANCEL_ORDER_HASH

    def test_perp_orders_sign_order(self):
        signature = perp_orders.sign_order(
            order=ORDER,
            private_key=PRIVATE_KEY_1
        )
        assert signature == ORDER_SIGNATURE

    def test_perp_orders_sign_cancel_order(self):
        signature = perp_orders.sign_cancel_order(
            order_hash=ORDER_HASH,
            private_key=PRIVATE_KEY_1
        )
        assert signature == CANCEL_ORDER_SIGNATURE
