import json
import os
import dydx.constants as consts
from web3 import Web3
from dydx.eth_solo import EthSolo
from dydx.eth_perp import EthPerp


class Eth(object):

    def __init__(
        self,
        node,
        private_key,
        public_address,
        account_number
    ):
        self.web3 = Web3(None if node is None else Web3.HTTPProvider(node))
        self.private_key = private_key
        self.public_address = public_address
        self.account_number = account_number
        self.min_nonce = self.web3.eth.getTransactionCount(self.public_address)

        self.solo = EthSolo(
            self,
            self.public_address,
            self.account_number,
        )
        self.perp = EthPerp(
            self,
            self.public_address,
        )

        self.weth_contract = self.create_contract(
            consts.WETH_ADDRESS,
            'abi/erc20.json'
        )
        self.sai_contract = self.create_contract(
            consts.SAI_ADDRESS,
            'abi/erc20.json'
        )
        self.usdc_contract = self.create_contract(
            consts.USDC_ADDRESS,
            'abi/erc20.json'
        )
        self.dai_contract = self.create_contract(
            consts.DAI_ADDRESS,
            'abi/erc20.json'
        )

    # -----------------------------------------------------------
    # Helper Functions
    # -----------------------------------------------------------

    def send_eth_transaction(
        self,
        method,
        options=None
    ):
        if options is None:
            options = dict()
        if 'from' not in options:
            options['from'] = self.public_address
        if 'nonce' not in options:
            options['nonce'] = max(
                self.min_nonce,
                self.web3.eth.getTransactionCount(self.public_address)
            )
        if 'gasPrice' not in options:
            try:
                options['gasPrice'] = \
                    self.web3.eth.gasPrice + consts.DEFAULT_GAS_PRICE_ADDITION
            except Exception:
                options['gasPrice'] = consts.DEFAULT_GAS_PRICE
        if 'value' not in options:
            options['value'] = 0
        if 'gas' not in options:
            try:
                options['gas'] = int(
                    method.estimateGas(options) *
                    consts.DEFAULT_GAS_MULTIPLIER
                )
            except Exception:
                options['gas'] = consts.DEFAULT_GAS_AMOUNT
        self.min_nonce = max(self.min_nonce, options['nonce'] + 1)
        tx = method.buildTransaction(options)
        stx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        return self.web3.eth.sendRawTransaction(stx.rawTransaction).hex()

    def create_contract(
        self,
        address,
        file_path
    ):
        this_folder = os.path.dirname(os.path.abspath(__file__))
        return self.web3.eth.contract(
            address=address,
            abi=json.load(open(os.path.join(this_folder, file_path), 'r'))
        )

    def get_token_contract(
        self,
        market
    ):
        if market == consts.MARKET_WETH:
            return self.weth_contract
        elif market == consts.MARKET_SAI:
            return self.sai_contract
        elif market == consts.MARKET_USDC:
            return self.usdc_contract
        elif market == consts.MARKET_DAI:
            return self.dai_contract
        else:
            raise ValueError('Invalid market number')

    def get_receipt(
        self,
        tx_hash
    ):
        '''
        Wait for a transaction to be mined and return the receipt

        :param tx_hash: required
        :type tx_hash: number

        :returns: transactionReceipt
        '''
        return self.web3.eth.waitForTransactionReceipt(tx_hash)

    # -----------------------------------------------------------
    # Transactions
    # -----------------------------------------------------------

    def set_allowance(
        self,
        market,
        spender
    ):
        '''
        Set allowance for some token for some spender.

        :param market: required
        :type market: number

        :param spender: required
        :type spender: string

        :returns: transactionHash

        :raises: ValueError
        '''
        contract = self.get_token_contract(market)

        # if allowance is already set, don't set allowance
        try:
            allowance = contract.functions.allowance(
                self.public_address,
                spender
            ).call()
            if allowance != 0:
                return
        except Exception:
            pass

        return self.send_eth_transaction(
            method=contract.functions.approve(
                spender,
                consts.MAX_SOLIDITY_UINT
            )
        )

    # -----------------------------------------------------------
    # Getters
    # -----------------------------------------------------------

    def get_my_wallet_balance(
        self,
        market
    ):
        '''
        Gets the on-chain balance of the users wallet for some asset.

        :param market: required
        :type market: number

        :returns: number
        '''
        return self.get_wallet_balance(
            address=self.public_address,
            market=market
        )

    def get_wallet_balance(
        self,
        address,
        market
    ):
        '''
        Gets the on-chain balance of a users wallet for some asset.

        :param address: required
        :type address: str (address)

        :param market: required
        :type market: number

        :returns: number
        '''
        if market == consts.MARKET_ETH:
            balance = self.web3.eth.getBalance(address)
        else:
            contract = self.get_token_contract(market)
            balance = contract.functions.balanceOf(address).call()
        return balance
