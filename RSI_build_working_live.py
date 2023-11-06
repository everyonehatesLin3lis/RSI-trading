from config1 import ALPACA_CONFIG
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import pandas as pd

class SwingHigh(Strategy):
    data = []
    order_number = 0
    def initialize(self):
        self.sleeptime = "20S"


    def on_trading_iteration(self):
        symbol ="ARM"
        entry_price = self.get_last_price(symbol)
        self.log_message(f"Position: {self.get_position(symbol)}")
        self.data.append(self.get_last_price(symbol))
        entry_pricee = 0

        if len(self.data) > 16:
            period = len(self.data[-15:])
            delta = pd.Series(self.data[-15:])
            delta = delta.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta <0, 0)
            avg_gain = gain.rolling(period).mean()
            avg_loss = loss.rolling(period).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            print(rsi.iloc[-1])
            RSI = rsi.iloc[-1]


            if RSI <=50 and self.get_position(symbol) is None :
                self.log_message(f"Last RSI prints: {RSI}")
                self.log_message(f"Last RSI prints: {self.data[-1]}")
                order = self.create_order(symbol, quantity = 10, side = "buy")
                self.submit_order(order)
                self.order_number += 1
                if self.order_number == 1:
                    self.log_message(f"Entry RSI: {RSI}; Entry price: {self.data[-1]}")
                    entry_pricee = self.data[-1] 
            elif self.get_position(symbol) and self.data[-1] < entry_pricee * .99:
                print("elif test su .998")
            elif self.get_position(symbol) and self.data[-1] < entry_pricee * .99:
                print("cia entry price is elif", entry_pricee)
                print("cia self.data-1 is elif", self.data[-1])
                print("cia self get position is elif", self.get_position(symbol))
                self.sell_all()
                self.order_number = 0

            elif self.get_position(symbol) and self.data[-1] >= entry_pricee * 1.002:
                self.sell_all()
                self.order_number = 0
            

    def before_market_closes(self):
        self.sell_all()


if __name__ == "__main__":
    broker = Alpaca(ALPACA_CONFIG)
    strategy = SwingHigh(broker=broker)
    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()
