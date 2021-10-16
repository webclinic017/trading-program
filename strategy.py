from config import Connect
import datetime as dt
import talib
import time
import numpy


class Strategy():
    def condition(self, client):
        date_before = int(
            (dt.datetime.now() - dt.timedelta(days=5)).timestamp())
        try:
            # Change date and/or interval for different time frame
            klines = (client.LinearKline.LinearKline_get(
                symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        except:
            print('Timeout! Waiting for time binance to respond...')
            time.sleep(120)
            print('Trying to connect again...')
            klines = (client.LinearKline.LinearKline_get(
                symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
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

        return k, d
