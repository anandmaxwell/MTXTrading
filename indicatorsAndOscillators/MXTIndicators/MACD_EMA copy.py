
import datetime
from os import close
import signal
from matplotlib.axis import XAxis
import vectorbt as vbt
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from dataLoader.YahooFinanceDataCollector import YahooFinanceDataCollector
pio.renderers.default='browser'  

class MACD_EMA():

    def __init__(self, ema_short_window: int = 121, ema_middle_window: int = 120, ema_long_window: int = 200):
        print(datetime.datetime.now(), "MACD_EMA init")
        self.ema_short_window = ema_short_window
        self.ema_middle_window = ema_middle_window
        self.ema_long_window = ema_long_window
        print(datetime.datetime.now(), "MACD_EMA init completed")

        
        
    def mtxIndicator(self, priceData, ema_short_window=12, ema_middle_window=120, ema_long_window=200):
        """
        Runs the MACD calculation on the provided price data.
        """
        print(datetime.datetime.now(), "MACD_EMA run started")
        close = priceData.get("Close")

        priceData.ta.macd(append=True)

        priceData.ta.ema(length=20, append=True)  

        priceData.ta.ema(length=120, append=True)    

        priceData.ta.ema(length=200, append=True)    

        priceData = priceData.dropna(subset=['EMA_20', 'EMA_120', 'EMA_200', 'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9'])

        priceData['Signal'] =0

        priceData.loc[
                (priceData['MACD_12_26_9'] > priceData['MACDs_12_26_9']) &
                (priceData['MACD_12_26_9'].shift(1) <= priceData['MACDs_12_26_9'].shift(1)) &
                (priceData['MACDh_12_26_9'] > 0) &
                (priceData['EMA_20'] > priceData['Close']) ,
        'Signal'] =1


        priceData.loc[
                (priceData['MACD_12_26_9'] < priceData['MACDs_12_26_9']) &
                (priceData['MACD_12_26_9'].shift(1) >= priceData['MACDs_12_26_9'].shift(1)) &
                (priceData['MACDh_12_26_9'] < 0) &
                (priceData['EMA_20'] < priceData['Close']) ,
        'Signal'] = -1

        singnal = priceData['Signal'].to_numpy()

        return signal
    
    def run(self, priceData, mtxIndicator=mtxIndicator):
        """
        Runs the MACD_EMA indicator on the provided price data.
        """
        ind = vbt.IndicatorFactory(
            class_name = "Combinations",
            short_name = "comb",
            input_names = ["priceData"],
            param_names = ["ema_short_window", "ema_middle_window", "ema_long_window"],
            output_names = ["mtxValue"]
            ).from_apply_func(
                    mtxIndicator,
                    ema_short_window=self.ema_short_window,
                    ema_middle_window=self.ema_middle_window,  
                    ema_long_window=self.ema_long_window
                    )
        
        res = ind.run(
                priceData,
                ema_short_window=self.ema_short_window,
                ema_middle_window=self.ema_middle_window,
                ema_long_window=self.ema_long_window
                )

    def plotIt(self, priceData):
        """        Plots the price data with MACD and EMAs using Plotly.
        """
        # --- Create Plotly Figure ---
        fig =  go.Figure(
            layout_yaxis_range=[min(priceData['Close']), max(priceData['Close'])]
        )

        fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                row_heights=[0.6, 0.4],
                subplot_titles=('Price Chart', 'MACD')
            )

            # Candlestick in Row 1
        fig.add_trace(go.Candlestick(
                x=priceData.index,
                open=priceData['Open'],
                high=priceData['High'],
                low=priceData['Low'],
                close=priceData['Close'],
                name='Price'
            ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=priceData.index,
            y=priceData['EMA_20'],
            line=dict(color='green', width=1.5, dash='dot'),  # Style as you like
            name='EMA 20'
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=priceData.index,
            y=priceData['EMA_120'],
            line=dict(color='orange', width=1.5, dash='dot'),  # Style as you like
            name='EMA 120'
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=priceData.index,
            y=priceData['EMA_200'],
            line=dict(color='red', width=2, dash='dot'),  # Style as you like
            name='EMA 200'
        ), row=1, col=1)

            # MACD Line in Row 2
        fig.add_trace(go.Scatter(
                x=priceData.index,
                y=priceData['MACD_12_26_9'],
                line=dict(color='blue', width=1),
                name='MACD'
            ), row=2, col=1)

            # Signal Line in Row 2
        fig.add_trace(go.Scatter(
                x=priceData.index,
                y=priceData['MACDs_12_26_9'],
                line=dict(color='red', width=1),
                name='Signal'
            ), row=2, col=1)

            # Histogram in Row 2
        fig.add_trace(go.Bar(
                x=priceData.index,
                y=priceData['MACDh_12_26_9'],
                name='Histogram',
                marker_color=[
                        'green' if val > 0 else 'red' for val in priceData['MACDh_12_26_9']
                ],
                opacity=0.5
            ), row=2, col=1)

        # Layout settings

        fig.update_xaxes( type='category',
            rangebreaks=[
                dict(bounds=["15:30", "09:15"], pattern="hour")
            ]
        )

        fig.update_layout(
            height=800,
            title='Candlestick + MACD Indicator',
            xaxis2_title='Date',
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
           
 
        )

        fig.show()
        
       
        
        # # Calculate EMAs
        # ema_short = vbt.IndicatorFactory.from_pandas_ta('ema').run(priceData, length=self.ema_short_window).ema
        # ema_middle = vbt.IndicatorFactory.from_pandas_ta('ema').run(priceData, length=self.ema_middle_window).ema
        # ema_long = vbt.IndicatorFactory.from_pandas_ta('ema').run(priceData, length=self.ema_long_window).ema
        
        # # Calculate MACD
        # macd = ema_short - ema_long
        # signal = macd.ewm(span=self.ema_middle_window, adjust=False).mean()
        
        # print(datetime.datetime.now(), "MACD_EMA run completed")
        # return 1
    
if __name__ == "__main__":
    # Example usage
    macd_ema = MACD_EMA(ema_short_window=12, ema_middle_window=120, ema_long_window=200)
    
    print(datetime.datetime.now(), "Testing MACD_EMA")
    print("This is a custom MACD_EMA indicator example using vectorbt.")    
    ticker ="SCODATUBES.NS" # 15-July chart is interesting
    #ticker ="BHEL.NS"
    period = "3d"
    interval = "1m"

    # yahooFinanceDataCollector = YahooFinanceDataCollector(ticker, period=period , interval = interval)
    # tickerDFPrice = yahooFinanceDataCollector.collectDate()
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=2)

    tickerDFPrice = vbt.YFData.download(
        ["BTC-USD","ETH-USD"],
        missing_index='drop',
        start=start_time,
        end=end_time,
        interval="1m").get("Close")

    macd_ema.run(tickerDFPrice)

    # macd_values = macd_ema.indicator(tickerDFPrice)
    # print(macd_values)
    print(datetime.datetime.now(), "MACD_EMA test completed")