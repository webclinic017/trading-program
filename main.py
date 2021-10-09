from config import Connect
from order import Order
from trade_history import Hist 
import datetime as dt
import numpy
import talib
import time
import pandas as pd

class Main:
    def __init__(self):

        self.client = Connect().make_connection()
        print("logged in")
        self.df = pd.DataFrame(columns=['orderID','Time','side','2ndlast_ROC','last_ROC','2ndlast_WMSR', 'last_WMSR','2ndlast_CCI','last_CCI' 'last_price','quantity','profit'])
        self.df.to_csv(f'trade_record/trades.csv')
        self.start_trade()

    def start_trade(self):
        self.df = pd.read_csv(f'trade_record/trades.csv', index_col=0)
        self.trading = Order()
        position = float(self.client.futures_position_information(symbol='ETHUSDT')[-1][
            'positionAmt'])
        if abs(position) > 0:
            self.track_trade()
        print("Starting new trade...")

        while True:
            try:
                # Change date and/or interval for different time frame
                klines = self.client.futures_historical_klines(
                    "ETHUSDT", self.client.KLINE_INTERVAL_30MINUTE, start_str=str(dt.datetime.now()-dt.timedelta(days=1)), end_str=str(dt.datetime.now()))
            except:
                print('Timeout! Waiting for time binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                klines = self.client.futures_historical_klines(
                    "ETHUSDT", self.client.KLINE_INTERVAL_30MINUTE, start_str=str(dt.datetime.now()-dt.timedelta(days=1)), end_str=str(dt.datetime.now()))

            close = []
            high = []
            low = []
            for i in klines:
                close.append(float(i[4]))
                low.append(float(i[3]))
                high.append(float(i[2]))
            # RSI calculation, change for different strategy or indicator
            last_ROC = talib.ROC(numpy.asarray(close), 9)[-2]
            second_last_ROC = talib.ROC(numpy.asarray(close), 9)[-3]
            third_last_ROC = talib.ROC(numpy.asarray(close), 9)[-4]
            last_WMSR = talib.WILLR(numpy.asarray(high), numpy.asarray(
                low), numpy.asarray(close), 14)[-2]

            if last_ROC > 0 and last_WMSR > -50 and (second_last_ROC < 0 or third_last_ROC < 0):
                self.order_to_track = self.trading.buy(close[len(close)-1])
                print(last_ROC)
                print("BUY Order is sent")
                self.df = self.df.append({'Time': str(dt.datetime.now()),
                                'side': 'BUY',
                                'last_ROC': last_ROC,
                                '2ndlast_ROC':second_last_ROC,
                                'last_WMSR': last_WMSR,
                                'last_price':close[-1]
                                }, ignore_index=True)
                self.df.to_csv(f'trade_record/trades.csv')
                self.track_trade()

            elif last_ROC < 0  and last_WMSR < -50 and (second_last_ROC > 0 or third_last_ROC > 0):
                self.order_to_track = self.trading.sell(close[len(close)-1])
                print(last_ROC)
                print("SELL Order is sent")
                self.df = self.df.append({'Time': str(dt.datetime.now()),
                                'side': 'SELL',
                                'last_ROC': last_ROC,
                                '2ndlast_ROC':second_last_ROC,
                                'last_WMSR': last_WMSR,
                                'last_price':close[-1]
                                }, ignore_index=True)
                self.df.to_csv(f'trade_record/trades.csv')
                self.track_trade()
            else:
                time.sleep(1.5)
                print('No enter points, looking again...')

            print("ROC", last_ROC)
            print("WMSR", last_WMSR)

    def track_trade(self):

        self.df = pd.read_csv(f'trade_record/trades.csv', index_col=0)
        print("tracking")
        position = float(self.client.futures_position_information(symbol='ETHUSDT')[-1][
            'positionAmt'])
        if position > 0:
            side = 'BUY'
        else:
            side = 'SELL'
        # How much price changed in % based on current price and order price

        def percent_change(original, new):

            original = float(original)
            new = float(new)
            return (new - original)/original*100

        while True:
            time.sleep(1.5)
            try:
                # Change date and/or interval for different time frame
                klines = self.client.futures_historical_klines(
                    "ETHUSDT", self.client.KLINE_INTERVAL_30MINUTE, start_str=str(dt.datetime.now()-dt.timedelta(days=1)), end_str=str(dt.datetime.now()))
            except:
                print('Timeout! Waiting for time binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                klines = self.client.futures_historical_klines(
                    "ETHUSDT", self.client.KLINE_INTERVAL_30MINUTE, start_str=str(dt.datetime.now()-dt.timedelta(days=1)), end_str=str(dt.datetime.now()))

            close = []
            high = []
            low = []
            for i in klines:
                close.append(float(i[4]))
                low.append(float(i[3]))
                high.append(float(i[2])
                            )
            last_ROC = talib.ROC(numpy.asarray(close), 9)[-2]
            last_CCI = talib.CCI(numpy.asarray(
                high), numpy.asarray(low), numpy.asarray(close), 20)[-2]
            second_last_CCI = talib.CCI(numpy.asarray(
                high), numpy.asarray(low), numpy.asarray(close), 20)[-3]
            position = float(self.client.futures_position_information(symbol='ETHUSDT')[-1][
            'positionAmt'])
            cost = float(self.client.futures_get_all_orders(symbol='ETHUSDT')[-1]['avgPrice'])
            id = self.client.futures_get_all_orders(symbol='ETHUSDT')[-1]['orderId']
            try:
                self.last_price = self.client.futures_recent_trades(
                    symbol='ETHUSDT')[-1]['price']

            except:
                print('Timeout! Waiting for binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                self.last_price = self.client.futures_recent_trades(
                    symbol='ETHUSDT')[-1]['price']

            try:
                for i in range(-1, -10, -1):
                    last_order_status = self.client.futures_get_all_orders(symbol='ETHUSDT')[
                        i]['status']
                    if last_order_status != 'FILLED':
                        continue
                    else:
                        last_order_price = self.client.futures_get_all_orders(symbol='ETHUSDT')[
                            i]['avgPrice']
                        break
            except:
                print('Timeout! Waiting for binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                for i in range(-1, -10, -1):
                    last_order_status = self.client.futures_get_all_orders(symbol='ETHUSDT')[
                        i]['status']
                    if last_order_status != 'FILLED':
                        continue
                    else:
                        last_order_price = self.client.futures_get_all_orders(symbol='ETHUSDT')[
                            i]['avgPrice']

            change = percent_change(
                last_order_price, self.last_price)
            if(side == 'SELL'):

                change = change*-1
                print(change)
                profit = position*(close[-1]-cost)
            else:
                profit = position*(close[-1]-cost)

            # Specify the profit take and stop loss
            condition1 = (change <= -1 and side == 'BUY')
            condition2 = (change <= -1 and side == 'SELL')
            condition3 = (side == 'BUY' and second_last_CCI >
                          100 and last_CCI < 100)
            condition4 = (side == 'SELL' and second_last_CCI < -
                          100 and last_CCI > -100)
            condition5 = (side == 'BUY' and last_CCI < -100)
            condition6 = (side == 'SELL' and last_CCI > 100)

            if condition1 or condition2 or condition3 or condition4 or condition5 or condition6:
                print("condition1", condition1)
                print("condition2", condition2)
                print("condition3", condition3)
                print("condition4", condition4)
                self.end_trade()
                self.df = self.df.append({'Time': str(dt.datetime.now()),
                                'orderID': id,
                                'last_ROC': last_ROC,
                                '2ndlast_CCI': second_last_CCI,
                                'last_CCI': last_CCI,
                                'last_price':close[-1],
                                'quantity': abs(position),
                                'profit': profit
                                }, ignore_index=True)
                print('Current trade ended with profit  of:', change, '%')
                self.df.to_csv(f'trade_record/trades.csv')
                Hist().get_trade_hist()
                time.sleep(1.5)

                try:

                    # now=dt.datetime.now()
                    # sleep = (60-now.minute)*60
                    # time.sleep(sleep)
                    self.start_trade()

                except:
                    print("Can't make new trade, trying again in 120 sec...")
                    time.sleep(120)
                    self.start_trade()

            else:
                print("position: {}, secondlast CCI:{}, last CCI:{}".format(
                    side, second_last_CCI, last_CCI))
                print("Current trade profit: ", format(change, '2f'), "%")

    def end_trade(self):
        position = float(self.client.futures_position_information(symbol='ETHUSDT')[-1][
            'positionAmt'])
        if position > 0:
            side = 'BUY'
        else:
            side = 'SELL'

        self.trading.close_order(
            abs(position), side)
        print('End. Order finished successfully')


Main()
