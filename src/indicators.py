import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from config import RSI_WINDOWS, MACD_FAST, MACD_SLOW, MACD_SIGNAL


# Calculate RSI and MACD indicators
def calculate_indicators(df):
    df["RSI_Short"] = RSIIndicator(df["close"], window=RSI_WINDOWS[0]).rsi()
    df["RSI_Mid"] = RSIIndicator(df["close"], window=RSI_WINDOWS[1]).rsi()
    df["RSI_Long"] = RSIIndicator(df["close"], window=RSI_WINDOWS[2]).rsi()

    macd = MACD(
        df["close"],
        window_slow=MACD_SLOW,
        window_fast=MACD_FAST,
        window_sign=MACD_SIGNAL,
    )
    df["MACD_Line"] = macd.macd()
    df["MACD_Signal_Line"] = macd.macd_signal()
    df["MACD_Histogram"] = macd.macd_diff()

    return df
