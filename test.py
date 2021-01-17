import ccxt
import config
#
# print(config.binance_auth)
# exchange = ccxt.binance({
#     'apiKey': config.binance_auth['apiKey'],
#     'secret': config.binance_auth['secret'],
#     'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
#     'options': {
#         'defaultType': 'future',
#     }
# })
#
# exchange.load_markets()
#
# symbol = u'BTC/USDT'
# market = exchange.market(symbol)
# leverage = 40
#
# response = exchange.fapiPrivate_post_leverage({
#     'symbol': market['id'],
#     'leverage': leverage,
# })
#
# print(response)

import asyncio
import os
import sys
from pprint import pprint

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402


async def main(asyncio_loop):
    exchange = ccxt.binance({
        'asyncio_loop': asyncio_loop,
        'enableRateLimit': True,
        'apiKey': config.binance_auth['apiKey'],
        'secret': config.binance_auth['secret'],
        # 'verbose': True,  # for debug output
    })
    try:
        # change the values here
        symbol = 'BTC/USDT'
        price = 9000
        amount = 10
        type = 'market'  # or market
        side = 'buy'
        order = await exchange.create_order(symbol, type, side, amount,
                                            params={'quoteOrderQty': config.ordersize, 'type': 'margin',
        })
        pprint(order)
    except ccxt.InsufficientFunds as e:
        print('create_order() failed – not enough funds')
        print(e)
    except Exception as e:
        print('create_order() failed')
        print(e)
    await exchange.close()

if __name__ == '__main__':
    asyncio_loop = asyncio.get_event_loop()
    asyncio_loop.run_until_complete(main(asyncio_loop))
