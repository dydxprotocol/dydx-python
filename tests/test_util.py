import pytest
import dydx.util as utils
import dydx.constants as consts

PRIVATE_KEY_1 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PRIVATE_KEY_2 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'  # noqa: E501
ADDRESS_1 = '0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1'
ADDRESS_2 = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
ADDRESS_1_NO_PREFIX = ADDRESS_1[2:]
ADDRESS_2_NO_PREFIX = ADDRESS_2[2:]
ORDER = {
    'makerMarket': 0,
    'takerMarket': 1,
    'makerAmount': 100,
    'takerAmount': 200,
    'makerAccountOwner': ADDRESS_1,
    'makerAccountNumber': 111,
    'takerAccountOwner': ADDRESS_2,
    'takerAccountNumber': 222,
    'expiration': 1234,
    'salt': 4321
}
ORDER_HASH = '0x998ec84efeb9d5b2e20820722d90a9430ec7085ad45bbd7b2cd6b312abe294c5'  # noqa: E501
CANCEL_ORDER_HASH = '0x54da43ec40e5ae61b2dac3d9068cd56d257459bc105ad0317857b7b4f66e101c'  # noqa: E501
ORDER_SIGNATURE = '0x342f7533477aff89c3d25facdecb3875a68ccb5271a79dca64d19c822a6a8d560dba1ce392a50d7cd0d76ee45cfd8e6627764b012970bf43f6f8fd61677cf2ba1c01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0xe1381f81b47132cc23809ddff717b40d52f3a4c7cbb49f85aadf2f893c6f433c05d5cc4143694630ac504429b1c325251dec3dde9fec6c02f95246663c0f4b7f1c01'  # noqa: E501


class TestUtil():

    def test_util_get_order_hash(self):
        assert utils.get_order_hash(ORDER) == ORDER_HASH

    def test_util_get_cancel_order_hash(self):
        assert utils.get_cancel_order_hash(ORDER_HASH) == CANCEL_ORDER_HASH

    def test_util_hash_string(self):
        assert utils.hash_string('baconfries') == \
            '0xae5dd6cd2427c8b9f8600be5fe223f87913bb47c1b1cef18792a34033f6d752a'  # noqa: E501

    def test_util_strip_hex_prefix(self):
        assert utils.strip_hex_prefix(ADDRESS_1_NO_PREFIX) == ADDRESS_1_NO_PREFIX  # noqa: E501
        assert utils.strip_hex_prefix(ADDRESS_1) == ADDRESS_1_NO_PREFIX

    def test_util_address_to_bytes32(self):
        expected_result = '0x' + ADDRESS_1_NO_PREFIX.zfill(64)
        assert utils.address_to_bytes32(ADDRESS_1_NO_PREFIX) == expected_result
        assert utils.address_to_bytes32(ADDRESS_1) == expected_result

    def test_util_normalize_private_key(self):
        ek_pk = utils.normalize_private_key(PRIVATE_KEY_1)
        assert '0x' + ek_pk.hex() == PRIVATE_KEY_1
        assert utils.normalize_private_key(ek_pk) == ek_pk
        with pytest.raises(TypeError) as error:
            utils.normalize_private_key(0x1234)
        assert 'private_key incorrect type' in str(error.value)

    def test_util_private_key_to_address(self):
        ek_pk_1 = utils.normalize_private_key(PRIVATE_KEY_1)
        ek_pk_2 = utils.normalize_private_key(PRIVATE_KEY_2)
        assert utils.private_key_to_address(ek_pk_1) == ADDRESS_1
        assert utils.private_key_to_address(ek_pk_2) == ADDRESS_2

    def test_sign_order(self):
        signature = utils.sign_order(
            order=ORDER,
            private_key=PRIVATE_KEY_1
        )
        assert signature == ORDER_SIGNATURE

    def test_sign_cancel_order(self):
        signature = utils.sign_cancel_order(
            order_hash=ORDER_HASH,
            private_key=PRIVATE_KEY_1
        )
        assert signature == CANCEL_ORDER_SIGNATURE

    def test_sign_hash(self):
        signature = utils.sign_hash(
            hash=ORDER_HASH,
            private_key=PRIVATE_KEY_1
        )
        assert signature == ORDER_SIGNATURE
        signature = utils.sign_hash(
            hash=CANCEL_ORDER_HASH,
            private_key=PRIVATE_KEY_1
        )
        assert signature == CANCEL_ORDER_SIGNATURE

    def test_token_to_wei(self):
        assert utils.token_to_wei(11, consts.MARKET_WETH) == \
            11 * (10 ** 18)
        assert utils.token_to_wei(22, consts.MARKET_DAI) == \
            22 * (10 ** 18)
        assert utils.token_to_wei(33, consts.MARKET_USDC) == \
            33 * (10 ** 6)
