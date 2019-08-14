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

```python
from dydx.client import Client

# create a new client with a private key (string or bytearray)
client = Client(
    private_key='0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d',
    node='https://parity.expotrading.com'
)

# -----------------------------------------------------------
# API Calls
# -----------------------------------------------------------

# get all trading pairs for dydx
trading_pairs = client.get_pairs()

# ...

# -----------------------------------------------------------
# Ethereum Transactions
# -----------------------------------------------------------

# deposit 10 ETH
# does not require set_allowance
tx_hash = client.deposit(market=0, wei=(10 * 1e18)) # ETH has 18 decimal places

# deposit 100 DAI
tx_hash = client.set_allowance(market=1) # must only be called once, ever
tx_hash = client.deposit(market=1, wei=(100 * 1e18)) # DAI has 18 decimal places

# deposit 100 USDC
tx_hash = client.set_allowance(market=2) # must only be called once, ever
tx_hash = client.deposit(market=2, wei=(100 * 1e6)) # USDC has 6 decimal places

# withdraw 50 USDC
tx_hash = client.withdraw(market=2, wei=(100 * 1e6)) # USDC has 6 decimal places

# withdraw all DAI (including interest)
tx_hash = client.withdraw_to_zero(market=1)
```

## Testing
```
# Install the requirements
pip install -r requirements.txt

# Run the tests
docker-compose up
tox
```
