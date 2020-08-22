import dydx.constants as consts


class EthPerp(object):

    def __init__(
        self,
        eth,
        public_address
    ):
        self.eth = eth
        self.public_address = public_address

        # initialize contracts
        self.btc_perpetual = self.eth.create_contract(
            consts.BTC_PERPETUAL_ADDRESS,
            'abi/perpetualv1.json'
        )
        self.link_perpetual = self.eth.create_contract(
            consts.LINK_PERPETUAL_ADDRESS,
            'abi/perpetualv1.json'
        )
        self.eth_perpetual = self.eth.create_contract(
            consts.ETH_PERPETUAL_ADDRESS,
            'abi/perpetualv1.json'
        )
        self.weth_proxy = self.eth.create_contract(
            consts.WETH_PROXY_ADDRESS,
            'abi/wethproxy.json'
        )

    def _get_perpetual_by_market(
        self,
        market
    ):
        if market == consts.PAIR_PBTC_USDC:
            return self.btc_perpetual
        elif market == consts.PAIR_PLINK_USDC:
            return self.link_perpetual
        elif market == consts.PAIR_WETH_PUSD:
            return self.eth_perpetual
        else:
            raise ValueError('Invalid market')

    # -----------------------------------------------------------
    # Transactions
    # -----------------------------------------------------------

    def set_allowance(
        self,
        market
    ):
        '''
        Set allowance on the Perpetual for some token. Must be done only once.

        :returns: transactionHash

        :raises: ValueError
        '''
        if market == consts.PAIR_PBTC_USDC:
            return self.eth.set_allowance(
                consts.MARKET_USDC,
                consts.BTC_PERPETUAL_ADDRESS,
            )
        if market == consts.PAIR_PLINK_USDC:
            return self.eth.set_allowance(
                consts.MARKET_USDC,
                consts.LINK_PERPETUAL_ADDRESS,
            )
        if market == consts.PAIR_WETH_PUSD:
            return self.eth.set_allowance(
                consts.MARKET_WETH,
                consts.ETH_PERPETUAL_ADDRESS,
            )

    def deposit(
        self,
        market,
        amount
    ):
        '''
        Deposit funds into the protocol

        :param amount: required
        :type amount: number

        :returns: transactionHash

        :raises: ValueError
        '''

        if market == consts.PAIR_WETH_PUSD:
            return self.eth.send_eth_transaction(
                method=self.weth_proxy.functions.depositEth(
                    consts.ETH_PERPETUAL_ADDRESS,
                    self.public_address
                ),
                options={'value': amount}
            )
        else:
            perpetual = self._get_perpetual_by_market(market)
            return self.eth.send_eth_transaction(
                method=perpetual.functions.deposit(
                    self.public_address,
                    amount
                )
            )

    def withdraw(
        self,
        market,
        amount,
        to=None
    ):
        '''
        Withdraw funds from the protocol

        :param amount: required
        :type amount: number

        :param to: optional
        :type to: str (address)

        :returns: transactionHash

        :raises: ValueError
        '''
        destination = to or self.public_address

        if market == consts.PAIR_WETH_PUSD:
            return self.eth.send_eth_transaction(
                method=self.weth_proxy.functions.withdrawEth(
                    consts.ETH_PERPETUAL_ADDRESS,
                    self.public_address,
                    destination,
                    amount
                )
            )
        else:
            perpetual = self._get_perpetual_by_market(market)
            return self.eth.send_eth_transaction(
                method=perpetual.functions.withdraw(
                    self.public_address,
                    destination,
                    amount
                )
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

        :returns: number
        '''
        perpetual = self._get_perpetual_by_market(market)
        price = perpetual.functions.getOraclePrice().call(
            {'from': consts.CURRENCY_CONVERTER_PROXY_ADDRESS}
        )
        return price / (10 ** 18)

    def get_my_balances(
        self,
        market
    ):
        '''
        Gets dYdX balances for my account.

        :returns: Object { margin: number, position, number }
        '''
        return self.get_balances(market, self.public_address)

    def get_balances(
        self,
        market,
        address
    ):
        '''
        Gets dYdX balances for some account.

        :param address: required
        :type address: str (address)

        :param accountNumber: required
        :type accountNumber: number

        :returns: Object { margin: number, position, number }
        '''
        perpetual = self._get_perpetual_by_market(market)
        result = perpetual.functions.getAccountBalance(address).call()
        (marginIsPositive, positionIsPositive, margin, position) = result
        return {
            'margin': margin if marginIsPositive else -margin,
            'position': position if positionIsPositive else -position
        }
