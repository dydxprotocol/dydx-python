import dydx.constants as consts


class EthSolo(object):

    def __init__(
        self,
        eth,
        public_address,
        account_number
    ):
        self.eth = eth
        self.public_address = public_address
        self.account_number = account_number

        # initialize contracts
        self.solo_margin = self.eth.create_contract(
            consts.SOLO_MARGIN_ADDRESS,
            'abi/solomargin.json'
        )
        self.payable_proxy = self.eth.create_contract(
            consts.PAYABLE_PROXY_ADDRESS,
            'abi/payableproxy.json'
        )

    # -----------------------------------------------------------
    # Private Helper Functions
    # -----------------------------------------------------------

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
            return self.eth.send_eth_transaction(
                self.payable_proxy.functions.operate(
                    accounts,
                    operations,
                    otherAddress
                ),
                options=txOptions
            )
        else:
            return self.eth.send_eth_transaction(
                self.solo_margin.functions.operate(
                    accounts,
                    operations
                ),
                options=txOptions
            )

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
        return self.eth.set_allowance(
            market,
            consts.SOLO_MARGIN_ADDRESS,
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
