from __future__ import print_function

import logging
import time

import config

import ExchgData
# logging.basicConfig(level=logging.INFO)
import orders
from indicators import *
from notifications import send_email
from utilities import *

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
dh = logging.FileHandler('logs/full.log')
dh.setLevel(logging.DEBUG)
ih = logging.FileHandler('logs/tradebot.log')
ih.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
ffm = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
cfm = logging.Formatter('[%(asctime)s] %(message)s')
sh.setFormatter(cfm)
dh.setFormatter(ffm)
ih.setFormatter(ffm)

log.addHandler(sh)
log.addHandler(dh)
log.addHandler(ih)
log.info("Logger initialized")

tl = logging.getLogger('logs/trades')
tl.setLevel(logging.DEBUG)
tfh = logging.FileHandler('logs/trades.log')
tsh = logging.StreamHandler()
tfh.setLevel(logging.DEBUG)
tsh.setLevel(logging.INFO)
tff = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
tsf = logging.Formatter('[%(asctime)s] %(message)s')
tfh.setFormatter(tff)
tsh.setFormatter(tsf)
tl.addHandler(tfh)
tl.addHandler(tsh)
tl.info("Trade Logger Initialized")


def report_trade(action, ordersize, stacked, price):
    report_string = "action: %s\tordersize: %d\tstacked: %d\tprice: %.2f" % (action, ordersize, stacked, price)
    tl.info(report_string)
    log.debug(report_string)
    send_email(report_string)


def hist_positive(exchgdata, tf):
    #  for the div detection
    (t, o, h, l, c, v) = exchgdata.get_split_tohlcv(tf, 34)
    exchgdata.dprint_last_candles(tf, 5)
    (kvo, signal) = klinger_kama(h, l, c, v)
    hist = kvo[-1] - signal[-1]
    log.info("hist is %.2f" % hist)
    positive = True
    if hist <= 0:
        positive = False
    return positive


sleeptime = 30
send_email('\nBot Active!')
hist_tf = '15m'

binance_data = ExchgData.ExchgData('binance')

last_hist_positive = hist_positive(binance_data, hist_tf)
curr_hist_positive = last_hist_positive

