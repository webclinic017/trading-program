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
        self.df = pd.DataFrame(columns=['orderID', 'Time', 'side','last_price', 'quantity', 'profit','balance'])
        self.df.to_csv(f'trade_record/trade_record.csv')

        self.get_trade_hist()

    def get_trade_hist(self):
            self.df = pd.read_csv(f'trade_record/trade_record.csv', index_col=0)
            trades = self.client.futures_account_trades(symbol='ETHUSDT')
            temp_orderId = "0"
            orderId = []
            orders = self.client.futures_get_all_orders(symbol='ETHUSDT')
            balance = float(self.client.futures_account_balance()[1]['balance'])
            
            for trade in trades:
                trade_timestamp = int(trade['time']/1000)
                trade_time = datetime.fromtimestamp(trade_timestamp).strftime('%Y-%m-%d')
                today_time = dt.datetime.today().strftime('%Y-%m-%d')
                trade_time_record = datetime.fromtimestamp(trade_timestamp).strftime('%Y-%m-%d, %H:%M:%S')
                if trade_time==today_time:
                    if temp_orderId != trade['orderId']:
                        
                        temp_orderId = trade['orderId']
                        realizedPnl = float(trade['realizedPnl'])
                        orderId.append(temp_orderId)
                        for order in orders:
                            if order['orderId'] == temp_orderId: 
                                quantity = order['executedQty']
                                last_price = order['avgPrice'] 
                                side = order['side']

                        self.df = self.df.append({'Time': trade_time_record,
                                    'orderID': temp_orderId,
                                    'side': side,
                                    'last_price': last_price,
                                    'quantity': quantity,
                                    'profit': realizedPnl,
                                    'balance':balance
                                    }, ignore_index=True)
                    else:
                        realizedPnl += float(trade['realizedPnl'])
                        self.df.loc[self.df['orderID']==temp_orderId, 'profit'] = realizedPnl
            
            self.df.to_csv(f'trade_record/trade_record_{today_time}.csv')



