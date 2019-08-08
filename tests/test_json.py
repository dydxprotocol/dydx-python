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

mock_create_order_json = mock_cancel_order_json
