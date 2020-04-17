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
CANCEL_ORDER_HASH = '0xf89b2620ce49bd09ebc0af2326953d0891cd76b96afa6150821cae441e9fb9e9'  # noqa: E501
ORDER_SIGNATURE = '0x49fb669e6e125cc4f41d84777a5fabfe3b5d32d4be23f744eb5054153545b76526ee0d025b9c017cf4cc6025d204ca1faae3c5fd90fb2a1a72dfa0791110ff991b01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0x63ea4af15870834996ab3fea1fa77b42dc0d98c4571c2a00e968fa7b3b80384175f6a7699265fec0e97f089aac36231b34f25010915eaf8eb9c7d29702fd18321c01'  # noqa: E501


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
