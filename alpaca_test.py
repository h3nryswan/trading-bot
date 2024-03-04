from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime, timedelta

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

today = datetime.now().date()
# Calculate yesterday's date
yesterday = today - timedelta(days=1)

# Calculate date for 2, 3 days ago
two_days = yesterday - timedelta(days=1)
three_days = yesterday - timedelta(days=2)





request_params = StockTradesRequest(
    symbol_or_symbols="SPY",
    start=datetime(2024,2,29,14,30),
    end = datetime(2024,2,29,14,45)
)

trades = data_client.get_stock_trades(request_params)

print(trades)
