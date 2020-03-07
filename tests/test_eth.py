import pytest
import re
import web3
import dydx.constants as consts
from dydx.client import Client

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
    'limitPrice': 250.01,
    'triggerPrice': 0,
    'limitFee':  0.0050,
    'makerAccountOwner': ADDRESS_1,
    'makerAccountNumber': 111,
    'expiration': 1234,
    'salt': 0,
}
ORDER_HASH = '0x50538cce27ddd08a8a3732aaedb90b5ef55fd92a6819f5798edc043833776405'  # noqa: E501
CANCEL_ORDER_HASH = '0xca25945c7cbc05dda130cff8f92acd555c464e22239e0864637aeec402e556c5'  # noqa: E501
ORDER_SIGNATURE = '0x229e6e1926aadea40b933dd6b12c9f4daac3267df5ca31041c72a9f6f2a057fe6257a664cca749be666f4452b1aa3587f5bc844c6b4fe7c835da8a4cabf9fa461b01'  # noqa: E501
CANCEL_ORDER_SIGNATURE = '0xe760368bbdb904809d2383606e27b9ab8ed57f47ce37dc67d4f87e59bb9102c46447f7ce20f1751cd7d670f2b7e4dec61da3288f242d3a003cc70b13a8560f7c1b01'  # noqa: E501
LOCAL_NODE = 'http://0.0.0.0:8545'
CONTRACT_NOT_FOUND_ERROR = 'Could not transact with/call contract function'


class TestEth():

    # ------------ Constructor ------------

    def test_constructor(self):
        pass

    # -----------------------------------------------------------
    # Transactions
    # -----------------------------------------------------------

    def _validate_tx_hash(self, client, tx_hash):
        assert re.compile("^0x[a-f0-9]{64}").match(tx_hash)
        receipt = client.eth.get_receipt(tx_hash)
        assert receipt['transactionHash'].hex() == tx_hash

    # ------------ set_allowance ------------

    def test_set_allowance_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.set_allowance(market=consts.MARKET_WETH)
        self._validate_tx_hash(client, tx_hash)

    def test_set_allowance_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.set_allowance(market=consts.MARKET_DAI)
        self._validate_tx_hash(client, tx_hash)

    def test_set_allowance_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.eth.set_allowance(market=consts.MARKET_INVALID)
        assert 'Invalid market number' in str(error.value)

    # ------------ deposit ------------

    def test_deposit_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.deposit(
            market=consts.MARKET_WETH,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_deposit_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.deposit(
            market=consts.MARKET_DAI,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_deposit_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.eth.deposit(
                market=consts.MARKET_INVALID,
                wei=1000
            )
        assert 'Invalid market number' in str(error.value)

    # ------------ withdraw ------------

    def test_withdraw_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw(
            market=consts.MARKET_WETH,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw(
            market=consts.MARKET_DAI,
            wei=1000
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_eth_to_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw(
            market=consts.MARKET_WETH,
            wei=1000,
            to=ADDRESS_2
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_dai_to_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw(
            market=consts.MARKET_DAI,
            wei=1000,
            to=ADDRESS_2
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.eth.withdraw(
                market=consts.MARKET_INVALID,
                wei=1000
            )
        assert 'Invalid market number' in str(error.value)

    # ------------ withdraw_to_zero ------------

    def test_withdraw_to_zero_eth_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw_to_zero(
            market=consts.MARKET_WETH
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_to_zero_dai_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw_to_zero(
            market=consts.MARKET_DAI
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_to_zero_eth_to_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw_to_zero(
            market=consts.MARKET_WETH,
            to=ADDRESS_2
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_to_zero_dai_to_success(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        tx_hash = client.eth.withdraw_to_zero(
            market=consts.MARKET_DAI,
            to=ADDRESS_2
        )
        self._validate_tx_hash(client, tx_hash)

    def test_withdraw_to_zero_unknown_failure(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(ValueError) as error:
            client.eth.withdraw_to_zero(market=consts.MARKET_INVALID)
        assert 'Invalid market number' in str(error.value)

    # -----------------------------------------------------------
    # Getters
    # -----------------------------------------------------------

    # ------------ get_oracle_price ------------

    def test_get_oracle_price(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_oracle_price(consts.MARKET_DAI)
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)

    # ------------ get_my_wallet_balance ------------

    def test_get_my_wallet_balance(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_my_wallet_balance(consts.MARKET_DAI)
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)

    def test_get_my_wallet_balance_eth(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        balance = client.eth.get_my_wallet_balance(consts.MARKET_ETH)
        assert balance > 0

    # ------------ get_wallet_balance ------------

    def test_get_wallet_balance(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_wallet_balance(
                address=ADDRESS_2,
                market=consts.MARKET_DAI
            )
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)

    def test_get_wallet_balance_eth(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        balance = client.eth.get_wallet_balance(
            address=ADDRESS_2,
            market=consts.MARKET_ETH
        )
        assert balance > 0

    # ------------ get_my_collateralization ------------

    def test_get_my_collateralization(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_my_collateralization()
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)

    # ------------ get_collateralization ------------

    def test_get_collateralization(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_collateralization(
                address=ADDRESS_2,
                accountNumber=1111,
            )
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)

    # ------------ get_my_balances ------------

    def test_get_my_balances(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_my_balances()
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)

    # ------------ get_my_balances ------------

    def test_get_balances(self):
        client = Client(PRIVATE_KEY_1, node=LOCAL_NODE)
        with pytest.raises(web3.exceptions.BadFunctionCallOutput) as error:
            client.eth.get_balances(
                address=ADDRESS_2,
                accountNumber=1111,
            )
        assert CONTRACT_NOT_FOUND_ERROR in str(error.value)
