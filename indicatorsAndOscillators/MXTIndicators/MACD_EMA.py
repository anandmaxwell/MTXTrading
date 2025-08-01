
import datetime
from os import close
import signal
from matplotlib.axis import XAxis
import pandas as pd
import vectorbt as vbt
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from dataLoader.YahooFinanceDataCollector import YahooFinanceDataCollector
pio.renderers.default='browser'  


def mtxIndicatorlogic( priceData : pd.DataFrame, ema_short_window=12, ema_middle_window=120, ema_long_window=200):
        df = priceData
        df = df.copy()
        df.ta.ema(length=20, append=True)
        df['Signal'] = df['EMA_20'] > df['Close']
        # self.full_df = df  # ⬅️ store the full DataFrame here
        return priceData
        # """
        # Runs the MACD calculation on the provided price data.
        # """
        # print(datetime.datetime.now(), "MACD_EMA run started")
        
        # priceData.ta.macd(append=True)

        # priceData.ta.ema(length=20, append=True)  

        # priceData.ta.ema(length=120, append=True)    

        # priceData.ta.ema(length=200, append=True)    

        # priceData = priceData.dropna(subset=['EMA_20', 'EMA_120', 'EMA_200', 'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9'])

        # priceData['Singal'] =0

        # priceData.loc[
        #         (priceData['MACD_12_26_9'] > priceData['MACDs_12_26_9']) &
        #         (priceData['MACD_12_26_9'].shift(1) <= priceData['MACDs_12_26_9'].shift(1)) &
        #         (priceData['MACDh_12_26_9'] > 0) &
        #         (priceData['EMA_20'] > priceData['Close']) ,
        # 'Signal'] =1


        # priceData.loc[
        #         (priceData['MACD_12_26_9'] < priceData['MACDs_12_26_9']) &
        #         (priceData['MACD_12_26_9'].shift(1) >= priceData['MACDs_12_26_9'].shift(1)) &
        #         (priceData['MACDh_12_26_9'] < 0) &
        #         (priceData['EMA_20'] < priceData['Close']) ,
        # 'Signal'] = -1

        # # singnal = priceData['Signal'].to_numpy()

        

        # return priceData


MTXIndicator = vbt.IndicatorFactory(
    class_name = "MTXIndicator",
    short_name = "comb",
    input_names = ["priceData"],
    param_names = ["ema_short_window", "ema_middle_window", "ema_long_window"],
    output_names = ["mtxValue"],
    ).from_apply_func(
        mtxIndicatorlogic,
        keep_pd=True                   
    )

class MACD_EMA:

    def __init__(self, ema_short_window: int = 121, ema_middle_window: int = 120, ema_long_window: int = 200):
        print(datetime.datetime.now(), "MACD_EMA init")
        self.ema_short_window = ema_short_window
        self.ema_middle_window = ema_middle_window
        self.ema_long_window = ema_long_window
        self.priceData = None
        print(datetime.datetime.now(), "MACD_EMA init completed")
    
    def run(self, priceData):
        
        res = MTXIndicator.run(
                priceData,
                ema_short_window=self.ema_short_window,
                ema_middle_window=self.ema_middle_window,
                ema_long_window=self.ema_long_window
                )

    
if __name__ == "__main__":
    macd_ema = MACD_EMA(ema_short_window=12, ema_middle_window=120, ema_long_window=200)
    
    print(datetime.datetime.now(), "Testing MACD_EMA")
    print("This is a custom MACD_EMA indicator example using vectorbt.")    
    ticker ="SCODATUBES.NS" # 15-July chart is interesting
    #ticker ="BHEL.NS"
    period = "3d"
    interval = "1m"

    yahooFinanceDataCollector = YahooFinanceDataCollector(ticker, period=period , interval = interval)
    tickerDFPrice = yahooFinanceDataCollector.collectDate()
    # end_time = datetime.datetime.now()
    # start_time = end_time - datetime.timedelta(days=2)

    # tickerDFPrice = vbt.YFData.download(
    #     ["BTC-USD","ETH-USD"],
    #     missing_index='drop',
    #     start=start_time,
    #     end=end_time,
    #     interval="1m").get()

    macd_ema.run(tickerDFPrice)
    
    # macd_values = macd_ema.indicator(tickerDFPrice)
    # print(macd_values)
    print(datetime.datetime.now(), "MACD_EMA test completed")