while [1]:
    log.debug("Main loop")
    orders.update_bracket_pct(config.sl, config.tp)

    curr_hist_positive = hist_positive(binance_data, hist_tf)

    shorts = orders.get_position_size('short')
    longs = orders.get_position_size('long')
    log.info(f'shorts-->>{shorts}')
    log.info(f'longs-->>{longs}')
    last, vwap = orders.get_last_and_vwap();
    # buybelow   =  10000
    buybelow = vwap
    # sellabove  =  1000
    sellabove = vwap
    # if 1d kvo has flipped, flip positions
    if curr_hist_positive and not last_hist_positive:
        print('Inside if')
        if last < buybelow:
            if shorts > longs:
                entryprice = orders.get_positions()[0]['avgCostPrice']
                breakEvenPrice = orders.get_positions()[0]['breakEvenPrice']
                if breakEvenPrice - last > 15:
                    orders.cancel_open_orders()
                    time.sleep(1)
                    orders.smart_order('Buy', shorts + config.ordersize)
                    send_email("%s %s %s %s %s" % ( \
                        ("\nBuy signal!! KVO flipped positive and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        (".\nCurrently net short with Average entry: " + str(entryprice)), \
                        (" and Breakeven at " + str(breakEvenPrice)), \
                        ".\nClosing short in profit and Going Long"))
                    report_trade("Closing short and Going Long", shorts + config.ordersize, longs + config.ordersize,
                                 last)
                else:
                    send_email("%s %s %s %s %s" % ( \
                        ("\nBuy signal!! KVO flipped positive and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        (".\nUnderwater short with Average entry: " + str(entryprice)), \
                        (" and Breakeven at " + str(breakEvenPrice)), \
                        ".\nSo not going long yet."))
            else:
                orders.cancel_open_orders()
                time.sleep(1)
                orders.smart_order('Buy', shorts + config.ordersize)
                if longs == 0:
                    send_email("%s %s %s" % ( \
                        ("\nBuy signal!! KVO flipped positive and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        ".\nGoing Long"))
                    report_trade("GOING LONG", shorts + config.ordersize, longs + config.ordersize, last)
                else:
                    send_email("%s %s %s" % ( \
                        ("\nBuy signal!! KVO flipped positive and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        ".\nAdding to Long"))
                    report_trade("Adding to LONG", shorts + config.ordersize, longs + config.ordersize, last)

        else:
            send_email("%s %s %s" % ( \
                ("\nKVO flipped positive and price is: " + str(last)), \
                (". But VWAP is: " + str(vwap)), \
                ".\nSo not going Long"))

    elif not curr_hist_positive and last_hist_positive:
        print('Inside else')
        if last > sellabove:
            if longs > shorts:
                entryprice = orders.get_positions()[0]['avgCostPrice']
                breakEvenPrice = orders.get_positions()[0]['breakEvenPrice']
                if last - breakEvenPrice > 15:
                    orders.cancel_open_orders()
                    time.sleep(1)
                    orders.smart_order('Sell', longs + config.ordersize)
                    send_email("%s %s %s %s %s" % ( \
                        ("\nSell signal!! KVO flipped negative and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        (".\nCurrently net long with Average entry: " + str(entryprice)), \
                        (" and Breakeven at " + str(breakEvenPrice)), \
                        (".\nClosing long in profit and Going short")))
                    report_trade("Closing long and Going short", longs + config.ordersize, shorts + config.ordersize,
                                 last)
                else:
                    send_email("%s %s %s %s %s" % ( \
                        ("Sell signal!! KVO flipped negative and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        (".\nUnderwater long with Average entry: " + str(entryprice)), \
                        (" and Breakeven at " + str(breakEvenPrice)), \
                        ".\nSo not going short yet."))
            else:
                orders.cancel_open_orders()
                time.sleep(1)
                orders.smart_order('Buy', longs + config.ordersize)
                if longs == 0:
                    send_email("%s %s %s" % ( \
                        ("\nSell signal!! KVO flipped negative and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        (".\Going short")))
                    report_trade("GOING short", longs + config.ordersize, shorts + config.ordersize, last)
                else:
                    send_email("%s %s %s" % ( \
                        ("\nSell signal!! KVO flipped negative and price is: " + str(last)), \
                        (". VWAP is: " + str(vwap)), \
                        ".\nAdding to short"))
                    report_trade("Adding to short", longs + config.ordersize, shorts + config.ordersize, last)


        else:
            send_email("%s %s %s" % ( \
                ("\nKVO flipped negative and price is: " + str(last)), \
                (". But VWAP is: " + str(vwap)), \
                ".\nSo not going short"))

    last_hist_positive = curr_hist_positive

    # now print some status info
    orders.print_positions()
    orders.print_open_orders()
    balanceInfo = orders.get_balance()
    totalbal_btc, freebal_btc, totalbal_usd, freebal_usd = 0.0, 0.0, 0.0, 0.0
    if balanceInfo is not None and "BTC" in balanceInfo['total'].keys():
        totalbal_btc = balanceInfo["total"]["BTC"]
    if balanceInfo is not None and "BTC" in balanceInfo['free'].keys():
        freebal_btc = balanceInfo["free"]["BTC"]
    if balanceInfo is not None and "USDT" in balanceInfo['total'].keys():
        totalbal_usd = balanceInfo["total"]["USDT"]
    if balanceInfo is not None and "USDT" in balanceInfo['free'].keys():
        freebal_usd = balanceInfo["free"]["USDT"]
    log.info(" Last price is: %.4f, VWAP is %.4f" % (last, vwap))
    log.info("Total Balance BTC: %.10f, Free Balance BTC: %.10f" % (totalbal_btc, freebal_btc))
    log.info("Total Balance USDT: %.10f, Free Balance USDT: %.10f" % (totalbal_usd, freebal_usd))
    log.info("Loop completed, sleeping for %d seconds" % sleeptime)
    time.sleep(sleeptime)
