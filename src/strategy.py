# Determine the trading signal based on RSI and MACD indicators
def trading_signal(df):
    # Get the latest values for RSI and MACD
    latest_rsi_short = df["RSI_Short"].iloc[-1]  # Most recent short-term RSI
    latest_macd_line = df["MACD_Line"].iloc[-1]  # Most recent MACD main line
    latest_macd_signal = df["MACD_Signal_Line"].iloc[-1]  # Most recent MACD signal line

    # Buy signal: Short-term RSI indicates oversold, and MACD shows upward momentum
    if latest_rsi_short < 40 and latest_macd_line > latest_macd_signal:
        return "BUY"

    # Sell signal: Short-term RSI indicates overbought, and MACD shows downward momentum
    if latest_rsi_short > 60 and latest_macd_line < latest_macd_signal:
        return "SELL"

    # No strong signal, hold the current position
    return "HOLD"
