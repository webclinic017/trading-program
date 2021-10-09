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
        self.orders = self.client.futures_get_all_orders(symbol='ETHUSDT')
        self.stop_loop()
    def stop_loop(self):   
        tstamp1 = int((dt.datetime.now() - dt.timedelta(hours = 1)).timestamp()*1000)
        counter = 0
        for order in self.orders:
            if int(order['time'])>tstamp1:
                print(order)
                counter += 1
        
        return counter



