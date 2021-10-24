from functools import reduce
from config import Connect
import datetime as dt
import talib
import numpy


class Order:
    def __init__(self):
        self.client = Connect().make_connection()
        # leverage = self.client.LinearPositions.LinearPositions_saveLeverage(symbol="ETHUSDT", buy_leverage=50, sell_leverage=50).result()
        balance = self.client.Wallet.Wallet_getBalance(coin="USDT").result()[0]['result']['USDT']['equity']
        eth_last_price = float(self.client.LinearMarket.LinearMarket_trading(symbol="ETHUSDT").result()[0]['result'][0]['price'])
        
        ##### Extract Klines data 
        date_before = int((dt.datetime.now() - dt.timedelta(days = 40)).timestamp())
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
        quantity = 0.07
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
        print ("buy quantity",buy_quantity)
        print("sell quantity",sell_quantity)
        
        self.sell_quan = round(float(balance*50/eth_last_price*sell_quantity),2)
        self.buy_quan = round(float(balance*50/eth_last_price*buy_quantity),2)

        print(self.sell_quan)
        print(self.buy_quan)

    def sell(self):

        order = self.client.LinearOrder.LinearOrder_new(
            side="Sell",
            symbol="ETHUSDT",
            order_type="Market",
            qty=self.sell_quan,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False).result()
        
        return(order)


    def buy(self):

        order = self.client.LinearOrder.LinearOrder_new(
            side="Buy",
            symbol="ETHUSDT",
            order_type="Market",
            qty=self.buy_quan,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False).result()
        
        return(order)
        
    def close_order(self, qty, side):

        if side == "BUY":
            order = self.client.LinearOrder.LinearOrder_new(
            side="Sell",
            symbol="ETHUSDT",
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel",
            reduce_only=True,
            close_on_trigger=False
            ).result()
        elif side == "SELL":
            order = self.client.LinearOrder.LinearOrder_new(
            side="Buy",
            symbol="ETHUSDT",
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel",
            reduce_only=True,
            close_on_trigger=False
            ).result()