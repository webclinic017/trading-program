from config import Connect
import datetime as dt


class Order:
    def __init__(self):
        self.client = Connect().make_connection()
        self.client.futures_change_leverage(symbol='ETHUSDT', leverage=50)
        balance = float(self.client.futures_account_balance()[1]['balance'])
        eth_last_price = float(self.client.futures_recent_trades(
                    symbol='ETHUSDT')[-1]['price'])
        self.my_quantity = round(float(balance*50/eth_last_price*0.3),2)

    def sell(self, last_price):

        order = self.client.futures_create_order(
        symbol='ETHUSDT',
        type=self.client.ORDER_TYPE_MARKET,
        side=self.client.SIDE_SELL,
        quantity= self.my_quantity,
        isIsolated='TRUE'
        )
        
        return(order)


    def buy(self, last_price):

        order = self.client.futures_create_order(
        symbol='ETHUSDT',
        type=self.client.ORDER_TYPE_MARKET,
        side=self.client.SIDE_BUY,
        quantity= self.my_quantity,
        isIsolated='TRUE'
        )
        
        return(order)
        
    def close_order(self, qty, side):

        if side == "BUY":
            order = self.client.futures_create_order(
            symbol='ETHUSDT',
            side=self.client.SIDE_SELL,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )
        elif side == "SELL":
            order = self.client.futures_create_order(
            symbol='ETHUSDT',
            side=self.client.SIDE_BUY,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )