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
ORDER_HASH = '0x0ca9eefb9f4fc6469bf691ab23e02db08396d51a0c48cad6c959a7e42f869c84'  # noqa: E501
CANCEL_ORDER_HASH = '0xbb6799cd525ea485f92f0b20854a53504f277a7d8f33a39c5c15364318cb330a'  # noqa: E501
ORDER_SIGNATURE = '0x0d47146d7d105adba200d6474fc587ed97956dd694ba31b38b268253b5e4095951bd9fd525741aa5a2192f5daebc3027e8a4895a7c5158554b4abc88f56e15201b01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0x25963ec4420752af9db7ee043a7868f7920d18cd3e7bffce061789d0dedeef2248bdd6074933b8d8d862f7eab07304ed69c91e8603f7cde93bc06591703678be1b01'  # noqa: E501


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
