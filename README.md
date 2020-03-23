<p align="center"><img src="https://s3.amazonaws.com/dydx-assets/dydx_logo_black.svg" width="256" /></p>

<div align="center">
  <a href="https://circleci.com/gh/dydxprotocol/workflows/dydx-python/tree/master">
    <img src="https://img.shields.io/circleci/project/github/dydxprotocol/dydx-python.svg" alt='CI' />
  </a>
  <a href='https://pypi.org/project/dydx-python'>
    <img src='https://img.shields.io/pypi/v/dydx-python.svg' alt='PyPi'/>
  </a>
  <a href='https://github.com/dydxprotocol/dydx-python/blob/master/LICENSE'>
    <img src='https://img.shields.io/github/license/dydxprotocol/dydx-python.svg?longCache=true' alt='License' />
  </a>
</div>

dYdX Python API for Limit Orders

The library is currently tested against Python versions 2.7, 3.4, 3.5, and 3.6

## Installation
`dydx-python` is available on [PyPI](https://pypi.org/project/dydx-python). Install with `pip`:
```
pip install dydx-python
```

## Documentation

Check the [dYdX developer docs](https://docs.dydx.exchange/#/api?id=orderbook) for the API endpoint.

## Example Usage

### Initializing the client

```python
from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

# create a new client with a private key (string or bytearray)
client = Client(
    private_key='0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d',
    node='https://parity.expotrading.com'
)
```

### HTTP API Calls

#### Trading Pairs

```python
# Get all trading pairs for dydx
pairs = client.get_pairs()
```

#### Account Balances

```python
# Get my account balances
my_balances = client.get_my_balances()

# Get balances of another account
balances = client.get_balances(
    address='0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1',
    number=0
)
```

#### Open Orders

```python
# Get orders created by my account for both sides of the book
my_orders = client.get_my_orders(
    market=['WETH-DAI', 'DAI-WETH'],
    limit=None,
    startingBefore=None
)

# Get all orders for both sides of the book
ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
all_orders = client.get_orders(
    market=['WETH-DAI', 'DAI-WETH'],
    makerAccountOwner=None,  # optional
    makerAccountNumber=None,  # optional
    limit=2,  # optional
    startingBefore=ten_days_ago  # optional
)
```

#### Historical Fills

```python
# Get fills created by my account for both sides of the orderbook
my_fills = client.get_my_fills(
    market=['WETH-DAI', 'DAI-WETH'],
    limit=None,  # optional
    startingBefore=None  # optional
)

# Get all fills from one side of the book
all_fills = client.get_fills(
    market=['WETH-DAI'], # 'DAI-WETH' side of the book is not included
    makerAccountOwner='0x5F5A46a8471F60b1E9F2eD0b8fc21Ba8b48887D8',  # optional
    makerAccountNumber=0,  # optional
    limit=2,  # optional
    startingBefore=None  # optional
)
'''
fills = {
  "fills": [
    {
      uuid: "b53ab8c4-465f-4950-add2-dd807c048d68",
      createdAt: "2020-03-08T17:42:36.037Z",
      transactionHash: "0x39576745c2f030ba04bf4df7bcc64ffaa97421243c53e714bca4161163be9d51",
      status: "PENDING",
      market: "WETH-DAI",
      side: "BUY",
      feeAmount: "0",
      orderClientId: null,
      price: "217.019",
      amount: "15000000000000000000",
      orderId: "0x8924cdc0d18899d250bfa27d5929967e26e7e676745a28b6ee5b3a8f182ceb9f",
      accountOwner: "0x8a9d46d28003673cd4fe7a56ecfcfa2be6372e64",
      accountNumber: "63397253610709255086306580859198088914565604507660670583302927962305720029570",
      liquidity: "TAKER"
    },
    ...
  ]
}
'''

# Get one order by id
order = client.get_order(
  orderId,
)
'''
order = {
  "order" = {
    "uuid": "c95c386a-307d-4fbf-bcac-a7ff965a7207",
    "id": "0x812f2e71081daa820d08fa25c76c06332cd39282433679a413c03c5d4591bc35",
    "clientId": "d046f4db-12a9-48fb-b413-6916a9f0cfff",
    "status": "CANCELED",
    "accountOwner": "0x862821badb9c5800654015ba9a2d9d7894c83a7a",
    "accountNumber": "0",
    "orderType": "LIMIT",
    "fillOrKill": false,
    "postOnly": false,
    "triggerPrice": null,
    "market": "WETH-DAI",
    "side": "BUY",
    "baseAmount": "186056800000000000000",
    "quoteAmount": "39808712928000001179648",
    "filledAmount": "0",
    "price": "213.96",
    "cancelReason": "USER_CANCELED",
    "createdAt": "2020-03-08T17:35:24.694Z",
    "updatedAt": "2020-03-08T17:35:25.474Z",
    "expiresAt": "2020-03-08T17:55:29.000Z"
  }
}
'''
```

#### Historical Trades

```python
# Get trades created by my account for both sides of the orderbook
my_trades = client.get_my_trades(
    market=['WETH-DAI', 'DAI-WETH'],
    limit=None,  # optional
    startingBefore=None  # optional
)

# Get all trades from one side of the book
all_trades = client.get_trades(
    market=['WETH-DAI'], # 'DAI-WETH' side of the book is not included
    makerAccountOwner='0x5F5A46a8471F60b1E9F2eD0b8fc21Ba8b48887D8',  # optional
    makerAccountNumber=0,  # optional
    limit=2,  # optional
    startingBefore=None  # optional
)
'''
trades = {
  "trades": [
    {
      "uuid": "7b00efba-5002-4562-b777-0122ede33fec",
      "createdAt": "2020-03-08T17:32:35.413Z",
      "transactionHash": "0xfd6fe9605114a5d44000b51d126751eee1f38866ebd4d4be7eacf89d8bf264d9",
      "status": "CONFIRMED",
      "market": "WETH-DAI",
      "side": "SELL",
      "price": "214.90",
      "amount": "2447332508052454104",
      "makerOrderId": "0x9e5cf0e5091566651ad33c56fb4e24ce96341b561d31180f0d471163709b098d",
      "makerAccountOwner": "0x862821badb9c5800654015ba9a2d9d7894c83a7a",
      "makerAccountNumber": "0",
      "takerOrderId": "0xc1a71851c62fc132ece0060c46a076cb082741ef6b80f894b20c4351b824dfb7",
      "takerAccountOwner": "0xd3069c9e486a8b77add55ae3ceb3a4b138fb76c7",
      "takerAccountNumber": "48394678789855236190833155557217125360276244141304950018155758748772338730587"
    },
    ...
  ]
}
'''
```

#### Create an Order

```python
# Create order to BUY 10 ETH for 2504.90 DAI (a price of 250.49 DAI/ETH)
created_order = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_BUY,
    amount=utils.token_to_wei(10, consts.MARKET_WETH),
    price=Decimal('250.49'),
    fillOrKill=False,
    postOnly=False
)

# Create order to SELL 10 ETH for 1500.10 USDC (a price of 150.01 USDC/ETH)
# 'e-12' is in the price since USDC has 6 decimal places (ETH and DAI have 18)
created_order = client.place_order(
    market=consts.PAIR_WETH_USDC,
    side=consts.SIDE_SELL,
    amount=utils.token_to_wei(10, consts.MARKET_WETH),
    price=Decimal('150.01e-12'),
    fillOrKill=False,
    postOnly=False
)
```

#### Cancel an Order

```python
# Cancel the previously created order
order_hash = created_order['order']['id']
canceled_order = client.cancel_order(
    hash=order_hash
)
```

#### Get Orderbook

```python
orderbook = client.get_orderbook(
    market='WETH-DAI'
)
'''
orderbook = {
  "bids": [
    {
      "id": "0xefa4562c0747a8f2a9aa69abb817474ee9e98c8505a71de6054a610ac744b0cd",
      "uuid": "c58be890-6e76-4e98-95d4-27977a91af19",
      "amount": "17459277053478281216",
      "price": "160.08"
    },
    {
      "id": "0xa2ab9f653106fefef5b1264a509b02eab021ffea442307e995908e5360f3cd4d",
      "uuid": "d2dba4c6-6442-46bc-b097-1f37312cf279",
      "amount": "149610989871929360384",
      "price": "160.07"
    },
    {
      "id": "0xec35d60dd1c5eab86cd7881fcbc1239193ceda695df2815d521a46f54bd90580",
      "uuid": "24d5a4e1-195b-43fa-a7d8-1d794619e97e",
      "amount": "54494000000000000000",
      "price": "160.06"
    },
  ],
  "asks": [
    {
      "id": "0xb242e2006a0d99c390fc7256d10558844a719d580e80eaa5a4f99dd14bd9ce5e",
      "uuid": "6fdff2f3-0175-4297-bf23-89526eb9aa36",
      "amount": "12074182754430260637",
      "price": "160.30"
    },
    {
      "id": "0xe32a00e11b91b6f8daa70fbe03ad0100fa458c0d87e5c59f2e629ce9d5d32921",
      "uuid": "3f9b35a8-d843-4ae6-bc8b-b534b07e8093",
      "amount": "50000000000000000000",
      "price": "160.40"
    },
    {
      "id": "0xcad0c2e92094bd1dd17a694bd25933a8825c6014aaf4ae2925512f62c15ae968",
      "uuid": "5aefdfd2-4e4d-4b37-9c99-35e8eec0ed9a",
      "amount": "50000000000000000000",
      "price": "160.50"
    },
  ]
}
'''
```

#### Get Market

```python
market = client.get_market(
    market='WETH-DAI'
)
'''
mock_get_market_json = {
  "market": {
    "WETH-DAI": {
        "name": "WETH-DAI",
        "baseCurrency": {
          "currency": "WETH",
          "decimals": 18,
          "soloMarketId": 0,
        },
        "quoteCurrency": {
          "currency": "DAI",
          "decimals": 18,
          "soloMarketId": 3,
        },
        "minimumTickSize": "0.01",
        "minimumOrderSize": "100000000000000000",
        "smallOrderThreshold": "500000000000000000",
        "makerFee": "0",
        "largeTakerFee": "0.005",
        "smallTakerFee": "0.0015",
    },
  }
}
'''
```

#### Get Markets

```python
market = client.get_markets()
'''
mock_get_markets_json = {
  "markets": {
    "WETH-DAI": {
      "name": "WETH-DAI",
      "baseCurrency": {
        "currency": "WETH",
        "decimals": 18,
        "soloMarketId": 0,
      },
      "quoteCurrency": {
        "currency": "DAI",
        "decimals": 18,
        "soloMarketId": 3,
      },
      "minimumTickSize": "0.01",
      "minimumOrderSize": "100000000000000000",
      "smallOrderThreshold": "500000000000000000",
      "makerFee": "0",
      "largeTakerFee": "0.005",
      "smallTakerFee": "0.0015",
    },
    "WETH-USDC": {
      "name": "WETH-USDC",
      "baseCurrency": {
        "currency": "WETH",
        "decimals": 18,
        "soloMarketId": 0,
      },
      "quoteCurrency": {
        "currency": "USDC",
        "decimals": 6,
        "soloMarketId": 2,
      },
      "minimumTickSize": "0.00000000000001",
      "minimumOrderSize": "100000000000000000",
      "smallOrderThreshold": "500000000000000000",
      "makerFee": "0",
      "largeTakerFee": "0.005",
      "smallTakerFee": "0.0015",
    },
    "DAI-USDC": {
      "name": "DAI-USDC",
      "baseCurrency": {
        "currency": "DAI",
        "decimals": 18,
        "soloMarketId": 3,
      },
      "quoteCurrency": {
        "currency": "USDC",
        "decimals": 6,
        "soloMarketId": 1,
      },
      "minimumTickSize": "0.0000000000000001",
      "minimumOrderSize": "20000000000000000000",
      "smallOrderThreshold": "100000000000000000000",
      "makerFee": "0",
      "largeTakerFee": "0.005",
      "smallTakerFee": "0.0005",
    },
  }
}
'''
```

### Ethereum Transactions

```python
# deposit 10 ETH
# does not require set_allowance
tx_hash = client.eth.deposit(
  market=consts.MARKET_WETH,
  wei=utils.token_to_wei(10, consts.MARKET_WETH)
)
receipt = client.eth.get_receipt(tx_hash)


# deposit 100 DAI
tx_hash = client.eth.set_allowance(market=consts.MARKET_DAI) # must only be called once, ever
receipt = client.eth.get_receipt(tx_hash)

tx_hash = client.eth.deposit(
  market=consts.MARKET_DAI,
  wei=utils.token_to_wei(100, consts.MARKET_DAI)
)
receipt = client.eth.get_receipt(tx_hash)


# deposit 100 USDC
tx_hash = client.eth.set_allowance(market=consts.MARKET_USDC) # must only be called once, ever
receipt = client.eth.get_receipt(tx_hash)

tx_hash = client.eth.deposit(
  market=consts.MARKET_USDC,
  wei=utils.token_to_wei(100, consts.MARKET_USDC)
)
receipt = client.eth.get_receipt(tx_hash)


# withdraw 50 USDC
tx_hash = client.eth.withdraw(
  market=consts.MARKET_USDC,
  wei=utils.token_to_wei(50, consts.MARKET_USDC)
)
receipt = client.eth.get_receipt(tx_hash)


# withdraw all DAI (including interest)
tx_hash = client.eth.withdraw_to_zero(market=consts.MARKET_DAI)
receipt = client.eth.get_receipt(tx_hash)
```

### Ethereum Getters

Getting information directly from the blockchain by querying a node

```python
# get the USD value of one atomic unit of DAI
dai_price = client.eth.get_oracle_price(consts.MARKET_DAI)

# get dYdX balances
balances = client.eth.get_my_balances()
'''
balances = [
  -91971743707894,
  3741715702031854553560,
  2613206278
]
'''

# get Wallet balances
balance = client.eth.get_my_wallet_balance(consts.MARKET_DAI)
'''
balance = 1000000000000000000
'''

# get dYdX account collateralization
collateralization = client.eth.get_my_collateralization()
'''
collateralization = 2.5 or float('inf')
'''

# collateralization must remain above the minimum to prevent liquidation
assert(collateralization > consts.MINIMUM_COLLATERALIZATION)
'''
consts.MINIMUM_COLLATERALIZATION = 1.15
'''
```

## Testing
```
# Install the requirements
pip install -r requirements.txt

# Run the tests
docker-compose up
tox
```
