from binance.client import Client
from config import Connect
from order import Order
import datetime as dt
import numpy
import talib
import time
import pandas as pd


class Stop:
    def __init__(self) -> None:
        self.client = Connect().make_connection()
        self.orders = self.client.LinearExecution.LinearExecution_getTrades(
            symbol="ETHUSDT").result()[0]['result']['data']
        self.stop_loop()

    def stop_loop(self):
        tstamp1 = int((dt.datetime.now() - dt.timedelta(minutes=5)).timestamp())
        counter = 0
        for order in self.orders:
            if int(order['trade_time']) > tstamp1:
                counter += 1

        return counter
