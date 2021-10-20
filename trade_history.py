from binance.client import Client
from config import Connect
from order import Order
import datetime as dt
import numpy
import talib
import time
import pandas as pd
from datetime import datetime


class Hist:
    def __init__(self) -> None:
        self.client = Connect().make_connection()
        self.get_trade_hist()

    def get_trade_hist(self):
        list = self.client.LinearPositions.LinearPositions_closePnlRecords(symbol="ETHUSDT").result()[0]['result']['data']
        df = pd.DataFrame([])
        today_time = dt.datetime.today().strftime('%Y-%m-%d')
        for i in list:
            df = df.append({
                "created_at": datetime.fromtimestamp(i['created_at']),
                 "id": i['id'],
                 "symbol": "ETHUSDT",
                 "order_id": i['order_id'],
                 "side": i['side'],
                 "qty": i['qty'],
                 "closed_size": i['closed_size'],    
                 "avg_entry_price": i['avg_entry_price'],    
                 "avg_exit_price": i['avg_exit_price'],    
                 "cum_entry_value": i['cum_entry_value'],   
                 "cum_exit_value": i['cum_exit_value'],  
                 "closed_pnl": i['closed_pnl'],   
                 "fill_count": i['fill_count'],           
                 "leverage": i['leverage']
             }, ignore_index=True
            )
        df.to_csv(f'trade_record/trade_record_{today_time}.csv')
        print(list)
        df.to_csv(f'trade_record/trade_record_{today_time}.csv')

Hist()