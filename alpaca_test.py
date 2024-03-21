import sys
sys.stdout = open('output.txt', 'a')

from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.requests import  StockBarsRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient
from datetime import datetime, timedelta
import pandas as pd
import pytz

api_key = "PK4QYWLWLCLXHRQ2EU39"
api_secret = "jhNufgfLEeCM0Sg9bkktn9cJSVnXRcgI7reOO3zY"

trading_client = TradingClient(api_key, api_secret )
data_client = StockHistoricalDataClient(api_key, api_secret)

def is_market_open():
    clock = trading_client.get_clock()
    market_status = clock.is_open
    return market_status

def close_all_positions():
    # Fetch open positions from Alpaca
    open_positions = trading_client.list_positions()
    
    # Iterate over open positions and submit closing orders
    for position in open_positions:
        symbol = position.symbol
        qty = position.qty
        side = OrderSide.SELL if position.side == 'long' else OrderSide.BUY  # Opposite side to close position
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY
        )
        
        # Submit market order to close position
        trading_client.submit_order(market_order_data)

def get_close_price(start, symbol):
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Hour,
            start=start
        )
        
        barset = data_client.get_stock_bars(request_params).df
        close = barset.xs(symbol)['close'].values[-1]  # Get the close price of the most recent bar
        
        return close

def are_sequentially_decreasing(numbers):
    # Check if the numbers are sequentially decreasing
    return numbers[0] > numbers[1] > numbers[2]

def are_sequentially_increasing(numbers):
    # Check if the numbers are sequentially increasing
    return numbers[0] < numbers[1] < numbers[2]

if is_market_open():

    print("The market is currently open.")
    us_eastern = pytz.timezone('America/New_York')
    now = datetime.now(us_eastern)
    print("Current Time (US Eastern):", now)

    market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    if market_close_time - now <= timedelta(minutes=10):
        print("Closing all positions...")
        close_all_positions()
        
    else:
        print("Market will close in more than 5 minutes. No action taken.")

        three_hours_ago = now - timedelta(hours=3)
        two_hours_ago = now - timedelta(hours=2)
        one_hours_ago = now - timedelta(hours=1)

        symbol = "SPY"
        date_list = [one_hours_ago, two_hours_ago, three_hours_ago]
        price_list = []

        for i in date_list:
            closing_price = get_close_price(i,symbol)
            print(f"Closing price for {symbol} on {i}: {closing_price}")
            price_list.append(closing_price)

        print(price_list)

        # Check if they are sequentially decreasing
        long = are_sequentially_decreasing(price_list)
        short = are_sequentially_increasing(price_list)
        print(long, short)  # Output will be True
        trade = False

        if long:
            trade = True
            market_order_data = MarketOrderRequest(
                symbol="SPY",
                qty=1,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
        elif short:
            trade = True
            market_order_data = MarketOrderRequest(
                symbol="SPY",
                qty=1,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )
            
        if trade:
            market_order = trading_client.submit_order(market_order_data)
            print(market_order)
        else:
            print("No trade supported")

else:
    print("The market is currently closed.")
