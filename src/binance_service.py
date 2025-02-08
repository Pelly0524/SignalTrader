from binance.client import Client
from config import api_key, api_secret, INTERVAL
from tqdm import tqdm
import pandas as pd
import datetime
import os

# Initialize the Binance client
client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"  # Using the testnet for safety


# Fetch historical market data and return as a DataFrame
def get_historical_data(symbol, interval=INTERVAL, limit=200):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    close_prices = [float(kline[4]) for kline in klines]  # Closing prices
    return pd.DataFrame({"close": close_prices})


# Fetch large historical market data for backtesting using multiple requests
def get_full_historical_data(symbol, interval=INTERVAL, limit=2000):
    all_klines = []  # Store data from multiple requests
    end_time = None  # Track where to start the next request

    # Binance API batch limit
    batch_limit = 1000

    with tqdm(total=limit, desc=f"Fetching {symbol} historical data") as pbar:
        while len(all_klines) < limit:
            klines = client.get_klines(
                symbol=symbol, interval=interval, limit=batch_limit, endTime=end_time
            )

            # If no more data is returned, stop requesting
            if not klines:
                break

            all_klines.extend(klines)
            pbar.update(len(klines))  # 更新進度條

            # Update the end_time to the first timestamp of this batch to fetch older data
            end_time = klines[0][0]  # The first kline's timestamp (in milliseconds)

            # If we reach the required limit, stop requesting
            if len(all_klines) >= limit:
                break

    # Process data into a DataFrame
    all_klines = all_klines[:limit]
    data = {
        "timestamp": [pd.to_datetime(kline[0], unit="ms") for kline in all_klines],
        "open": [float(kline[1]) for kline in all_klines],
        "high": [float(kline[2]) for kline in all_klines],
        "low": [float(kline[3]) for kline in all_klines],
        "close": [float(kline[4]) for kline in all_klines],
        "volume": [float(kline[5]) for kline in all_klines],
    }
    return pd.DataFrame(data)


# Get USDT balance
def get_balance(asset="USDT"):
    balance = client.get_asset_balance(asset=asset)
    return float(balance["free"])


# Get the current price of the symbol
def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])


# Execute a market order and log the transaction
def place_market_order(symbol, side, quantity):
    try:
        if side == "BUY":
            order = client.create_order(
                symbol=symbol, side="BUY", type="MARKET", quantity=float(quantity)
            )
            log_trade("BUY", symbol, quantity, order["fills"][0]["price"])
        elif side == "SELL":
            order = client.order_market_sell(symbol=symbol, quantity=quantity)
            log_trade("SELL", symbol, quantity, order["fills"][0]["price"])
    except Exception as e:
        print(f"❌ Order failed: {e}")


# Log the transaction to a log file
def log_trade(action, symbol, quantity, price):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{current_time}] {action} {quantity} {symbol} at price {price}\n"

    # Write log entry to the log file
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open("logs/trade_log.txt", "a") as log_file:
        log_file.write(log_entry)

    print(f"📄 Trade logged: {log_entry.strip()}")


if __name__ == "__main__":
    info = client.get_symbol_info("BTCUSDT")
