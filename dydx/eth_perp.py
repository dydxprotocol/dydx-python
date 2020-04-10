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
        self.perpetual = self.eth.create_contract(
            consts.PERPETUAL_ADDRESS,
            'abi/perpetualv1.json'
        )
        self.oracle = self.eth.create_contract(
            None,  # address to be set later
            'abi/p1oracle.json'
        )

    # -----------------------------------------------------------
    # Transactions
    # -----------------------------------------------------------

    def set_allowance(
        self
    ):
        '''
        Set allowance on the Perpetual for some token. Must be done only once.

        :returns: transactionHash

        :raises: ValueError
        '''
        return self.eth.set_allowance(
            consts.MARKET_USDC,
            consts.PERPETUAL_ADDRESS,
        )

    def deposit(
        self,
        amount
    ):
        '''
        Deposit funds into the protocol

        :param amount: required
        :type amount: number

        :returns: transactionHash

        :raises: ValueError
        '''
        return self.eth.send_eth_transaction(
            method=self.perpetual.functions.deposit(
                self.public_address,
                amount
            )
        )

    def withdraw(
        self,
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
        return self.eth.send_eth_transaction(
            method=self.perpetual.functions.withdraw(
                self.public_address,
                destination,
                amount
            )
        )

    # -----------------------------------------------------------
    # Getters
    # -----------------------------------------------------------

    def get_oracle_price(
        self
    ):
        '''
        Gets the on-chain price of an asset from the price oracle.

        :returns: number
        '''
        if self.oracle.address is None:
            self.oracle.address = \
                self.perpetual.functions.getOracleContract().call()
        price = self.oracle.functions.getPrice().call(
            {'from': consts.PERPETUAL_ADDRESS}
        )
        return price / (10 ** 18)

    def get_my_balances(
        self
    ):
        '''
        Gets dYdX balances for my account.

        :returns: Object { margin: number, position, number }
        '''
        return self.get_balances(self.public_address)

    def get_balances(
        self,
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
        result = self.perpetual.functions.getAccountBalance(address).call()
        (marginIsPositive, positionIsPositive, margin, position) = result
        return {
            'margin': margin if marginIsPositive else -margin,
            'position': position if positionIsPositive else -position
        }
