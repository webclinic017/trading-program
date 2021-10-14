from config import Connect
import datetime as dt
import talib
import numpy


class Order:
    def __init__(self):
        self.client = Connect().make_connection()
        self.client.futures_change_leverage(symbol='ETHUSDT', leverage=50)
        total_balance = self.client.futures_account_balance()
        for coin in total_balance:
            if coin['asset'] == 'USDT':
                balance = float(coin['balance'])
        eth_last_price = float(self.client.futures_recent_trades(
                    symbol='ETHUSDT')[-1]['price'])
        klines = self.client._historical_klines(
                    'ETHUSDT', self.client.KLINE_INTERVAL_1DAY, start_str=str(dt.datetime.now()-dt.timedelta(days=60)), end_str=str(dt.datetime.now()))
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
        print("k",k[-3])
        print("d",d[-3])
        print ("buy quantity",buy_quantity)
        print("sell quantity",sell_quantity)
        
        self.sell_quan = round(float(balance*50/eth_last_price*sell_quantity),2)
        self.buy_quan = round(float(balance*50/eth_last_price*buy_quantity),2)

        print(self.sell_quan)
        print(self.buy_quan)
    def sell(self, last_price):

        order = self.client.futures_create_order(
        symbol='ETHUSDT',
        type=self.client.ORDER_TYPE_MARKET,
        side=self.client.SIDE_SELL,
        quantity= self.sell_quan,
        isIsolated='TRUE'
        )
        
        return(order)


    def buy(self, last_price):

        order = self.client.futures_create_order(
        symbol='ETHUSDT',
        type=self.client.ORDER_TYPE_MARKET,
        side=self.client.SIDE_BUY,
        quantity= self.buy_quan,
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