# flake8: noqa

mock_get_pairs_json = {
    'pairs': [
        {
            'uuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
            'name': 'WETH-DAI',
            'createdAt': '2019-07-26T17:19:34.955Z',
            'updatedAt': '2019-07-26T17:19:34.955Z',
            'deletedAt': None,
            'makerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
            'takerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
            'makerCurrency': {
                'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                'symbol': 'WETH',
                'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                'decimals': 18,
                'soloMarket': 0,
                'createdAt': '2019-07-26T17:19:34.627Z',
                'updatedAt': '2019-07-26T17:19:34.627Z',
                'deletedAt': None
            },
            'takerCurrency': {
                'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                'symbol': 'DAI',
                'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                'decimals': 18,
                'soloMarket': 1,
                'createdAt': '2019-07-26T17:19:34.919Z',
                'updatedAt': '2019-07-26T17:19:34.919Z',
                'deletedAt': None
            }
        }
    ]
}

mock_cancel_order_json = {
    'orders': [
        {
            'uuid': 'd13aadc8-49fb-4420-a5a0-03c15b668705',
            'id': '0x2c45cdcd3bce2dd0f2b40502e6bea7975f6daa642d12d28620deb18736619fa2',
            'makerAccountOwner': '0x0913017c740260fea4b2c62828a4008ca8b0d6e4',
            'makerAccountNumber': '0',
            'status': 'PENDING',
            'price': '1',
            'fillOrKill': False,
            'cancelAmountOnRevert': False,
            'postOnly': False,
            'rawData': '{\"makerMarket\":\"0\",\"takerMarket\":\"1\",\"makerAccountNumber\":\"0\",\"takerAccountNumber\":\"222\",\"makerAccountOwner\":\"0x0913017c740260fea4b2c62828a4008ca8b0d6e4\",\"takerAccountOwner\":\"0x28a8746e75304c0780e011bed21c72cd78cd535e\",\"makerAmount\":\"10\",\"takerAmount\":\"10\",\"salt\":\"79776019296374116968729143546164248655125424402698335194396863096742023853053\",\"expiration\":\"0\",\"typedSignature\":\"0x9db8cc7ee2e06525949a0ae87301d890aee9973c464b276661d760ca8db4c73522ba48b94bf36d4aada7627656f79be9e40225a52f0adec079b07263b9e8ee0c1b01\"}',
            'makerAmount': '10',
            'unfillableAt': None,
            'unfillableReason': None,
            'takerAmount': '10',
            'makerAmountRemaining': '10',
            'takerAmountRemaining': '10',
            'createdAt': '2019-07-29T23:56:25.522Z',
            'updatedAt': '2019-07-29T23:56:25.522Z',
            'deletedAt': None,
            'pairUuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
            'pair': {
                'uuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
                'name': 'WETH-DAI',
                'createdAt': '2019-07-26T17:19:34.955Z',
                'updatedAt': '2019-07-26T17:19:34.955Z',
                'deletedAt': None,
                'makerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                'takerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                'makerCurrency': {
                    'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                    'symbol': 'WETH',
                    'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                    'decimals': 18,
                    'soloMarket': 0,
                    'createdAt': '2019-07-26T17:19:34.627Z',
                    'updatedAt': '2019-07-26T17:19:34.627Z',
                    'deletedAt': None
                },
                'takerCurrency': {
                    'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                    'symbol': 'DAI',
                    'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                    'decimals': 18,
                    'soloMarket': 1,
                    'createdAt': '2019-07-26T17:19:34.919Z',
                    'updatedAt': '2019-07-26T17:19:34.919Z',
                    'deletedAt': None
                }
            },
            'fills': []
        }
    ]
}

