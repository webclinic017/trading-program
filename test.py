from binance.client import Client
from config import Connect
from order import Order
from datetime import datetime
import numpy
import talib
import time
import pandas as pd
import datetime as dt


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

        # list = self.client.LinearPositions.LinearPositions_closePnlRecords(symbol="ETHUSDT").result()[0]['result']['data']
        # df = pd.DataFrame([])
        # today_time = dt.datetime.today().strftime('%Y-%m-%d')
        # for i in list:
        #     df = df.append({
        #         "created_at": datetime.fromtimestamp(i['created_at']),
        #          "id": i['id'],
        #          "symbol": "ETHUSDT",
        #          "order_id": i['order_id'],
        #          "side": i['side'],
        #          "qty": i['qty'],
        #          "closed_size": i['closed_size'],
        #          "avg_entry_price": i['avg_entry_price'],
        #          "avg_exit_price": i['avg_exit_price'],
        #          "cum_entry_value": i['cum_entry_value'],
        #          "cum_exit_value": i['cum_exit_value'],
        #          "closed_pnl": i['closed_pnl'],
        #          "fill_count": i['fill_count'],
        #          "leverage": i['leverage']
        #      }, ignore_index=True
        #     )
        # df.to_csv(f'trade_record/trade_record_{today_time}.csv')
        # print(list)
        # date_before = int(
        #     (dt.datetime.now() - dt.timedelta(days=4)).timestamp())
        # try:
        #     # Change date and/or interval for different time frame
        #     klines = (self.client.LinearKline.LinearKline_get(
        #         symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        # except:
        #     print('Timeout! Waiting for time binance to respond...')
        #     time.sleep(120)
        #     print('Trying to connect again...')
        #     klines = (self.client.LinearKline.LinearKline_get(
        #         symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        # close = []
        # open_time=[]
        # for i in klines:
        #     close.append(float(i['close']))
        #     open_time.append(float(i['open_time']))

        # close_arr = numpy.asarray(close)
        # open_time_arr = numpy.asarray(open_time)

        # short_rsi = talib.RSI(close_arr, 7)
        # long_rsi = talib.RSI(close_arr, 14)

        # df = pd.DataFrame(open_time_arr)
        # df.to_csv("time.csv")
        # print(long_rsi)

        # time_list = []
        # self.orders = self.client.LinearExecution.LinearExecution_getTrades(
        #     symbol="ETHUSDT").result()[0]['result']['data']
        # for order in self.orders:
        #     time_list.append(order['trade_time'])

        # tstamp1=int(time_list[0])
        # tstamp2=int(dt.datetime.now().timestamp())
        # time1 = dt.datetime.fromtimestamp(tstamp1)
        # time2 = dt.datetime.fromtimestamp(tstamp2)
        # time_difference = time2 - time1
        # time_diff_hour =time_difference.total_seconds()/3600
        # end_condtion2= time_diff_hour>2
        # print(time_diff_hour)

        # date_before = int(
        #     (dt.datetime.now() - dt.timedelta(days=5)).timestamp())
        # try:
        #     # Change date and/or interval for different time frame
        #     klines = (self.client.LinearKline.LinearKline_get(
        #         symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        # except:
        #     print('Timeout! Waiting for time binance to respond...')
        #     time.sleep(120)
        #     print('Trying to connect again...')
        #     klines = (self.client.LinearKline.LinearKline_get(
        #         symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        # close = []
        # high = []
        # low = []

        # for i in klines:
        #     close.append(float(i['close']))
        #     high.append(float(i['high']))
        #     low.append(float(i['low']))

        # close_arr = numpy.asarray(close)
        # high_arr = numpy.asarray(high)
        # low_arr = numpy.asarray(low)

        # close_rsi = talib.RSI(close_arr, 14)
        # max_rsi = talib.MAX(close_rsi, 14)
        # min_rsi = talib.MIN(close_rsi, 14)
        # stochrsi = (close_rsi - min_rsi)/(max_rsi - min_rsi)
        # k = talib.SMA(stochrsi, 3)*100
        # d = talib.SMA(k, 3)

        # mom_k = talib.MOM(k,10)

        

        # tstamp1=int(time_list[0])
        # tstamp2=int(dt.datetime.now().timestamp())
        # time1 = dt.datetime.fromtimestamp(tstamp1)
        # time2 = dt.datetime.fromtimestamp(tstamp2)
        # time_difference = time2 - time1
        # time_diff_hour =time_difference.total_seconds()/3600
        # end_condtion2= time_diff_hour>2

        # date_before = int(
        #     (dt.datetime.now() - dt.timedelta(days=5)).timestamp())
        # klines = (self.client.LinearKline.LinearKline_get(
        #     symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        # # final_df = pd.DataFrame(
        # # columns=['open', 'high', 'low', 'close', 'volume', 'openinterest', 'datetime'])
        # df = pd.DataFrame(klines)
        # final_df = df[['open', 'high', 'low', 'close']]
        # df = datetime.fromtimestamp(df[['open_time']])
        # # df = df[['datetime','open', 'high', 'low', 'close', 'volume', 'openinterest']]
        # final_df.to_csv('mydf.csv')


Kai()
