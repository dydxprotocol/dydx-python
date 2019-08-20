import json
import os
import random
import requests
import dydx.util as utils
import dydx.constants as consts
from web3 import Web3
from .exceptions import DydxAPIError


class Client(object):

    TAKER_ACCOUNT_OWNER = '0xf809e07870dca762B9536d61A4fBEF1a17178092'
    TAKER_ACCOUNT_NUMBER = 0
    BASE_API_URI = 'https://api.dydx.exchange/v1/'

    def __init__(
        self,
        private_key,
        account_number=0,
        node=None
    ):
        provider = None if node is None else Web3.HTTPProvider(node)
        self.web3 = Web3(provider)
        self.private_key = utils.normalize_private_key(private_key)
        self.account_number = account_number
        self.public_address = utils.private_key_to_address(self.private_key)
        self.session = self._init_session()

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
        self.dai_contract = self._create_contract(
            consts.DAI_ADDRESS,
            'abi/erc20.json'
        )
        self.usdc_contract = self._create_contract(
            consts.USDC_ADDRESS,
            'abi/erc20.json'
        )

    # -----------------------------------------------------------
    # Helper Methods
    # -----------------------------------------------------------

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

    def _init_session(self):
        session = requests.session()
        session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'dydx/python'
        })
        return session

    def _request(self, method, uri, **kwargs):
        complete_uri = self.BASE_API_URI + uri
        response = getattr(self.session, method)(complete_uri, **kwargs)
        if not str(response.status_code).startswith('2'):
            raise DydxAPIError(response)
        return response.json()

    def _get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request('put', *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request('delete', *args, **kwargs)

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
            options['nonce'] = \
                self.web3.eth.getTransactionCount(self.public_address)
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
        tx = method.buildTransaction(options)
        stx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        return self.web3.eth.sendRawTransaction(stx.rawTransaction).hex()

    def _operate(
        self,
        actionType,
        market,
        wei,
        ref,
    ):
        if (market == 0):
            otherAddress = consts.PAYABLE_PROXY_ADDRESS
        elif market == 1 or market == 2:
            otherAddress = self.public_address
        else:
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
        operations = [{
            'actionType': actionType,
            'accountId': 0,
            'amount': amountField,
            'primaryMarketId': market,
            'secondaryMarketId': 0,
            'otherAddress': otherAddress,
            'otherAccountId': 0,
            'data': '0x'
        }]

        if (market == 0):
            return self._send_eth_transaction(
                self.payable_proxy.functions.operate(
                    accounts,
                    operations,
                    self.public_address
                ),
                options=dict(
                    value=wei
                )
            )
        else:
            return self._send_eth_transaction(
                self.solo_margin.functions.operate(
                    accounts,
                    operations
                ),
                options=dict(
                    value=0
                )
            )

    def _get_token_contract(
        self,
        market
    ):
        if market == 0:
            return self.weth_contract
        elif market == 1:
            return self.dai_contract
        elif market == 2:
            return self.usdc_contract
        else:
            raise ValueError('Invalid market number')

    # -----------------------------------------------------------
    # Public API
    # -----------------------------------------------------------

    def get_pairs(
        self
    ):
        '''
        Return all tradable pairs

        :returns: list of trading pairs

        :raises: DydxAPIError
        '''
        return self._get('dex/pairs')

    def get_my_balances(
        self
    ):
        '''
        Return balances for the loaded account

        :returns: list of balances

        :raises: DydxAPIError
        '''
        return self.get_balances(
            address=self.public_address,
            number=self.account_number
        )

    def get_balances(
        self,
        address,
        number=0
    ):
        '''
        Return balances for an address and account number

        :param address: required
        :type address: str (address)

        :param number: optional, defaults to 0
        :type number: number

        :returns: list of balances

        :raises: DydxAPIError
        '''
        return self._get('accounts/' + address, params=utils.remove_nones({
            'number': number
        }))

    def get_my_orders(
        self,
        pairs,
        limit=None,
        startingBefore=None
    ):
        '''
        Return open orders for the loaded account

        :param pairs: required
        :type pairs: list of str

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of existing orders

        :raises: DydxAPIError
        '''
        return self.get_orders(
            pairs=pairs,
            makerAccountOwner=self.public_address,
            makerAccountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_orders(
        self,
        pairs,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None
    ):
        '''
        Return all open orders

        :param pairs: required
        :type pairs: list of str

        :param makerAccountOwner: optional, defaults to self.public_address
        :type makerAccountOwner: str (address)

        :param makerAccountNumber: optional, defaults to self.account_number
        :type makerAccountNumber: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of existing orders

        :raises: DydxAPIError
        '''
        return self._get('dex/orders', params=utils.remove_nones({
            'pairs': ','.join(pairs),
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore
        }))

    def get_my_fills(
        self,
        pairs,
        limit=None,
        startingBefore=None
    ):
        '''
        Return historical fills for the loaded account

        :param pairs: required
        :type pairs: list of str

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of processed fills

        :raises: DydxAPIError
        '''
        return self.get_fills(
            pairs=pairs,
            makerAccountOwner=self.public_address,
            makerAccountNumber=self.account_number,
            limit=limit,
            startingBefore=startingBefore
        )

    def get_fills(
        self,
        pairs,
        makerAccountOwner=None,
        makerAccountNumber=None,
        limit=None,
        startingBefore=None
    ):
        '''
        Return all historical fills

        :param pairs: required
        :type pairs: list of str

        :param makerAccountOwner: optional
        :type makerAccountOwner: str (address)

        :param makerAccountNumber: optional
        :type makerAccountNumber: number

        :param limit: optional, defaults to 100
        :type limit: number

        :param startingBefore: optional, defaults to now
        :type startingBefore: str (ISO-8601)

        :returns: list of processed fills

        :raises: DydxAPIError
        '''
        return self._get('dex/fills', params=utils.remove_nones({
            'pairs': ','.join(pairs),
            'makerAccountOwner': makerAccountOwner,
            'makerAccountNumber': makerAccountNumber,
            'limit': limit,
            'startingBefore': startingBefore
        }))

    def create_order(
        self,
        makerMarket,
        takerMarket,
        makerAmount,
        takerAmount,
        expiration=None,
        fillOrKill=False
    ):
        '''
        Create an order

        :param makerMarket: required
        :type makerMarket: number

        :param takerMarket: required
        :type takerMarket: number

        :param makerAmount: required
        :type makerAmount: number

        :param takerAmount: required
        :type takerAmount: number

        :param expiration: optional, defaults to 28 days from now
        :type expiration: number

        :param fillOrKill: optional, defaults to False
        :type fillOrKill: bool

        :returns: Order

        :raises: DydxAPIError
        '''

        order = {
            'makerMarket': makerMarket,
            'takerMarket': takerMarket,
            'makerAmount': makerAmount,
            'takerAmount': takerAmount,
            'makerAccountOwner': self.public_address,
            'makerAccountNumber': self.account_number,
            'takerAccountOwner': self.TAKER_ACCOUNT_OWNER,
            'takerAccountNumber': self.TAKER_ACCOUNT_NUMBER,
            'expiration': expiration or utils.epoch_in_four_weeks(),
            'salt': random.randint(0, 2**256)
        }
        order['typedSignature'] = utils.sign_order(order, self.private_key)

        return self._post('dex/orders', data=json.dumps({
            'fillOrKill': fillOrKill,
            'order': {k: str(v) for k, v in order.items()}
        }))

    def cancel_order(
        self,
        hash
    ):
        '''
        Cancel an order

        :param hash: required
        :type hash: str

        :returns: Order

        :raises: DydxAPIError
        '''
        signature = utils.sign_cancel_order(hash, self.private_key)
        return self._delete(
            'dex/orders/' + hash,
            headers={'Authorization': 'Bearer ' + signature}
        )

    # -----------------------------------------------------------
    # Ethereum Transactions
    # -----------------------------------------------------------

    def enable_limit_orders(
        self
    ):
        '''
        Set the LimitOrders contract as an operator for your account

        :returns: transactionHash
        '''
        try:
            is_operator = self.solo_.functions.getIsLocalOperator(
                self.public_address,
                consts.LIMIT_ORDERS_ADDRESS
            ).call()
            if is_operator:
                return
        except Exception:
            pass

        return self._send_eth_transaction(
            method=self.solo_margin.functions.setOperators([{
                'operator': consts.LIMIT_ORDERS_ADDRESS,
                'trusted': True
            }])
        )

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
            ref=consts.REFERENCE_DELTA
        )

    def withdraw(
        self,
        market,
        wei
    ):
        '''
        Withdraw funds from the protocol

        :param market: required
        :type market: number

        :param wei: required
        :type wei: number

        :returns: transactionHash

        :raises: ValueError
        '''
        return self._operate(
            actionType=consts.ACTION_TYPE_WITHDRAW,
            market=market,
            wei=wei,
            ref=consts.REFERENCE_DELTA
        )

    def withdraw_to_zero(
        self,
        market
    ):
        '''
        Withdraw all funds from the protocol for one asset

        :param market: required
        :type market: number

        :returns: transactionHash

        :raises: ValueError
        '''
        return self._operate(
            actionType=consts.ACTION_TYPE_WITHDRAW,
            market=market,
            wei=0,
            ref=consts.REFERENCE_TARGET
        )

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
