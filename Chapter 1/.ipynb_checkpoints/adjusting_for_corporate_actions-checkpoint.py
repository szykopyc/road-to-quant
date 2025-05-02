import yfinance as yf
import pandas as pd

ticker = "AAPL"
time_period = "6mo"

price_data = yf.download(ticker, period=time_period)["Close"]
dividend_data = yf.Ticker(ticker).dividends

print(price_data.head())
print(dividend_data.head())