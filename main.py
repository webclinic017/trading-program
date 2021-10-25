from config import Connect
from order import Order
from stop_loop import Stop
import datetime as dt
import numpy
import talib
import time
import pandas as pd
from strategy import Strategy
from rsiCross import RSICross

class Main:
    def __init__(self):

        self.client = Connect().make_connection()
        print("logged in")
        self.trade_symbol = 'ETHUSDT'
        self.start_trade()

##########Start Trade#############

    def start_trade(self):
        self.trading = Order()
        date_before = int(
            (dt.datetime.now() - dt.timedelta(days=5)).timestamp())
        buy_position = (self.client.LinearPositions.LinearPositions_myPosition(
            symbol="ETHUSDT").result()[0]['result'][0]['size'])
        sell_position = (self.client.LinearPositions.LinearPositions_myPosition(
            symbol="ETHUSDT").result()[0]['result'][1]['size'])
        if abs(buy_position) > 0 or abs(sell_position) > 0:
            self.track_trade()
        print("Starting new trade...")

##########GET Klines Data#############
        while True:
            buy_position = (self.client.LinearPositions.LinearPositions_myPosition(
                symbol="ETHUSDT").result()[0]['result'][0]['size'])
            sell_position = (self.client.LinearPositions.LinearPositions_myPosition(
                symbol="ETHUSDT").result()[0]['result'][1]['size'])
            if (buy_position>0 or sell_position>0):
                self.track_trade()

            k = Strategy().condition(self.client)[0]
            d = Strategy().condition(self.client)[1]
            buy_condition1 = k[-3] < d[-3] and k[-2] > d[-2]
            buy_condition2 = k[-3] < 25
            sell_condition1 = k[-3] > d[-3] and k[-2] < d[-2]
            sell_condition2 = k[-3] > 75

            if buy_condition1 and buy_condition2:
                self.order_to_track = self.trading.buy()
                print("BUY Order is sent")
                self.track_trade()

            elif sell_condition1 and sell_condition2:
                self.order_to_track = self.trading.sell()
                print("SELL Order is sent")
                self.track_trade()

            else:
                time.sleep(1.5)
                print('No enter points, looking again...')

            print("last_k", k[-2])
            print("last_d", d[-2])

######################### Track Trade #############
    def track_trade(self):
        print("tracking")
        date_before = int(
            (dt.datetime.now() - dt.timedelta(days=5)).timestamp())

        buy_position = (self.client.LinearPositions.LinearPositions_myPosition(
            symbol="ETHUSDT").result()[0]['result'][0]['size'])
        sell_position = (self.client.LinearPositions.LinearPositions_myPosition(
            symbol="ETHUSDT").result()[0]['result'][1]['size'])
        if buy_position > 0:
            side = 'BUY'
            position_size=buy_position
        elif sell_position > 0:
            side = 'SELL'
            position_size=sell_position

        # How much price changed in % based on current price and order price
        

        def percent_change(original, new):

            original = float(original)
            new = float(new)
            return (new - original)/original*100

        while True:
            time.sleep(1.5)
            try:
                if side == 'BUY':
                    entry_price = self.client.LinearPositions.LinearPositions_myPosition(
                        symbol="ETHUSDT").result()[0]['result'][0]['entry_price']
                elif side == 'SELL':
                    entry_price = self.client.LinearPositions.LinearPositions_myPosition(
                        symbol="ETHUSDT").result()[0]['result'][1]['entry_price']

            except:
                print('Timeout! Waiting for bybit to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                if side == 'BUY':
                    entry_price = self.client.LinearPositions.LinearPositions_myPosition(
                        symbol="ETHUSDT").result()[0]['result'][0]['entry_price']
                elif side == 'SELL':
                    entry_price = self.client.LinearPositions.LinearPositions_myPosition(
                        symbol="ETHUSDT").result()[0]['result'][1]['entry_price']

            try:
                last_price = self.client.LinearMarket.LinearMarket_trading(
                    symbol="ETHUSDT").result()[0]['result'][0]['price']
            except:
                print('Timeout! Waiting for bybit to respond...')
                time.sleep(120)
                print('Trying to connect again...')
                last_price = self.client.LinearMarket.LinearMarket_trading(
                    symbol="ETHUSDT").result()[0]['result'][0]['price']

            change = percent_change(
                entry_price, last_price)
            liquid_price = round(entry_price*0.995,2)

            if(side == 'SELL'):
                change = change*-1
                liquid_price = round(entry_price*1.005,2)


            k = Strategy().condition(self.client)[0]
            d = Strategy().condition(self.client)[1]

            buy_condition1 = k[-3] < d[-3] and k[-2] > d[-2]
            sell_condition1 = k[-3] > d[-3] and k[-2] < d[-2]

            ######
            time_list = []
            self.orders = self.client.LinearExecution.LinearExecution_getTrades(
                symbol="ETHUSDT").result()[0]['result']['data']
            for order in self.orders:
                time_list.append(order['trade_time'])
            

            # Specify the profit take and stop loss
            end_condition = change < -0.5
            if (side == 'BUY' and sell_condition1) or (side == 'SELL' and buy_condition1) or end_condition:
                self.end_trade()
                print('Current trade ended with profit  of:', change, '%')
                time.sleep(1.5)

                try:
                    self.start_trade()

                except:
                    print("Can't make new trade, trying again in 120 sec...")
                    time.sleep(120)
                    self.start_trade()

            else:
                print('****************************************************')
                print("position:{}, entry_price:{}, current_price:{}, liquidation_price:{}, position_size:{}, last_k > last_d:{}, k > d:{}".format(
                    side, entry_price, last_price, liquid_price,position_size ,k[-3]>d[-3],k[-2]>d[-2] ))
                print("Current trade profit: ", format(change, '2f'), "%")

    ######end trade###########
    def end_trade(self):
        buy_position = (self.client.LinearPositions.LinearPositions_myPosition(
            symbol="ETHUSDT").result()[0]['result'][0]['size'])
        sell_position = (self.client.LinearPositions.LinearPositions_myPosition(
            symbol="ETHUSDT").result()[0]['result'][1]['size'])

        counter = Stop().stop_loop()
        if counter > 30:
            time.sleep(3600)

        if abs(buy_position) > 0:
            side = 'BUY'
            self.trading.close_order(
                abs(buy_position), side)
        elif abs(sell_position) > 0:
            side = 'SELL'
            self.trading.close_order(
               abs(sell_position), side)
        print('End. Order finished successfully')


Main()
