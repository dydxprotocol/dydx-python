import json
import six
import pytest

from web3 import Web3

from dydx.client import Client

class TestClient():

    def test_basic(self):
        client = Client(Web3.HTTPProvider('http://0.0.0.0:8445'))