mock_get_order_json = {
    'order': {
        'uuid': 'd13aadc8-49fb-4420-a5a0-03c15b668705',
        'id': '0x2c45cdcd3bce2dd0f2b40502e6bea7975f6daa642d12d28620deb18736619fa2',
        'makerAccountOwner': '0x0913017c740260fea4b2c62828a4008ca8b0d6e4',
        'makerAccountNumber': '0',
        'status': 'PENDING',
        'price': '1',
        'fillOrKill': False,
        'cancelAmountOnRevert': False,
        'postOnly': False,
        'rawData': '{\"makerMarket\":\"0\",\"takerMarket\":\"1\",\"makerAccountNumber\":\"0\",\"takerAccountNumber\":\"222\",\"makerAccountOwner\":\"0x0913017c740260fea4b2c62828a4008ca8b0d6e4\",\"takerAccountOwner\":\"0x28a8746e75304c0780e011bed21c72cd78cd535e\",\"makerAmount\":\"10\",\"takerAmount\":\"10\",\"salt\":\"79776019296374116968729143546164248655125424402698335194396863096742023853053\",\"expiration\":\"0\",\"typedSignature\":\"0x9db8cc7ee2e06525949a0ae87301d890aee9973c464b276661d760ca8db4c73522ba48b94bf36d4aada7627656f79be9e40225a52f0adec079b07263b9e8ee0c1b01\"}',
        'makerAmount': '10',
        'unfillableAt': None,
        'unfillableReason': None,
        'takerAmount': '10',
        'makerAmountRemaining': '10',
        'takerAmountRemaining': '10',
        'createdAt': '2019-07-29T23:56:25.522Z',
        'updatedAt': '2019-07-29T23:56:25.522Z',
        'deletedAt': None,
        'pairUuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
        'pair': {
            'uuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
            'name': 'WETH-DAI',
            'createdAt': '2019-07-26T17:19:34.955Z',
            'updatedAt': '2019-07-26T17:19:34.955Z',
            'deletedAt': None,
            'makerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
            'takerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
            'makerCurrency': {
                'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                'symbol': 'WETH',
                'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                'decimals': 18,
                'soloMarket': 0,
                'createdAt': '2019-07-26T17:19:34.627Z',
                'updatedAt': '2019-07-26T17:19:34.627Z',
                'deletedAt': None
            },
            'takerCurrency': {
                'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                'symbol': 'DAI',
                'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                'decimals': 18,
                'soloMarket': 1,
                'createdAt': '2019-07-26T17:19:34.919Z',
                'updatedAt': '2019-07-26T17:19:34.919Z',
                'deletedAt': None
            }
        },
        'fills': []
    }
}

mock_get_orders_json = {
    'orders': [
        {
            'uuid': 'd13aadc8-49fb-4420-a5a0-03c15b668705',
            'id': '0x2c45cdcd3bce2dd0f2b40502e6bea7975f6daa642d12d28620deb18736619fa2',
            'makerAccountOwner': '0x0913017c740260fea4b2c62828a4008ca8b0d6e4',
            'makerAccountNumber': '0',
            'status': 'PENDING',
            'price': '1',
            'fillOrKill': False,
            'cancelAmountOnRevert': False,
            'postOnly': False,
            'rawData': '{\"makerMarket\":\"0\",\"takerMarket\":\"1\",\"makerAccountNumber\":\"0\",\"takerAccountNumber\":\"222\",\"makerAccountOwner\":\"0x0913017c740260fea4b2c62828a4008ca8b0d6e4\",\"takerAccountOwner\":\"0x28a8746e75304c0780e011bed21c72cd78cd535e\",\"makerAmount\":\"10\",\"takerAmount\":\"10\",\"salt\":\"79776019296374116968729143546164248655125424402698335194396863096742023853053\",\"expiration\":\"0\",\"typedSignature\":\"0x9db8cc7ee2e06525949a0ae87301d890aee9973c464b276661d760ca8db4c73522ba48b94bf36d4aada7627656f79be9e40225a52f0adec079b07263b9e8ee0c1b01\"}',
            'makerAmount': '10',
            'unfillableAt': None,
            'unfillableReason': None,
            'takerAmount': '10',
            'makerAmountRemaining': '10',
            'takerAmountRemaining': '10',
            'createdAt': '2019-07-29T23:56:25.522Z',
            'updatedAt': '2019-07-29T23:56:25.522Z',
            'deletedAt': None,
            'pairUuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
            'pair': {
                'uuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
                'name': 'WETH-DAI',
                'createdAt': '2019-07-26T17:19:34.955Z',
                'updatedAt': '2019-07-26T17:19:34.955Z',
                'deletedAt': None,
                'makerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                'takerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                'makerCurrency': {
                    'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                    'symbol': 'WETH',
                    'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                    'decimals': 18,
                    'soloMarket': 0,
                    'createdAt': '2019-07-26T17:19:34.627Z',
                    'updatedAt': '2019-07-26T17:19:34.627Z',
                    'deletedAt': None
                },
                'takerCurrency': {
                    'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                    'symbol': 'DAI',
                    'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                    'decimals': 18,
                    'soloMarket': 1,
                    'createdAt': '2019-07-26T17:19:34.919Z',
                    'updatedAt': '2019-07-26T17:19:34.919Z',
                    'deletedAt': None
                }
            },
            'fills': []
        }
    ]
}

