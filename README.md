# dydx-python
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
from dydx-python.dydx.client import Client

# create a new client with a private key (string or bytearray)
client = Client('0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d')

# get all trading pairs for dydx
trading_pairs = client.get_pairs()

# ...
```

## Testing
```
# Install the requirements
pip install -r requirements.txt

# Run the tests
docker-compose up
tox
```
