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
        # date_before = int((dt.datetime.now() - dt.timedelta(days = 5)).timestamp())
        # # print(date_before)
        # klines=(self.client.LinearKline.LinearKline_get(symbol="ETHUSDT", interval="60", **{'from':date_before}).result()[0]['result'])
        # close = []
        # for i in klines:
        #     close.append(float(i['close']))

        # print(close)
        # print(klines[0]['result'][-4])
        # position = (self.client.LinearPositions.LinearPositions_myPosition(symbol="ETHUSDT").result()[0]['result'][0]['size'])
        # print(position)
        # leverage = self.client.LinearPositions.LinearPositions_saveLeverage(symbol="ETHUSDT", buy_leverage=50, sell_leverage=50).result()
        # balance = self.client.Wallet.Wallet_getBalance(coin="USDT").result()[0]['result']['USDT']['equity']
        # print(self.client.LinearMarket.LinearMarket_trading(symbol="ETHUSDT").result()[0]['result'][0]['price'])

        # entry_price = self.client.LinearPositions.LinearPositions_myPosition(symbol="ETHUSDT").result()[0]['result'][0]['entry_price'])
        # self.last_price = self.client.LinearMarket.LinearMarket_trading(
        #             symbol="ETHUSDT").result()[0]['result'][0]['price']


        # sell_entry_price = self.client.LinearPositions.LinearPositions_myPosition(
        #             symbol="ETHUSDT").result()[0]['result'][1]['entry_price']


        # print(self.last_price)
        # print(last_order_price)
        date_before = int((dt.datetime.now() - dt.timedelta(days = 60)).timestamp())
        klines=(self.client.LinearKline.LinearKline_get(symbol="ETHUSDT", interval="D", **{'from':date_before}).result()[0]['result'])
        close = []
        for i in klines:
            close.append(float(i['close']))

        close_arr = numpy.asarray(close)
        close_rsi = talib.RSI(close_arr, 14)
        max_rsi = talib.MAX(close_rsi, 14)
        min_rsi = talib.MIN(close_rsi, 14)
        stochrsi = (close_rsi - min_rsi)/(max_rsi - min_rsi)
        k = talib.SMA(stochrsi, 3)*100
        d = talib.SMA(k, 3)
        quantity = 0.2 
        if k[-1]<d[-1]:
            buy_quantity = quantity*0.7
            sell_quantity = quantity
        elif k[-1]>d[-1]:
            sell_quantity = quantity*0.7
            buy_quantity = quantity
        else:
            sell_quantity = quantity
            buy_quantity = quantity

        # print(close)
        print("k",k)
        print("d",d)
        print(close)
Kai()
