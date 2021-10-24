from config import Connect
import datetime as dt
import talib
import time
import numpy


class RSICross():
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

        short_rsi = talib.RSI(close_arr, 7)
        long_rsi = talib.RSI(close_arr, 14)

        return short_rsi, long_rsi
