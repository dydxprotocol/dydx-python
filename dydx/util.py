from web3 import Web3
import eth_keys
import eth_account
import time
import dydx.constants as consts

EIP712_ORDER_STRUCT_STRING = \
  'LimitOrder(' + \
  'uint256 makerMarket,' + \
  'uint256 takerMarket,' + \
  'uint256 makerAmount,' + \
  'uint256 takerAmount,' + \
  'address makerAccountOwner,' + \
  'uint256 makerAccountNumber,' + \
  'address takerAccountOwner,' + \
  'uint256 takerAccountNumber,' + \
  'uint256 expiration,' + \
  'uint256 salt' + \
  ')'

EIP712_DOMAIN_STRING = \
  'EIP712Domain(' + \
  'string name,' + \
  'string version,' + \
  'uint256 chainId,' + \
  'address verifyingContract' + \
  ')'

EIP712_CANCEL_ORDER_STRUCT_STRING = \
  'CancelLimitOrder(' + \
  'string action,' + \
  'bytes32[] orderHashes' + \
  ')'

EIP712_CANCEL_ACTION = 'Cancel Orders'


def get_eip712_hash(domain_hash, struct_hash):
    return Web3.solidityKeccak(
        [
            'bytes2',
            'bytes32',
            'bytes32'
        ],
        [
            '0x1901',
            domain_hash,
            struct_hash
        ]
    ).hex()


def get_domain_hash():
    return Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
            'uint256',
            'bytes32'
        ],
        [
            hash_string(EIP712_DOMAIN_STRING),
            hash_string('LimitOrders'),
            hash_string('1.1'),
            consts.NETWORK_ID,
            address_to_bytes32(consts.LIMIT_ORDERS_ADDRESS)
        ]
    ).hex()


def get_order_hash(order):
    '''
    Returns the final signable EIP712 hash for an order.
    '''
    struct_hash = Web3.solidityKeccak(
        [
            'bytes32',
            'uint256',
            'uint256',
            'uint256',
            'uint256',
            'bytes32',
            'uint256',
            'bytes32',
            'uint256',
            'uint256',
            'uint256'
        ],
        [
            hash_string(EIP712_ORDER_STRUCT_STRING),
            order['makerMarket'],
            order['takerMarket'],
            order['makerAmount'],
            order['takerAmount'],
            address_to_bytes32(order['makerAccountOwner']),
            order['makerAccountNumber'],
            address_to_bytes32(order['takerAccountOwner']),
            order['takerAccountNumber'],
            order['expiration'],
            order['salt']
        ]
    ).hex()
    return get_eip712_hash(get_domain_hash(), struct_hash)


def get_cancel_order_hash(order_hash):
    '''
    Returns the final signable EIP712 hash for a cancel order API call.
    '''
    action_hash = Web3.solidityKeccak(
        ['string'],
        [EIP712_CANCEL_ACTION]
    ).hex()
    orders_hash = Web3.solidityKeccak(
        ['bytes32'],
        [order_hash]
    ).hex()
    struct_hash = Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
        ],
        [
            hash_string(EIP712_CANCEL_ORDER_STRUCT_STRING),
            action_hash,
            orders_hash,
        ]
    ).hex()
    return get_eip712_hash(get_domain_hash(), struct_hash)


def hash_string(input):
    return Web3.solidityKeccak(['string'], [input]).hex()


def strip_hex_prefix(input):
    if input[0:2] == '0x':
        return input[2:]
    else:
        return input


def address_to_bytes32(addr):
    return '0x000000000000000000000000' + strip_hex_prefix(addr)


def normalize_private_key(private_key):
    if type(private_key) == str:
        return bytearray.fromhex(strip_hex_prefix(private_key))
    elif type(private_key) == bytearray:
        return private_key
    else:
        raise TypeError('private_key incorrect type')


def private_key_to_address(key):
    eth_keys_key = eth_keys.keys.PrivateKey(key)
    return eth_keys_key.public_key.to_checksum_address()


def sign_order(order, private_key):
    order_hash = get_order_hash(order)
    return sign_hash(order_hash, private_key)


def sign_cancel_order(order_hash, private_key):
    cancel_order_hash = get_cancel_order_hash(order_hash)
    return sign_hash(cancel_order_hash, private_key)


def sign_hash(hash, private_key):
    result = eth_account.account.Account.sign_message(
        eth_account.messages.encode_defunct(hexstr=hash),
        private_key
    )
    return result['signature'].hex() + '01'


def remove_nones(original):
    return {k: v for k, v in original.items() if v is not None}


def epoch_in_four_weeks():
    return int(time.time()) + consts.FOUR_WEEKS_IN_SECONDS


def token_to_wei(amount, market):
    if market == 0:
        decimals = consts.DECIMALS_WETH
    elif market == 1:
        decimals = consts.DECIMALS_SAI
    elif market == 2:
        decimals = consts.DECIMALS_USDC
    elif market == 3:
        decimals = consts.DECIMALS_DAI
    else:
        raise ValueError('Invalid market number')
    return int(amount * (10 ** decimals))
