from indicators import calculate_indicators
from strategy import trading_signal
from config import ORDER_PERCENTAGE, BINANCE_FEE, SYMBOL, INTERVAL, LIMIT
from binance_service import get_full_historical_data


# Backtesting strategy
def backtest_strategy(data, initial_balance=10000):
    balance = initial_balance
    position = 0
    trades = []

    # Calculate technical indicators
    data = calculate_indicators(data)

    for i in range(len(data)):
        # Use the latest data point to determine the signal
        signal = trading_signal(data.iloc[i : i + 1])
        price = data["close"].iloc[i]

        # Handle the signal
        if signal == "BUY" and position == 0:
            quantity = (balance * ORDER_PERCENTAGE) / price  # Calculate order quantity
            position += quantity
            balance -= quantity * price
            trades.append(f"BUY at {price}, quantity: {quantity}")

        elif signal == "SELL" and position > 0:
            gross_profit = position * price
            net_profit = gross_profit * (1 - BINANCE_FEE)  # Deduct trading fees
            balance += net_profit
            trades.append(
                f"SELL at {price}, quantity: {position}, net_profit: {net_profit:.2f}"
            )
            position = 0  # Clear the position

    # Calculate the final balance
    final_balance = balance + (position * data["close"].iloc[-1])
    profit = final_balance - initial_balance

    # Display the results
    print(f"Initial Balance: ${initial_balance:.2f}")
    print(f"Final Balance: ${final_balance:.2f}")
    print(f"Total Profit: ${profit:.2f}")

    # Output the trade log
    print("\nTrade Log:")
    for trade in trades:
        print(trade)


# Main function
if __name__ == "__main__":
    # Fetch historical data from Binance
    print("Fetching historical data from Binance...")
    data = get_full_historical_data(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
    print(f"Fetched {len(data)} rows of historical data.")

    # Execute backtest
    backtest_strategy(data)
