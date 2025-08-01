import datetime
import vectorbt as vbt
import pandas_ta as ta
import pandas as pd
import numpy as np

# ---- Step 1: Indicator function (outside the class) ---- #
def mtx_indicator(priceData: pd.DataFrame, ema_short_window: int, ema_middle_window: int, ema_long_window: int):
    priceData = priceData.copy()
    priceData.ta.macd(append=True)
    priceData.ta.ema(length=ema_short_window, append=True)
    priceData.ta.ema(length=ema_middle_window, append=True)
    priceData.ta.ema(length=ema_long_window, append=True)

    required_cols = [
        f'EMA_{ema_short_window}', f'EMA_{ema_middle_window}', f'EMA_{ema_long_window}',
        'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9'
    ]
    priceData = priceData.dropna(subset=required_cols)

    priceData['Signal'] = 0
    priceData.loc[
        (priceData['MACD_12_26_9'] > priceData['MACDs_12_26_9']) &
        (priceData['MACD_12_26_9'].shift(1) <= priceData['MACDs_12_26_9'].shift(1)) &
        (priceData['MACDh_12_26_9'] > 0) &
        (priceData[f'EMA_{ema_short_window}'] > priceData['Close']),
        'Signal'
    ] = 1

    priceData.loc[
        (priceData['MACD_12_26_9'] < priceData['MACDs_12_26_9']) &
        (priceData['MACD_12_26_9'].shift(1) >= priceData['MACDs_12_26_9'].shift(1)) &
        (priceData['MACDh_12_26_9'] < 0) &
        (priceData[f'EMA_{ema_short_window}'] < priceData['Close']),
        'Signal'
    ] = -1

    return priceData['Signal'].to_numpy()

# ---- Step 2: Define IndicatorFactory class ---- #
MACD_EMA_Indicator = vbt.IndicatorFactory(
    class_name="MACD_EMA_Indicator",
    short_name="macdema",
    input_names=["priceData"],
    param_names=["ema_short_window", "ema_middle_window", "ema_long_window"],
    output_names=["signal"]
).from_apply_func(
    mtx_indicator
)

# ---- Step 3: Wrapper Class ---- #
class MACD_EMA:

    def __init__(self, ema_short_window=20, ema_middle_window=120, ema_long_window=200):
        print(datetime.datetime.now(), "MACD_EMA initialized")
        self.ema_short_window = ema_short_window
        self.ema_middle_window = ema_middle_window
        self.ema_long_window = ema_long_window

    def run(self, priceData):
        result = MACD_EMA_Indicator.run(
            priceData,
            ema_short_window=self.ema_short_window,
            ema_middle_window=self.ema_middle_window,
            ema_long_window=self.ema_long_window
        )
        return result


# ---- Step 4: Testing ---- #
if __name__ == "__main__":
    print(datetime.datetime.now(), "Testing MACD_EMA...")

    ticker = "RELIANCE.NS"
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=2)

    priceData = vbt.YFData.download(
        ticker,
        start=start_time,
        end=end_time,
        interval="1m",
        missing_index='drop'
    ).get()

    macd_ema = MACD_EMA(ema_short_window=20, ema_middle_window=120, ema_long_window=200)
    result = macd_ema.run(priceData)

    print(result.signal.tail())

    print(datetime.datetime.now(), "MACD_EMA test completed")
