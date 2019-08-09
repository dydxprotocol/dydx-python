# dydx-python
dYdX Python API for Limit Orders

The library is currently tested against Python versions 2.7, 3.4, 3.5, and 3.6

## Installation
`dydx-python` is available on [PyPI](https://pypi.org/project/dydx-python). Install with `pip`:
```
pip install dydx-python
```

## Usage

```python
from dydx-python.dydx.client import Client

# create a new client with a private key (string or bytearray)
client = Client(private_key)

# get all trading pairs for dydx
trading_pairs = client.get_pairs()

# ...
```

## Documentation

(to be added soon)


## Testing
```
# Install the requirements
pip install -r requirements.txt

# Run the tests
docker-compose up
tox
```
