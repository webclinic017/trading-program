from binance.client import Client
from config import Connect
from order import Order
import datetime as dt
import numpy
import talib
import time
import pandas as pd

class Kai:
    def __init__(self) -> None:
        self.client = Connect().make_connection()
        # try:
        #     # Change date and/or interval for different time frame
        #     klines = self.client.futures_historical_klines(
        #         "BTCUSDT", self.client.KLINE_INTERVAL_5MINUTE, start_str=str(dt.datetime.now()-dt.timedelta(days=1)), end_str=str(dt.datetime.now()))
        # except:
        #     print('Timeout! Waiting for time binance to respond...')
        #     time.sleep(120)
        #     print('Trying to connect again...')
        #     klines = self.client.futures_historical_klines(
        #         "BTCUSDT", self.client.KLINE_INTERVAL_5MINUTE, start_str=str(dt.datetime.now()-dt.timedelta(days=1)), end_str=str(dt.datetime.now()))

        # df = pd.DataFrame(klines)
        # df.to_csv('on92.csv')

        # for i in range(-1,-10,-1):
        #     print(i)
        #     last_order_status = self.client.futures_get_all_orders(symbol = 'BTCUSDT')[i]['status']
        #     print(last_order_status)
        #     if last_order_status != 'FILLED':
        #         continue
        #     else:
        #         last_order_price = self.client.futures_get_all_orders(symbol = 'BTCUSDT')[i]['avgPrice']
        #         break
        # print (last_order_status+last_order_price)
        # position = self.client.futures_position_information(symbol='BTCUSDT')[-1]['positionAmt']
        # print (position)

    #     balance = float(self.client.futures_account_balance()[1]['balance'])
    #     print(balance)
    #     eth_last_price = float(self.client.futures_recent_trades(
    #                 symbol='ETHUSDT')[-1]['price'])
    #     print(eth_last_price)
    #     self.quantity = round(float(balance*50/eth_last_price*0.35),2)
    #     self.hi()

    # def hi(self):
    #         quantity = self.quantity
        orders = self.client.futures_get_all_orders(symbol='ETHUSDT')
        for order in orders:
            quantity = order['executedQty']
            cost = order['avgPrice'] 
            print()

Kai()

