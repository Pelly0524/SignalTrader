import os

# Binance API keys
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Trading pair settings
SYMBOL = "BTCUSDT"  # Trading pair

# Trading configuration
ORDER_PERCENTAGE = 0.15  # Use 5% of available capital per order
CHECK_INTERVAL = 3600  # Check the market every hour
INTERVAL = "1h"  # K-line (candlestick) interval set to 15 minutes

# RSI and MACD configuration
RSI_WINDOWS = [3, 5, 10]  # RSI time periods, can be adjusted as needed
MACD_FAST = 3  # MACD fast moving average
MACD_SLOW = 8  # MACD slow moving average
MACD_SIGNAL = 2  # MACD signal line

# Backtesting configuration
LIMIT = 2000  # Number of data points to retrieve
BINANCE_FEE = 0.001  # Binance trading fee (0.1%)