mock_get_market_json = {
    'market': {
        'WETH-DAI': {
            'name': 'WETH-DAI',
            'baseCurrency': {
                'currency': 'WETH',
                'decimals': 18,
                'soloMarketId': 0,
            },
            'quoteCurrency': {
                'currency': 'DAI',
                'decimals': 18,
                'soloMarketId': 3,
            },
            'minimumTickSize': '0.01',
            'minimumOrderSize': '100000000000000000',
            'smallOrderThreshold': '500000000000000000',
            'makerFee': '0',
            'largeTakerFee': '0.005',
            'smallTakerFee': '0.0015',
        },
    }
}

mock_get_markets_json = {
    'markets': {
        'WETH-DAI': {
            'name': 'WETH-DAI',
            'baseCurrency': {
                'currency': 'WETH',
                'decimals': 18,
                'soloMarketId': 0,
            },
            'quoteCurrency': {
                'currency': 'DAI',
                'decimals': 18,
                'soloMarketId': 3,
            },
            'minimumTickSize': '0.01',
            'minimumOrderSize': '100000000000000000',
            'smallOrderThreshold': '500000000000000000',
            'makerFee': '0',
            'largeTakerFee': '0.005',
            'smallTakerFee': '0.0015',
        },
        'WETH-USDC': {
            'name': 'WETH-USDC',
            'baseCurrency': {
                'currency': 'WETH',
                'decimals': 18,
                'soloMarketId': 0,
            },
            'quoteCurrency': {
                'currency': 'USDC',
                'decimals': 6,
                'soloMarketId': 2,
            },
            'minimumTickSize': '0.00000000000001',
            'minimumOrderSize': '100000000000000000',
            'smallOrderThreshold': '500000000000000000',
            'makerFee': '0',
            'largeTakerFee': '0.005',
            'smallTakerFee': '0.0015',
        },
        'DAI-USDC': {
            'name': 'DAI-USDC',
            'baseCurrency': {
                'currency': 'DAI',
                'decimals': 18,
                'soloMarketId': 3,
            },
            'quoteCurrency': {
                'currency': 'USDC',
                'decimals': 6,
                'soloMarketId': 1,
            },
            'minimumTickSize': '0.0000000000000001',
            'minimumOrderSize': '20000000000000000000',
            'smallOrderThreshold': '100000000000000000000',
            'makerFee': '0',
            'largeTakerFee': '0.005',
            'smallTakerFee': '0.0005',
        },
    }
}

