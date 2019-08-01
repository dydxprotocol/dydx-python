import pytest
from dydx.client import Client

PRIVATE_KEY = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'  # noqa: E501
PUBLIC_ADDRESS = '0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1'
PUBLIC_ADDRESS_2 = '0xffcf8fdee72ac11b5c542428b35eef5769c409f0'


class TestClient():

    def test_constructor_string_private_key(self):
        client = Client(PRIVATE_KEY)
        assert(client.public_address == PUBLIC_ADDRESS)
        assert(client.account_number == '0')

    def test_constructor_bytes_private_key(self):
        client = Client(bytearray.fromhex(PRIVATE_KEY[2:]))
        assert(client.public_address == PUBLIC_ADDRESS)
        assert(client.account_number == '0')

    def test_constructor_public_address(self):
        client = Client(PRIVATE_KEY, public_address=PUBLIC_ADDRESS)
        assert(client.public_address == PUBLIC_ADDRESS)
        assert(client.account_number == '0')

    def test_constructor_account_number(self):
        client = Client(PRIVATE_KEY, account_number='1')
        assert(client.account_number == '1')

    def test_constructor_bad_private_key(self):
        with pytest.raises(TypeError):
            Client(1)

    def test_constructor_no_private_key(self):
        with pytest.raises(TypeError):
            Client()

    def test_constructor_bad_public_address(self):
        with pytest.raises(ValueError) as error:
            Client(PRIVATE_KEY, public_address=PUBLIC_ADDRESS_2)
        assert 'private_key/public_address mismatch' in str(error.value)
