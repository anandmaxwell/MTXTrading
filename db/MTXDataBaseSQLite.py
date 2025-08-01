import vectorbt as vbt
import pandas as pd
import numpy as np
import sqlite3

# Simulate sample price data
price = pd.Series(np.random.rand(100) * 100 + 100)

# Dummy strategy: Buy if price > yesterday's price, sell otherwise
buy_signals = price > price.shift(1)
sell_signals = price < price.shift(1)

# Run portfolio backtest
portfolio = vbt.Portfolio.from_signals(
    close=price,
    entries=buy_signals,
    exits=sell_signals,
    init_cash=10000
)

# Get total return
total_return = portfolio.total_return()

# ✅ Store to SQLite
conn = sqlite3.connect('MTXTrading.db')
df = pd.DataFrame({'strategy': ['basic_momentum'], 'total_return': [total_return]})

# Save to table named "results"
df.to_sql('results', conn, if_exists='append', index=False)

conn.close()

if __name__ == "__main__":
    print("Backtest complete. Results stored in MTXTrading.db")
    print(df)   
