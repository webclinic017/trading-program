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
        high = []
        low = []

        for i in klines:
            close.append(float(i['close']))
            high.append(float(i['high']))
            low.append(float(i['low']))

        close_arr = numpy.asarray(close)
        high_arr = numpy.asarray(high)
        low_arr = numpy.asarray(low)

        k, d = talib.STOCH(high_arr, low_arr, close_arr, fastk_period=14, slowk_period=5, slowk_matype=0, slowd_period=5, slowd_matype=0)

        return k, d
