from config import Connect
from order import Order
from trade_history import Hist
from stop_loop import Stop
import datetime as dt
import numpy
import talib
import time
import pandas as pd


class Main:
    def __init__(self):

        self.client = Connect().make_connection()
        print("logged in")
        self.df = pd.DataFrame(columns=['orderID', 'Time', 'side', '2ndlast_ROC', 'last_ROC',
                               '2ndlast_WMSR', 'last_WMSR', '2ndlast_CCI', 'last_CCI' 'last_price', 'quantity', 'profit'])
        self.df.to_csv(f'trade_record/trades.csv')
        self.trade_symbol = 'ETHUSDT'
        self.start_trade()

    def start_trade(self):
        self.df = pd.read_csv(f'trade_record/trades.csv', index_col=0)
        self.trading = Order()
        position = float(self.client.futures_position_information(symbol=self.trade_symbol)[-1][
            'positionAmt'])
        if abs(position) > 0:
            self.track_trade()
        print("Starting new trade...")

        while True:
            try:
                # Change date and/or interval for different time frame
                klines = self.client._historical_klines(
                    self.trade_symbol, self.client.KLINE_INTERVAL_1HOUR, start_str=str(dt.datetime.now()-dt.timedelta(days=5)), end_str=str(dt.datetime.now()))
            except:
                print('Timeout! Waiting for time binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                klines = self.client._historical_klines(
                    self.trade_symbol, self.client.KLINE_INTERVAL_1HOUR, start_str=str(dt.datetime.now()-dt.timedelta(days=5)), end_str=str(dt.datetime.now()))

            close = []
            volume = []
            for i in klines:
                close.append(float(i[4]))
                volume.append(float(i[5]))

                # RSI calculation, change for different strategy or indicator
            last_vma = talib.MA(numpy.asarray(volume), 20)
            last_vma_ROC = talib.ROC(last_vma, 20)[-2]
            last_vma_ROC2 = talib.ROC(last_vma, 20)[-3]

            print(last_vma)
            print(last_vma_ROC)

            if last_vma_ROC2 < 0 and last_vma_ROC > 0:
                self.order_to_track = self.trading.buy(close[len(close)-1])
                print(last_vma_ROC)
                print("BUY Order is sent")
                self.track_trade()

            elif last_vma_ROC2 > 0 and last_vma_ROC < 0:
                self.order_to_track = self.trading.sell(close[len(close)-1])
                print(last_vma_ROC)
                print("SELL Order is sent")
                self.track_trade()

            else:
                time.sleep(1.5)
                print('No enter points, looking again...')

            print("VMA", last_vma)
            print("ROC(vma)", last_vma_ROC)

    def track_trade(self):

        self.df = pd.read_csv(f'trade_record/trades.csv', index_col=0)
        print("tracking")
        position = float(self.client.futures_position_information(symbol=self.trade_symbol)[-1][
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
                klines = self.client._historical_klines(
                    self.trade_symbol, self.client.KLINE_INTERVAL_1HOUR, start_str=str(dt.datetime.now()-dt.timedelta(days=5)), end_str=str(dt.datetime.now()))
            except:
                print('Timeout! Waiting for time binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                klines = self.client._historical_klines(
                    self.trade_symbol, self.client.KLINE_INTERVAL_1HOUR, start_str=str(dt.datetime.now()-dt.timedelta(days=5)), end_str=str(dt.datetime.now()))

            close = []
            volume = []
            for i in klines:
                close.append(float(i[4]))
                volume.append(float(i[5]))

                # RSI calculation, change for different strategy or indicator
            last_vma = talib.MA(numpy.asarray(volume), 20)
            last_vma_ROC = talib.ROC(last_vma, 20)[-2]
            last_vma_ROC2 = talib.ROC(last_vma, 20)[-3]

            position = float(self.client.futures_position_information(symbol=self.trade_symbol)[-1][
                'positionAmt'])
            cost = float(self.client.futures_get_all_orders(
                symbol=self.trade_symbol)[-1]['avgPrice'])
            id = self.client.futures_get_all_orders(
                symbol=self.trade_symbol)[-1]['orderId']
            try:
                self.last_price = self.client.futures_recent_trades(
                    symbol=self.trade_symbol)[-1]['price']

            except:
                print('Timeout! Waiting for binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                self.last_price = self.client.futures_recent_trades(
                    symbol=self.trade_symbol)[-1]['price']

            try:
                for i in range(-1, -10, -1):
                    last_order_status = self.client.futures_get_all_orders(symbol=self.trade_symbol)[
                        i]['status']
                    if last_order_status != 'FILLED':
                        continue
                    else:
                        last_order_price = self.client.futures_get_all_orders(symbol=self.trade_symbol)[
                            i]['avgPrice']
                        break
            except:
                print('Timeout! Waiting for binance to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                for i in range(-1, -10, -1):
                    last_order_status = self.client.futures_get_all_orders(symbol=self.trade_symbol)[
                        i]['status']
                    if last_order_status != 'FILLED':
                        continue
                    else:
                        last_order_price = self.client.futures_get_all_orders(symbol=self.trade_symbol)[
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
            end_buy_condition = last_vma_ROC2 > 0 and last_vma_ROC < 0
            end_sell_condition = last_vma_ROC2 < 0 and last_vma_ROC > 0

            if (side == 'BUY' and end_buy_condition) or (side == 'SELL' and end_sell_condition):
                self.end_trade()
                print('Current trade ended with profit  of:', change, '%')
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
                print("position: {},entry_price:{}, vma:{}, roc:{}".format(
                    side, last_order_price, last_vma[-2], last_vma_ROC))
                print("Current trade profit: ", format(change, '2f'), "%")

    def end_trade(self):
        position = float(self.client.futures_position_information(symbol=self.trade_symbol)[-1][
            'positionAmt'])
        counter = Stop().stop_loop()
        if counter > 5:
            time.sleep(3600)

        if position > 0:
            side = 'BUY'
        else:
            side = 'SELL'

        self.trading.close_order(
            abs(position), side)
        print('End. Order finished successfully')


Main()
