import json
import os
import dydx.constants as consts
from web3 import Web3


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

        # initialize contracts
        self.solo_margin = self._create_contract(
            consts.SOLO_MARGIN_ADDRESS,
            'abi/solomargin.json'
        )
        self.payable_proxy = self._create_contract(
            consts.PAYABLE_PROXY_ADDRESS,
            'abi/payableproxy.json'
        )
        self.weth_contract = self._create_contract(
            consts.WETH_ADDRESS,
            'abi/erc20.json'
        )
        self.sai_contract = self._create_contract(
            consts.SAI_ADDRESS,
            'abi/erc20.json'
        )
        self.usdc_contract = self._create_contract(
            consts.USDC_ADDRESS,
            'abi/erc20.json'
        )
        self.dai_contract = self._create_contract(
            consts.DAI_ADDRESS,
            'abi/erc20.json'
        )

    # -----------------------------------------------------------
    # Private Helper Functions
    # -----------------------------------------------------------

    def _send_eth_transaction(
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

    def _operate(
        self,
        actionType,
        market,
        wei,
        ref,
        otherAddress
    ):
        if market < 0 or market >= consts.MARKET_INVALID:
            raise ValueError('Invalid market number')

        isDeposit = (actionType == consts.ACTION_TYPE_DEPOSIT)
        accounts = [{
            'owner': self.public_address,
            'number': self.account_number
        }]
        amountField = {
            'sign': isDeposit,
            'denomination': 0,  # wei
            'ref': ref,
            'value': wei
        }
        actualWithdrawOrDepositAddress = (
            consts.PAYABLE_PROXY_ADDRESS
            if market == consts.MARKET_WETH
            else otherAddress
        )
        operations = [{
            'actionType': actionType,
            'accountId': 0,
            'amount': amountField,
            'primaryMarketId': market,
            'secondaryMarketId': 0,
            'otherAddress': actualWithdrawOrDepositAddress,
            'otherAccountId': 0,
            'data': '0x'
        }]
        txOptions = dict(
            value=(
                wei
                if (isDeposit and market == consts.MARKET_WETH)
                else 0
            )
        )

        if market == consts.MARKET_WETH:
            return self._send_eth_transaction(
                self.payable_proxy.functions.operate(
                    accounts,
                    operations,
                    otherAddress
                ),
                options=txOptions
            )
        else:
            return self._send_eth_transaction(
                self.solo_margin.functions.operate(
                    accounts,
                    operations
                ),
                options=txOptions
            )

    def _create_contract(
        self,
        address,
        file_path
    ):
        this_folder = os.path.dirname(os.path.abspath(__file__))
        return self.web3.eth.contract(
            address=address,
            abi=json.load(open(os.path.join(this_folder, file_path), 'r'))
        )

    def _get_token_contract(
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

    # -----------------------------------------------------------
    # Public Helper Functions
    # -----------------------------------------------------------

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
        market
    ):
        '''
        Set allowance on Solo for some token. Must be done only once per
        market. Not necessary for WETH (market 0)

        :param market: required
        :type market: number

        :returns: transactionHash

        :raises: ValueError
        '''
        contract = self._get_token_contract(market)

        # if allowance is already set, don't set allowance
        try:
            allowance = contract.functions.allowance(
                self.public_address,
                consts.SOLO_MARGIN_ADDRESS
            ).call()
            if allowance != 0:
                return
        except Exception:
            pass

        return self._send_eth_transaction(
            method=contract.functions.approve(
                consts.SOLO_MARGIN_ADDRESS,
                consts.MAX_SOLIDITY_UINT
            )
        )

    def deposit(
        self,
        market,
        wei
    ):
        '''
        Deposit funds into the protocol

        :param market: required
        :type market: number

        :param wei: required
        :type wei: number

        :returns: transactionHash

        :raises: ValueError
        '''
        return self._operate(
            actionType=consts.ACTION_TYPE_DEPOSIT,
            market=market,
            wei=wei,
            ref=consts.REFERENCE_DELTA,
            otherAddress=self.public_address
        )

    def withdraw(
        self,
        market,
        wei,
        to=None
    ):
        '''
        Withdraw funds from the protocol

        :param market: required
        :type market: number

        :param wei: required
        :type wei: number

        :param to: optional
        :type to: str (address)

        :returns: transactionHash

        :raises: ValueError
        '''
        return self._operate(
            actionType=consts.ACTION_TYPE_WITHDRAW,
            market=market,
            wei=wei,
            ref=consts.REFERENCE_DELTA,
            otherAddress=(to or self.public_address)
        )

    def withdraw_to_zero(
        self,
        market,
        to=None
    ):
        '''
        Withdraw all funds from the protocol for one asset

        :param market: required
        :type market: number

        :param to: optional
        :type to: str (address)

        :returns: transactionHash

        :raises: ValueError
        '''
        return self._operate(
            actionType=consts.ACTION_TYPE_WITHDRAW,
            market=market,
            wei=0,
            ref=consts.REFERENCE_TARGET,
            otherAddress=(to or self.public_address)
        )

    # -----------------------------------------------------------
    # Getters
    # -----------------------------------------------------------

    def get_oracle_price(
        self,
        market
    ):
        '''
        Gets the on-chain price of an asset from the price oracle.
        Returns the price of 1 wei (atomic amount) of the asset in USD.

        :param market: required
        :type market: number

        :returns: number
        '''
        price = self.solo_margin.functions.getMarketPrice(market).call()[0]
        return price / (consts.PRICE_ORACLE_USD_MULTIPLIER)

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
            contract = self._get_token_contract(market)
            balance = contract.functions.balanceOf(address).call()
        return balance

    def get_my_collateralization(
        self
    ):
        '''
        Gets collateralization of my account.

        :returns: number
        '''
        return self.get_collateralization(
            self.public_address,
            self.account_number
        )

    def get_collateralization(
        self,
        address,
        accountNumber
    ):
        '''
        Gets collateralization of some account.

        :param address: required
        :type address: str (address)

        :param accountNumber: required
        :type accountNumber: number

        :returns: number
        '''
        [supply], [borrow] = self.solo_margin.functions.getAccountValues([
            address,
            accountNumber,
        ]).call()

        if borrow == 0:
            return float('inf')
        return supply / borrow

    def get_my_balances(
        self
    ):
        '''
        Gets dYdX balances for my account.

        :returns: number
        '''
        return self.get_balances(
            self.public_address,
            self.account_number
        )

    def get_balances(
        self,
        address,
        accountNumber
    ):
        '''
        Gets dYdX balances for some account.

        :param address: required
        :type address: str (address)

        :param accountNumber: required
        :type accountNumber: number

        :returns: number
        '''
        _, _, weis = self.solo_margin.functions.getAccountBalances([
            address,
            accountNumber,
        ]).call()
        result = list(map(
            lambda wei: wei[1] if wei[0] else -wei[1],
            weis
        ))
        return result