mock_get_fills_json = {
    'fills': [
        {
            'uuid': 'c389c0de-a193-49c3-843a-eebee25d1bfa',
            'messageId': '8f1ed6dc-8bd6-4155-ab33-5a252814f88b',
            'status': 'PENDING',
            'orderId': '0x66a5b2d4bca3414ed902bd7cda0500df5947fadbfd48c280a206d44606c1c906',
            'transactionHash': '0x811cf67aca5fb8d085efcc47cd8213e767410866c7c840f2177391bf6e6b2fd0',
            'fillAmount': '10',
            'createdAt': '2019-07-27T00:48:15.963Z',
            'updatedAt': '2019-07-27T00:48:15.963Z',
            'deletedAt': None,
            'order': {
                'uuid': 'b415de0d-a54c-4496-a8af-0a15d9fb95d5',
                'id': '0x66a5b2d4bca3414ed902bd7cda0500df5947fadbfd48c280a206d44606c1c906',
                'makerAccountOwner': '0x0913017c740260fea4b2c62828a4008ca8b0d6e4',
                'makerAccountNumber': '0',
                'status': 'FILLED',
                'price': '1',
                'fillOrKill': False,
                'cancelAmountOnRevert': False,
                'postOnly': False,
                'rawData': '{\"makerAccountOwner\":\"0x0913017c740260fea4b2c62828a4008ca8b0d6e4\",\"takerAccountOwner\":\"0x28a8746e75304c0780e011bed21c72cd78cd535e\",\"makerAccountNumber\":\"0\",\"takerAccountNumber\":\"222\",\"makerMarket\":\"0\",\"takerMarket\":\"1\",\"makerAmount\":\"10\",\"takerAmount\":\"10\",\"salt\":\"0\",\"expiration\":\"0\",\"typedSignature\":\"0xd9561c880b9572899eb97901f58423a610640357c1d36138f0bd31b16ca17edb715ec175b7cd7a308d70e88a6654ac706672419765720b6d8e357e60a9a5ce9b1c01\"}',
                'makerAmount': '10',
                'unfillableAt': '2019-07-27T00:48:16.000Z',
                'unfillableReason': 'ENTIRELY_FILLED',
                'takerAmount': '10',
                'makerAmountRemaining': '0',
                'takerAmountRemaining': '0',
                'createdAt': '2019-07-26T17:20:36.999Z',
                'updatedAt': '2019-07-27T00:48:16.001Z',
                'deletedAt': None,
                'pairUuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
                'pair': {
                    'uuid': 'b9b38876-c3a6-470e-81cf-d352d26685d0',
                    'name': 'WETH-DAI',
                    'createdAt': '2019-07-26T17:19:34.955Z',
                    'updatedAt': '2019-07-26T17:19:34.955Z',
                    'deletedAt': None,
                    'makerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                    'takerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                    'makerCurrency': {
                        'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                        'symbol': 'WETH',
                        'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                        'decimals': 18,
                        'soloMarket': 0,
                        'createdAt': '2019-07-26T17:19:34.627Z',
                        'updatedAt': '2019-07-26T17:19:34.627Z',
                        'deletedAt': None
                    },
                    'takerCurrency': {
                        'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                        'symbol': 'DAI',
                        'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                        'decimals': 18,
                        'soloMarket': 1,
                        'createdAt': '2019-07-26T17:19:34.919Z',
                        'updatedAt': '2019-07-26T17:19:34.919Z',
                        'deletedAt': None
                    }
                }
            }
        },
    ]
}

