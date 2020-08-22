from web3 import Web3
import dydx.constants as consts
import dydx.util as utils

EIP712_ORDER_STRUCT_STRING = \
  'Order(' + \
  'bytes32 flags,' + \
  'uint256 amount,' + \
  'uint256 limitPrice,' + \
  'uint256 triggerPrice,' + \
  'uint256 limitFee,' + \
  'address maker,' + \
  'address taker,' + \
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


def get_domain_hash(pair):
    contract_name = ''
    contract_address = ''
    if pair == consts.PAIR_PBTC_USDC:
        contract_name = 'P1Orders'
        contract_address = consts.BTC_P1_ORDERS_ADDRESS
    elif pair == consts.PAIR_PLINK_USDC:
        contract_name = 'P1Orders'
        contract_address = consts.LINK_P1_ORDERS_ADDRESS
    elif pair == consts.PAIR_WETH_PUSD:
        contract_name = 'P1InverseOrders'
        contract_address = consts.ETH_P1_ORDERS_ADDRESS
    else:
        raise ValueError('Invalid perpetual pair')

    return Web3.solidityKeccak(
        [
            'bytes32',
            'bytes32',
            'bytes32',
            'uint256',
            'bytes32'
        ],
        [
            utils.hash_string(EIP712_DOMAIN_STRING),
            utils.hash_string(contract_name),
            utils.hash_string('1.0'),
            consts.NETWORK_ID,
            utils.address_to_bytes32(contract_address)
        ]
    ).hex()


def get_order_hash(order, pair):
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
            'bytes32',
            'bytes32',
            'uint256'
        ],
        [
            utils.hash_string(EIP712_ORDER_STRUCT_STRING),
            get_order_flags(order['salt'], order['isBuy'], order['limitFee']),
            int(order['amount']),
            int(order['limitPrice'] * consts.BASE_DECIMAL),
            int(order['triggerPrice'] * consts.BASE_DECIMAL),
            int(abs(order['limitFee']) * consts.BASE_DECIMAL),
            utils.address_to_bytes32(order['maker']),
            utils.address_to_bytes32(order['taker']),
            int(order['expiration'])
        ]
    ).hex()
    return utils.get_eip712_hash(get_domain_hash(pair), struct_hash)


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
            utils.hash_string(EIP712_CANCEL_ORDER_STRUCT_STRING),
            action_hash,
            orders_hash,
        ]
    ).hex()
    return utils.get_eip712_hash(get_domain_hash(
        consts.PAIR_PBTC_USDC,  # Use BTC Market. Orderbook should accept it.
    ), struct_hash)


def sign_order(order, pair, private_key):
    order_hash = get_order_hash(order, pair)
    return utils.sign_hash(order_hash, private_key)


def sign_cancel_order(order_hash, private_key):
    cancel_order_hash = get_cancel_order_hash(order_hash)
    return utils.sign_hash(cancel_order_hash, private_key)


def get_order_flags(salt, isBuy, limitFee):
    salt_string = utils.strip_hex_prefix(hex(salt))[-63:]
    salt_int = 0
    salt_int += 1 if isBuy else 0
    salt_int += 4 if (limitFee < 0) else 0
    salt_string += str(salt_int)
    return '0x' + salt_string.rjust(64, '0')
