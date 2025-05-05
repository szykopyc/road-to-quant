#!/usr/bin/env python
# coding: utf-8

# ## Momentum Trading Strategy based on Section 2.2.2 of Quantitative Portfolio Management
# ### Imports, tickers, and data downloads. Convert to log returns

# In[190]:


import pandas as pd
import numpy as np
import yfinance as yf
from time import sleep
import os.path


# In[192]:


stocks_tickers = pd.read_csv("liquid_us_stocks.csv")
ticker_company_dict = {key: value for key,value in zip(stocks_tickers["Ticker"],stocks_tickers["Company Name"])}


# In[195]:


stocks_tickers = stocks_tickers[["Ticker"]]


# In[182]:


stocks_tickers.head()


# In[212]:


stocks_tickers = stocks_tickers["Ticker"].tolist()


# In[213]:


def batch_download_data(tickers, period, batch_size=5, file_path='stock_data.csv'):
    all_data = pd.DataFrame()

    for i in range(0, len(tickers), batch_size):
        batch_tickers = tickers[i:i+batch_size]
        print(f"Downloading data for {batch_tickers}")
        
        batch_data = yf.download(batch_tickers, period=period, auto_adjust=True)["Close"]
        if isinstance(batch_data, pd.Series):
            batch_data = batch_data.to_frame()

        na_count = batch_data.isna().sum().sum()
        print(f"Downloaded data for {batch_tickers} with NA count: {na_count}")
        
        all_data = pd.concat([all_data, batch_data], axis=1)
        sleep(30)

    return all_data

period = "1y"

if os.path.exists('stock_data.pkl'):
    stock_data = pd.read_pickle("stock_data.pkl")
else:
    downloaded_data = batch_download_data(stocks_tickers, period, 5)
    downloaded_data.to_pickle("stock_data.pkl")


# In[214]:


stock_data = pd.read_pickle("stock_data.pkl")


# In[215]:


stock_log_returns_data = np.log(stock_data/stock_data.shift(1))


# In[216]:


print(stock_log_returns_data.isna().sum().sum())


# In[217]:


stock_log_returns_data = stock_log_returns_data.dropna()


# ## Creating the momentum signal
# - For each stock *s* on day *d*, compute past *k*-day returns (7 day returns)
# - Rank stocks by past return
# - Go long (1) top decile, and short (-1) bottom decile

# In[218]:


def momentum_signal(df, k):
    k_day_returns = np.exp(df.rolling(window=k).sum())-1

    signal_returns = k_day_returns.shift(1)

    signal_returns = signal_returns.dropna()

    daily_ranks = signal_returns.rank(axis=1, method='first',ascending=False)
    
    n_stocks = signal_returns.shape[1]

    top_n = int(n_stocks*0.1)
    bottom_n = int(n_stocks*0.1)

    signals = pd.DataFrame(np.where(daily_ranks <= top_n, 1, np.where(daily_ranks > n_stocks - bottom_n, -1, 0)), index=signal_returns.index, columns=signal_returns.columns)

    return signals


# In[219]:


signals = momentum_signal(stock_log_returns_data, 21)


# In[220]:


signals.head()


# ## Simple backtest

# In[221]:


portfolio_returns = []
capital = 100000
cash = capital
positions = {}
portfolio_returns = []
previous_portfolio_value = capital

common_dates = signals.index.intersection(stock_data.index)
signals = signals.loc[common_dates]
stock_prices = stock_data.loc[common_dates]
stock_log_returns = stock_log_returns_data.loc[common_dates]


# In[222]:


for date, daily_signals in signals.iterrows():
    if daily_signals.isna().all():
        portfolio_returns.append(0)
        continue

    daily_returns = stock_log_returns_data.loc[date]
    daily_portfolio_return = 0

    for ticker in list(positions.keys()):
        price = stock_prices.loc[date, ticker]
        if positions[ticker] > 0:  # Close long
            cash += positions[ticker] * price
        else:  # Close short
            cash -= abs(positions[ticker]) * price
        del positions[ticker]

    long_signals = daily_signals[daily_signals == 1].index
    short_signals = daily_signals[daily_signals == -1].index
    num_long = len(long_signals)
    num_short = len(short_signals)
    total_signals = num_long + num_short

    if total_signals > 0:
        capital_per_position = capital / total_signals

        # Open long positions
        for ticker in long_signals:
            price = stock_prices.loc[date, ticker]
            num_shares = capital_per_position / price 
            if num_shares > 0:
                positions[ticker] = num_shares
                cash -= num_shares * price
            daily_portfolio_return += positions.get(ticker, 0) * daily_returns[ticker]

        # Open short positions
        for ticker in short_signals:
            price = stock_prices.loc[date, ticker]
            num_shares = capital_per_position / price
            if num_shares > 0:
                positions[ticker] = -num_shares
                cash += num_shares * price
            daily_portfolio_return += positions.get(ticker, 0) * daily_returns[ticker]

    # Calculate portfolio value and daily return
    portfolio_value = cash + sum(positions.get(ticker, 0) * stock_prices.loc[date, ticker] for ticker in positions)
    daily_return = (portfolio_value - previous_portfolio_value) / previous_portfolio_value
    portfolio_returns.append(daily_return)
    previous_portfolio_value = portfolio_value


# In[223]:


portfolio_returns_df = pd.DataFrame(portfolio_returns, columns=["PortfolioReturn"], index=signals.index)
portfolio_returns_df['Cumulative Return'] = (1 + portfolio_returns_df['PortfolioReturn']).cumprod() - 1

sharpe = (portfolio_returns_df['PortfolioReturn'].mean() * np.sqrt(252)) / portfolio_returns_df['PortfolioReturn'].std()

print(f"Final Portfolio Value: {portfolio_value}")
print(f"Annualised Sharpe Ratio: {sharpe}")


# In[224]:


portfolio_returns_df["Cumulative Return"].plot(title="Cumulative Portfolio Return")