mock_get_trades_json = {
    'trades': [
        {
            'uuid': '9c575414-503f-4d19-97ba-7e329ce7c1f0',
            'transactionSender': '0xf809e07870dca762b9536d61a4fbef1a17178092',
            'transactionNonce': '2036',
            'transactionHash': '0x6376e4af2c2429a1f9fdb0bd46d022c074713c58007f4c36825ed2228cbf6ce2',
            'status': 'CONFIRMED',
            'price': '200',
            'makerAmount': '100',
            'takerAmount': '201500',
            'makerOrderId': '0xb5576698cd7ecca927bba833c60e66ae55585c3f9a722cef5fe6fd5cf80eee2a',
            'takerOrderId': '0x20cab002ade434d4e21cc7ff6144339c4b4f199bd1d35ec93813b19c7a03162b',
            'createdAt': '2019-08-27T21:34:12.619Z',
            'updatedAt': '2019-08-27T21:35:14.054Z',
            'takerOrder': {
                'uuid': '3ed110f1-a98b-462f-9a41-a04e6e0da94c',
                'id': '0x20cab002ade434d4e21cc7ff6144339c4b4f199bd1d35ec93813b19c7a03162b',
                'makerAccountOwner': '0x5f5a46a8471f60b1e9f2ed0b8fc21ba8b48887d8',
                'makerAccountNumber': '0',
                'status': 'PARTIALLY_FILLED',
                'price': '0.004962779156327543424317617866004962779156327543424317617866004962779156327543',
                'fillOrKill': False,
                'cancelAmountOnRevert': False,
                'postOnly': False,
                'rawData': '{\"makerMarket\":\"1\",\"takerMarket\":\"0\",\"makerAccountNumber\":\"0\",\"takerAccountNumber\":\"0\",\"makerAccountOwner\":\"0x5F5A46a8471F60b1E9F2eD0b8fc21Ba8b48887D8\",\"takerAccountOwner\":\"0xf809e07870dca762B9536d61A4fBEF1a17178092\",\"makerAmount\":\"2015000000000000000\",\"takerAmount\":\"10000000000000000\",\"salt\":\"98520959837884420232461297527105290253597439542504267862519345092558369505856\",\"expiration\":\"1569360848\",\"typedSignature\":\"0xf26210e77f8ed100c88ba7ab8c3a3132506805c0b7e14a2ba0fb7ea2b8edd659705525b2e98460e3c23ebda83975b668aab287d4c588196eb7e607bba87545a61b00\"}',
                'makerAmount': '2015000000000000000',
                'unfillableAt': None,
                'expiresAt': '2019-09-24T21:34:08.000Z',
                'unfillableReason': None,
                'clientId': None,
                'takerAmount': '10000000000000000',
                'makerAmountRemaining': '2014999999999798500',
                'orderType': 'dydexLimitV1',
                'takerAmountRemaining': '9999999999999000',
                'createdAt': '2019-08-27T21:34:10.906Z',
                'updatedAt': '2019-08-27T21:34:12.648Z',
                'deletedAt': None,
                'pairUuid': '83b69358-a05e-4048-bc11-204da54a8b19',
                'pair': {
                    'uuid': '83b69358-a05e-4048-bc11-204da54a8b19',
                    'name': 'DAI-WETH',
                    'createdAt': '2018-08-24T16:26:46.963Z',
                    'updatedAt': '2018-08-24T16:26:46.963Z',
                    'deletedAt': None,
                    'makerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                    'takerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                    'makerCurrency': {
                        'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                        'symbol': 'DAI',
                        'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                        'decimals': 18,
                        'soloMarket': 1,
                        'createdAt': '2018-08-24T16:26:46.904Z',
                        'updatedAt': '2018-08-24T16:26:46.904Z',
                        'deletedAt': None
                    },
                    'takerCurrency': {
                        'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                        'symbol': 'WETH',
                        'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                        'decimals': 18,
                        'soloMarket': 0,
                        'createdAt': '2018-08-24T16:26:46.683Z',
                        'updatedAt': '2018-08-24T16:26:46.683Z',
                        'deletedAt': None
                    }
                }
            },
            'makerOrder': {
                'uuid': 'cd764c34-5198-48d7-a167-8ef120c93a4b',
                'id': '0xb5576698cd7ecca927bba833c60e66ae55585c3f9a722cef5fe6fd5cf80eee2a',
                'makerAccountOwner': '0xa33d2b7ad08cb84784a4db70fe7429eb603774e2',
                'makerAccountNumber': '0',
                'status': 'FILLED',
                'price': '200',
                'fillOrKill': False,
                'cancelAmountOnRevert': False,
                'postOnly': False,
                'rawData': '{\"makerMarket\":\"0\",\"takerMarket\":\"1\",\"makerAccountNumber\":\"0\",\"takerAccountNumber\":\"0\",\"makerAccountOwner\":\"0xa33d2b7ad08cb84784a4db70fe7429eb603774e2\",\"takerAccountOwner\":\"0xf809e07870dca762b9536d61a4fbef1a17178092\",\"makerAmount\":\"100\",\"takerAmount\":\"20000\",\"salt\":\"71396665083958089451142428285242792093549457850088753846410228331338822485995\",\"expiration\":\"0\",\"typedSignature\":\"0xfa843b61052d5ac28b7c47acdd0bcf568113eadead435f9f34b474a4fbeab8cd4c88ca7823ac0162c1081d081a50bcfe523dba2dff3b26f98d38c81aa9aad6e21c01\"}',
                'makerAmount': '100',
                'unfillableAt': '2019-08-27T21:34:12.640Z',
                'expiresAt': None,
                'unfillableReason': 'ENTIRELY_FILLED',
                'clientId': None,
                'takerAmount': '20000',
                'makerAmountRemaining': '0',
                'orderType': 'dydexLimitV1',
                'takerAmountRemaining': '0',
                'createdAt': '2019-08-12T21:10:12.936Z',
                'updatedAt': '2019-08-27T21:34:12.640Z',
                'deletedAt': None,
                'pairUuid': '5a40f128-ced5-4947-ab10-2f5afee8e56b',
                'pair': {
                    'uuid': '5a40f128-ced5-4947-ab10-2f5afee8e56b',
                    'name': 'WETH-DAI',
                    'createdAt': '2018-08-24T16:26:46.963Z',
                    'updatedAt': '2018-08-24T16:26:46.963Z',
                    'deletedAt': None,
                    'makerCurrencyUuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                    'takerCurrencyUuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                    'makerCurrency': {
                        'uuid': '84298577-6a82-4057-8523-27b05d3f5b8c',
                        'symbol': 'WETH',
                        'contractAddress': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                        'decimals': 18,
                        'soloMarket': 0,
                        'createdAt': '2018-08-24T16:26:46.683Z',
                        'updatedAt': '2018-08-24T16:26:46.683Z',
                        'deletedAt': None
                    },
                    'takerCurrency': {
                        'uuid': 'b656c441-68ab-4776-927c-d894f4d6483b',
                        'symbol': 'DAI',
                        'contractAddress': '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
                        'decimals': 18,
                        'soloMarket': 1,
                        'createdAt': '2018-08-24T16:26:46.904Z',
                        'updatedAt': '2018-08-24T16:26:46.904Z',
                        'deletedAt': None
                    }
                }
            }
        }
    ]
}

mock_get_balances_json = {
  'owner': '0x0913017c740260fea4b2c62828a4008ca8b0d6e4',
  'number': '0',
  'uuid': '72cd6a2a-17ff-4394-92d3-e951a96aa266',
  'hasAtLeastOneNegativePar': False,
  'hasAtLeastOnePositivePar': True,
  'sumBorrowUsdValue': '0',
  'sumSupplyUsdValue': '0',
  'balances': {
    '0': {
      'owner': '0x0913017c740260fea4b2c62828a4008ca8b0d6e4',
      'number': '0',
      'marketId': 0,
      'newPar': '9994719126810778',
      'accountUuid': '72cd6a2a-17ff-4394-92d3-e951a96aa266',
      'isParPositive': True,
      'isParNegative': False,
      'wei': '10000184397123234.892111593021043502',
      'expiresAt': None,
      'par': '9994719126810778',
      'adjustedSupplyUsdValue': '0',
      'adjustedBorrowUsdValue': '0'
    },
    '1': {
      'par': 0,
      'wei': 0,
      'expiresAt': None
    },
    '2': {
      'par': 0,
      'wei': 0,
      'expiresAt': None
    }
  }
}

mock_place_order_json = mock_cancel_order_json
