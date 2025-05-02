import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "MNG.L"
time_period = "2y"

price_data = yf.download(ticker, period=time_period, auto_adjust=False)["Close"]
dividend_data = yf.Ticker(ticker).dividends

price_data.index = pd.to_datetime(price_data.index).tz_localize(None)
dividend_data.index = pd.to_datetime(dividend_data.index).tz_localize(None)
dividend_data = dividend_data.loc[price_data.index[0]:]

price_dividend_df = pd.concat([price_data,dividend_data], axis=1)
price_dividend_df = price_dividend_df.fillna(0.00)

price_dividend_df["UnadjustedPct"] = price_dividend_df[ticker].pct_change()

# Initialize the Adjustment column with 1s
price_dividend_df["Adjustment"] = 1.0

# List to store the daily a_d values (single-day adjustments)
daily_adjustments = [1.0]  # A_0 is 1

for i in range(1, len(price_dividend_df)):
    dividend = price_dividend_df.iloc[i]["Dividends"]
    prev_close = price_dividend_df.iloc[i - 1][ticker]

    if prev_close == 0:
        daily_adjustments.append(1.0)  # Avoid error, assume no adjustment
        continue

    # a_d = S_d / (1 - D_d / C_{d-1}); assuming S_d = 1 unless specified
    one_day_adj = 1 / (1 - dividend / prev_close)

    # Multiply previous adjustment by today's a_d to get cumulative A_d
    cumulative_adj = daily_adjustments[-1] * one_day_adj

    daily_adjustments.append(cumulative_adj)

# Assign the forward adjustment factor A_d to the DataFrame
price_dividend_df["Adjustment"] = daily_adjustments

price_dividend_df["AdjustedPrices"] = price_dividend_df[ticker]
for i in range(1,len(price_dividend_df)):
    price_dividend_df.at[price_dividend_df.index[i], "AdjustedPrices"] = price_dividend_df.at[price_dividend_df.index[i], ticker] * price_dividend_df.at[price_dividend_df.index[i], "Adjustment"]

price_dividend_df["AdjustedPct"] = price_dividend_df["AdjustedPrices"].pct_change()
df = price_dividend_df[["AdjustedPct","UnadjustedPct"]]
df = df.dropna()

df["CumAdj"] = (1 + df["AdjustedPct"]).cumprod()
df["CumUnadj"] = (1 + df["UnadjustedPct"]).cumprod()

plt.figure(figsize=(10, 6))
plt.plot(df["CumAdj"], label="Cumulative Adjusted Return")
plt.plot(df["CumUnadj"], label="Cumulative Unadjusted Return")
plt.title("Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()