from web3 import Web3
import eth_keys
import eth_account
import time
import dydx.constants as consts


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


def remove_nones(original):
    return {k: v for k, v in original.items() if v is not None}


def dict_to_query_params(param_dict):
    values_dict = remove_nones(param_dict)
    if not values_dict:
        return ''
    return '?' + '&'.join(
        [key + '=' + str(value) for key, value in values_dict.items()],
    )


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
    elif market == consts.MARKET_PBTC:
        decimals = consts.DECIMALS_PBTC
    else:
        raise ValueError('Invalid market')
    return int(amount * (10 ** decimals))


def btc_to_sats(amount):
    return amount * (10 ** consts.DECIMALS_PBTC)


def pair_to_base_quote_markets(pair):
    if pair == consts.PAIR_WETH_DAI:
        return (consts.MARKET_WETH, consts.MARKET_DAI)
    elif pair == consts.PAIR_WETH_USDC:
        return (consts.MARKET_WETH, consts.MARKET_USDC)
    elif pair == consts.PAIR_DAI_USDC:
        return (consts.MARKET_DAI, consts.MARKET_USDC)
    elif pair == consts.PAIR_PBTC_USDC:
        return (consts.MARKET_PBTC, consts.MARKET_USDC)
    elif pair == consts.PAIR_WETH_PUSD:
        return (consts.MARKET_PUSD, consts.MARKET_WETH)
    raise ValueError('Invalid pair')


def get_is_buy(side):
    if side == consts.SIDE_BUY:
        return True
    elif side == consts.SIDE_SELL:
        return False
    raise ValueError('Invalid side')


def get_limit_fee(base_market, amount):
    return consts.LIMIT_FEE


def decimalToStr(d):
    return '{:f}'.format(d.normalize())


def sign_hash(hash, private_key):
    result = eth_account.account.Account.sign_message(
        eth_account.messages.encode_defunct(hexstr=hash),
        private_key
    )
    return result['signature'].hex() + '01'
