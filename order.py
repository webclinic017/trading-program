from config import Connect
import datetime as dt
import talib
import numpy


class Order:
    def __init__(self):
        self.client = Connect().make_connection()
        self.client.futures_change_leverage(symbol='ETHUSDT', leverage=50)
        balance = float(self.client.futures_account_balance()[1]['balance'])
        eth_last_price = float(self.client.futures_recent_trades(
                    symbol='ETHUSDT')[-1]['price'])
        klines = self.client._historical_klines(
                    self.trade_symbol, self.client.KLINE_INTERVAL_1DAY, start_str=str(dt.datetime.now()-dt.timedelta(days=30)), end_str=str(dt.datetime.now()))
        close = []
        for i in klines:
            close.append(float(i[4]))

        close_arr = numpy.asarray(close)
        close_rsi = talib.RSI(close_arr, 14)
        max_rsi = talib.MAX(close_rsi, 14)
        min_rsi = talib.MIN(close_rsi, 14)
        stochrsi = (close_rsi - min_rsi)/(max_rsi - min_rsi)
        k = talib.SMA(stochrsi, 3)*100
        d = talib.SMA(k, 3)
        if k[-2]<d[-2]:
            buy_quantity = 0.05
            sell_quantity = 0.1
        elif k[2]>d[-2]:
            sell_quantity = 0.05
            buy_quantity = 0.1
        else:
            sell_quantity = 0.1
            buy_quantity = 0.1

        # print(close)
        print("k",k[-3])
        print("d",d[-3])
        print (buy_quantity)
        print(sell_quantity)
        
        self.sell_quantity = round(float(balance*50/eth_last_price*sell_quantity),2)
        self.buy_quantity = round(float(balance*50/eth_last_price*buy_quantity),2)


    def sell(self, last_price):

        order = self.client.futures_create_order(
        symbol='ETHUSDT',
        type=self.client.ORDER_TYPE_MARKET,
        side=self.client.SIDE_SELL,
        quantity= self.sell_quantity,
        isIsolated='TRUE'
        )
        
        return(order)


    def buy(self, last_price):

        order = self.client.futures_create_order(
        symbol='ETHUSDT',
        type=self.client.ORDER_TYPE_MARKET,
        side=self.client.SIDE_BUY,
        quantity= self.buy_quantity,
        isIsolated='TRUE'
        )
        
        return(order)
        
    def close_order(self, qty, side):

        if side == "BUY":
            order = self.client.futures_create_order(
            symbol='ETHUSDT',
            side=self.client.SIDE_SELL,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )
        elif side == "SELL":
            order = self.client.futures_create_order(
            symbol='ETHUSDT',
            side=self.client.SIDE_BUY,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )