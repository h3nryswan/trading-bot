from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.requests import  StockBarsRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime, timedelta
import pandas as pd

import pytz

trading_client = TradingClient("PK4QYWLWLCLXHRQ2EU39", "jhNufgfLEeCM0Sg9bkktn9cJSVnXRcgI7reOO3zY")

# market_order_data = MarketOrderRequest(
#     symbol="SPY",
#     qty=1,
#     side=OrderSide.BUY,
#     TimeInForce=TimeInForce.DAY
# )

# market_order = trading_client.submit_order(market_order_data)
# print(market_order)



data_client = StockHistoricalDataClient("PK4QYWLWLCLXHRQ2EU39", "jhNufgfLEeCM0Sg9bkktn9cJSVnXRcgI7reOO3zY")

us_eastern = pytz.timezone('America/New_York')
today = datetime.now(us_eastern).date()
print(today)

# Calculate yesterday's date
yesterday = today - timedelta(days=1)
print(yesterday)

# Calculate date for 2, 3 days ago
two_days = yesterday - timedelta(days=1)
three_days = yesterday - timedelta(days=2)

symbol="SPY",

def get_close_price(date, symbol):
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe= TimeFrame.Day,
        start=date,
        # datetime.combine(date, datetime.min.time()),  # 9:30 AM,
        # end = datetime.combine(date, datetime.max.time()) - timedelta(hours=6, minutes=30)  # 4:00 PM
        limit=1
    )
    start=date
    # date_string = start.strftime("%Y-%m-%d %H:%M:%S") + "+00:00"
    
    barset = data_client.get_stock_bars(request_params).df
    # print(barset)
    close = barset.xs(symbol)['close'].values[0]

    

    return close

date_list = [yesterday, two_days, three_days]
price_list = []

for i in date_list:
    closing_price = get_close_price(i,symbol)
    print(f"Closing price for {symbol} on {i}: {closing_price}")
    price_list.append(closing_price)

print(price_list)

def are_sequentially_decreasing(numbers):
    # Check if the numbers are sequentially decreasing
    return numbers[0] > numbers[1] > numbers[2]

def are_sequentially_increasing(numbers):
    # Check if the numbers are sequentially increasing
    return numbers[0] < numbers[1] < numbers[2]

# Example list of numbers

# Check if they are sequentially decreasing
long = are_sequentially_decreasing(price_list)
short = are_sequentially_increasing(price_list)
print(long, short)  # Output will be True
