from pylab import mpl
import pandas as pd
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt
import tushare as ts
from config import Connect
import datetime as dt
import talib
import time
import numpy
from dateutil import tz
from collections import defaultdict


class my_strategy1(bt.Strategy):

    # 全局设定交易策略的参数
    params = (
        ('maperiod', 20), ('rsi_period', 14), ('k_period', 3),
        ('d_period', 3), ('mom_period', 3)
    )

    def __init__(self):
        # 指定价格序列
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 添加移动均线指标，内置了talib模块
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        self.close_rsi = bt.talib.RSI(
            self.dataclose, timeperiod=14)
        self.max_rsi = bt.talib.MAX(self.close_rsi, timeperiod=14)
        self.min_rsi = bt.talib.MIN(self.close_rsi, timeperiod=14)
        self.stochrsi = (self.close_rsi - self.min_rsi) / \
                         (self.max_rsi - self.min_rsi)
        self.k = bt.talib.SMA(self.stochrsi, timeperiod=3)*100
        self.d = bt.talib.SMA(self.k, timeperiod=3)
        self.mom_k = bt.talib.MOM(self.k, timeperiod=10)

    def next(self):
        if not self.position:  # 没有持仓

            if self.mom_k[-2] < 0 and self.mom_k[-1] > 0:
                # 执行买入
                print('buy order sent')
                self.order = self.buy(price=self.dataopen[0],size=1)
            elif self.mom_k[-2] > 0 and self.mom_k[-1] < 0:
                # 执行卖出
                print('sell order sent')
                self.order = self.sell(price=self.dataopen[0],size=1)
        else:
            
            if int(self.position.size) == -1 and self.mom_k[-2] < 0 and self.mom_k[-1] > 0:
                # 执行买入
                print('close sell')
                self.order = self.buy(price=self.dataopen[0],size=1)
            elif int(self.position.size) == 1 and self.mom_k[-2] > 0 and self.mom_k[-1] < 0:
                # 执行卖出
                print('close buy')
                self.order = self.sell(price=self.dataopen[0],size=1)

# 正常显示画图时出现的中文和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 使用tushare旧版接口获取数据
client = Connect().make_connection()
print("logged in")


def get_data():
    mytime = dt.datetime.now() - dt.timedelta(days=5)
    date_before = int(
        (mytime).timestamp())
    klines = (client.LinearKline.LinearKline_get(
        symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
    df = pd.DataFrame(klines)
    for i in range(10):
        mytime = mytime - dt.timedelta(days=5)
        date_before = int((mytime).timestamp())
        next_klines = (client.LinearKline.LinearKline_get(
        symbol="ETHUSDT", interval="60", **{'from': date_before}).result()[0]['result'])
        df = df.append(next_klines, sort=True)

    
    final_df = df['openinterest'] = 0
    final_df = df[['open', 'high', 'low', 'close', 'volume', 'openinterest']]
    final_df.index = pd.to_datetime(df['open_time'], unit='s').dt.tz_localize(tz.tzlocal())
    final_df = final_df.sort_values(by="open_time")
    final_df.to_csv('mydf.csv')

    
    datapath = ('mydf.csv')
    dataframe = pd.read_csv(datapath,
                            parse_dates=True,
                            index_col=0)
    return dataframe


dataframe = get_data()
# 回测期间
start = datetime(2021, 9, 1)
end = datetime(2021, 10, 27)
# 加载数据
data = bt.feeds.PandasData(dataname=dataframe, fromdate=start, todate=end)

if __name__ == '__main__':
    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    # 将数据传入回测系统
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    cerebro.addstrategy(my_strategy1)
    # 设置初始资本为10,000
    startcash = 1000000
    cerebro.broker.setcash(startcash)
    # 设置交易手续费为 0.2%
    cerebro.broker.setcommission(commission=0.002)


d1 = start.strftime('%Y%m%d')
d2 = end.strftime('%Y%m%d')
print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')
# 运行回测系统
cerebro.run()
# 获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
# 打印结果
print(f'总资金: {round(portvalue,2)}')

print(f'净收益: {round(pnl,2)}')
