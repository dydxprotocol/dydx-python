from web3 import Web3
import eth_keys

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


def get_order_hash(order):
    '''
    Returns the final signable EIP712 hash for an order.
    '''
    domain_hash = Web3.soliditySha3(
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
            hash_string('1.0'),
            1,
            '0xeb32d60A5cDED175cea9aFD0f2447297C125F2f4'
        ]
    )
    struct_hash = Web3.soliditySha3(
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
            order.maker_market,
            order.taker_market,
            order.maker_amount,
            order.taker_amount,
            address_to_bytes32(order.maker_account_owner),
            order.maker_account_number,
            address_to_bytes32(order.taker_account_owner),
            order.taker_account_number,
            order.expiration,
            order.salt
        ]
    )

    return Web3.soliditySha3(
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
    )


def get_cancel_order_hash(order_hash):
    return Web3.soliditySha3(
        ['string', 'bytes32'],
        ['cancel', order_hash]
    )


def hash_string(input):
    return Web3.soliditySha3(['string'], [input])


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
    return eth_keys_key.public_key.to_checksum_address().lower()
