
import datetime
import signal
import vectorbt as vbt
import pandas_ta as ta
import pandas as pd
import numpy as np


from dataLoader.YahooFinanceDataCollector import YahooFinanceDataCollector

class MACD_EMA:

    def __init__(self):        
        
        print(datetime.datetime.now(), "MACD_EMA initialized")

        self.ema_short_window = 20
        self.ema_middle_window = 120
        self.ema_long_window = 200

        self.macd_fastperiod = 12
        self.macd_slowperiod = 26
        self.macd_signalperiod = 9
        
        self.originalPricedata= pd.DataFrame
        self.calculatedPricedata = pd.DataFrame

    def mtxIndicatorlogic(self, 
                          orignalPriceData , 
                          ema_short_window=12, 
                          ema_middle_window=120, 
                          ema_long_window=200,
                          macd_fastperiod=12,
                          macd_slowperiod=26,
                          macd_signalperiod=9):
        
        priceData = orignalPriceData.copy()
        self.originalPricedata = orignalPriceData
        

        MACD = vbt.IndicatorFactory.from_talib('MACD')
        MACD_Indicator = MACD.run(priceData['Close'], fastperiod=macd_fastperiod, slowperiod=macd_slowperiod, signalperiod=macd_signalperiod)

        macd_line = MACD_Indicator.macd
        signal_line = MACD_Indicator.macdsignal
        histogram = MACD_Indicator.macdhist

        print(macd_line, signal_line, histogram)
        # """
        # Runs the MACD calculation on the provided price data.
        # """
        print(datetime.datetime.now(), "MACD_EMA run started")

        EMA_SHORT = vbt.IndicatorFactory.from_talib('EMA')

        EMA_SHORT_Result = EMA_SHORT.run(priceData['Close'], ema_short_window).real

        priceData['Signal'] = 0

        buy = (macd_line >  signal_line) & (macd_line.shift(1) <= signal_line.shift(1)) & (histogram > 0) & (priceData['Close'] > EMA_SHORT_Result)
        
        sell = (macd_line <  signal_line) & (macd_line.shift(1) >= signal_line.shift(1)) & (histogram < 0) & (priceData['Close'] < EMA_SHORT_Result)
        

        # priceData.loc[
        #         (macd_line >  signal_line) &
        #         (macd_line.shift(1) <= signal_line.shift(1)) &
        #         (histogram > 0) &
        #        (priceData['Close'] > EMA_SHORT_Result),
        # 'Signal'] =1

        # priceData.loc[
        #         (macd_line <  signal_line) &
        #         (macd_line.shift(1) >= signal_line.shift(1)) &
        #         (histogram < 0) &
        #        (priceData['Close'] < EMA_SHORT_Result),
        # 'Signal'] = -1
        
        # priceData.ta.macd(append=True)

        # priceData.ta.ema(length=20, append=True)  

        # priceData.ta.ema(length=120, append=True)    

        # priceData.ta.ema(length=200, append=True)    

        # #priceData = priceData.dropna(subset=['EMA_20', 'EMA_120', 'EMA_200', 'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9'])

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

        # self.calculatedPricedata = priceData

        return buy.astype(int), sell.astype(int)

# ---- Step 2: Define IndicatorFactory class ---- #
    MACD_EMA_Indicator = vbt.IndicatorFactory(
        class_name="MACD_EMA_Indicator",
        short_name="macdema",
        input_names=["self","priceData"],
        param_names=["ema_short_window", "ema_middle_window", "ema_long_window","macd_fastperiod", "macd_slowperiod", "macd_signalperiod"],
        output_names=["buy","sell"]
    ).from_apply_func(
        mtxIndicatorlogic,
        keep_pd=True,
        param_product=True
    )        

        # return priceData

    def run(self, priceData):

        # priceData['Signal'] = 0

        result = self.MACD_EMA_Indicator.run(
            self,
            priceData.get('Close', priceData),  # Use 'Close' column for MACD calculation
            ema_short_window=self.ema_short_window,
            ema_middle_window=self.ema_middle_window,
            ema_long_window=self.ema_long_window,

            macd_fastperiod=self.macd_fastperiod,
            macd_slowperiod=self.macd_slowperiod,
            macd_signalperiod=self.macd_signalperiod       
        )
        buy_signals = result.buy  # DataFrame with same shape as `price`
        sell_signals = result.sell

        portfolio = vbt.Portfolio.from_signals(
            close=priceData.get('Close', priceData),
            entries=buy_signals,
            exits=sell_signals
        )
        print(portfolio.total_return().to_string())
        return result

# ---- Step 4: Testing ---- #
if __name__ == "__main__":
    print(datetime.datetime.now(), "Testing MACD_EMA...")

    print(datetime.datetime.now(), "Testing MACD_EMA")
    print("This is a custom MACD_EMA indicator example using vectorbt.")    
    ticker ="SCODATUBES.NS" # 15-July chart is interesting
    #ticker ="BHEL.NS"
    period = "3d"
    interval = "1m"

    yahooFinanceDataCollector = YahooFinanceDataCollector(ticker, period=period , interval = interval)
    tickerDFPrice = yahooFinanceDataCollector.collectDate()
    
    macd_ema = MACD_EMA()
    macd_ema.ema_short_window = [20,30,40,50,60,70,80,90,100]
    macd_ema.macd_fastperiod = [12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    result = macd_ema.run(tickerDFPrice)
    # print(result.signal.to_string())
    print(datetime.datetime.now(), "MACD_EMA testing completed")

