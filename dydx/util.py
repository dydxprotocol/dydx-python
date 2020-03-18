from web3 import Web3
import eth_keys
import eth_account
import time
import dydx.constants as consts

EIP712_ORDER_STRUCT_STRING = \
  'CanonicalOrder(' + \
  'bytes32 flags,' + \
  'uint256 baseMarket,' + \
  'uint256 quoteMarket,' + \
  'uint256 amount,' + \
  'uint256 limitPrice,' + \
  'uint256 triggerPrice,' + \
  'uint256 limitFee,' + \
  'address makerAccountOwner,' + \
  'uint256 makerAccountNumber,' + \
  'uint256 expiration' + \
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
            hash_string('CanonicalOrders'),
            hash_string('1.1'),
            consts.NETWORK_ID,
            address_to_bytes32(consts.CANONICAL_ORDERS_ADDRESS)
        ]
    ).hex()


def get_order_hash(order):
    '''
    Returns the final signable EIP712 hash for an order.
    '''
    struct_hash = Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'uint256',
            'uint256',
            'uint256',
            'uint256',
            'uint256',
            'uint256',
            'bytes32',
            'uint256',
            'uint256'
        ],
        [
            hash_string(EIP712_ORDER_STRUCT_STRING),
            get_order_flags(order['salt'], order['isBuy']),
            int(order['baseMarket']),
            int(order['quoteMarket']),
            int(order['amount']),
            int(order['limitPrice'] * consts.BASE_DECIMAL),
            int(order['triggerPrice'] * consts.BASE_DECIMAL),
            int(order['limitFee'] * consts.BASE_DECIMAL),
            address_to_bytes32(order['makerAccountOwner']),
            int(order['makerAccountNumber']),
            int(order['expiration'])
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
    if market == consts.MARKET_WETH:
        decimals = consts.DECIMALS_WETH
    elif market == consts.MARKET_SAI:
        decimals = consts.DECIMALS_SAI
    elif market == consts.MARKET_USDC:
        decimals = consts.DECIMALS_USDC
    elif market == consts.MARKET_DAI:
        decimals = consts.DECIMALS_DAI
    else:
        raise ValueError('Invalid market number')
    return int(amount * (10 ** decimals))


def pair_to_base_quote_markets(pair):
    if pair == consts.PAIR_WETH_DAI:
        return (consts.MARKET_WETH, consts.MARKET_DAI)
    elif pair == consts.PAIR_WETH_USDC:
        return (consts.MARKET_WETH, consts.MARKET_USDC)
    elif pair == consts.PAIR_DAI_USDC:
        return (consts.MARKET_DAI, consts.MARKET_USDC)
    raise ValueError('Invalid pair')


def get_is_buy(side):
    if side == consts.SIDE_BUY:
        return True
    elif side == consts.SIDE_SELL:
        return False
    raise ValueError('Invalid side')


def get_order_flags(salt, isBuy):
    salt_string = strip_hex_prefix(hex(salt))[-63:]
    salt_string += '1' if isBuy else '0'
    return '0x' + salt_string.rjust(64, '0')


def get_limit_fee(base_market, amount, postOnly):
    if postOnly:
        return 0
    if base_market == consts.MARKET_WETH:
        if (amount < consts.SMALL_TRADE_SIZE_WETH):
            return consts.FEE_SMALL_WETH
        else:
            return consts.FEE_LARGE_WETH
    elif base_market == consts.MARKET_DAI:
        if (amount < consts.SMALL_TRADE_SIZE_DAI):
            return consts.FEE_SMALL_DAI
        else:
            return consts.FEE_LARGE_DAI
    raise ValueError('Invalid base_market')


def decimalToStr(d):
    return '{:f}'.format(d.normalize())
