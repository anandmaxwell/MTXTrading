import vectorbt as vbt
import pandas as pd

# Download multi-symbol price data
tickers = ['AAPL', 'MSFT']
price = vbt.YFData.download(tickers, period='6mo').get('Close')

# Run MACD
MACD = vbt.IndicatorFactory.from_talib('MACD')
MACD_Indicator = MACD.run(price, fastperiod=12, slowperiod=26, signalperiod=9)



macd_line = MACD_Indicator.macd
signal_line = MACD_Indicator.macdsignal
hist = MACD_Indicator.macdhist

# Define a custom indicator using IndicatorFactory
from vectorbt.indicators.factory import IndicatorFactory

def generate_signals(macd, signal, hist, close):
    # Ensure 2D DataFrame output
    buy = (macd > signal) &  (hist > 0) 
    sell = (macd < signal) &  (hist < 0)

    return buy.astype(int), sell.astype(int)

# Create the IndicatorFactory
SignalFactory = IndicatorFactory(
    input_names=['macd', 'signal', 'hist', 'close'],
    output_names=['buy', 'sell']
).from_apply_func(generate_signals)

# Run the indicator for multiple columns (symbols)
signals = SignalFactory.run(macd_line, signal_line, hist, price)

# Access 2D buy/sell signals
buy_signals = signals.buy  # DataFrame with same shape as `price`
sell_signals = signals.sell

print("Buy signals:")
print(buy_signals.tail())

print("Sell signals:")
print(sell_signals.tail())

portfolio = vbt.Portfolio.from_signals(
    close=price,
    entries=buy_signals,
    exits=sell_signals
)

print(portfolio.stats())