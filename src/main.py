import time
from config import CHECK_INTERVAL, SYMBOL, ORDER_PERCENTAGE
from indicators import calculate_indicators
from strategy import trading_signal
from binance_service import get_historical_data, place_market_order
from order_management import calculate_order_quantity


def run_trading_bot():
    while True:
        # Fetch market data and calculate technical indicators
        df = get_historical_data(SYMBOL)
        df = calculate_indicators(df)

        # Determine the trading signal
        signal = trading_signal(df)
        print(f"🔍 Trading Signal: {signal}")

        # If a BUY or SELL signal is triggered, calculate the order quantity and execute the trade
        if signal in ["BUY", "SELL"]:
            quantity = calculate_order_quantity(SYMBOL, ORDER_PERCENTAGE)
            place_market_order(SYMBOL, signal, quantity)

        # Wait for the configured interval before checking the market again
        print(f"⏳ Waiting for {CHECK_INTERVAL / 60} minutes before the next check...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_trading_bot()
