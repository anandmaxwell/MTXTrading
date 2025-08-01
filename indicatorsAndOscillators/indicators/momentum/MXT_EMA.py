

import datetime
import vectorbt as vbt
import pandas as pd

class MXT_EMA():
    """
    Custom RSI class that extends vectorbt's RSI to include additional functionality.
    """

    def __init__(self,  window: int =14 ):
        print(datetime.datetime.now(), "MXTRSI init")
        self.window = window
        print(datetime.datetime.now(), "MXT_EMA init completed")
  
    def getInputParams(self):
        """
        Returns the input parameters for the RSI calculation.
        """
        input_params_name = "window"
        return input_params_name
    
    def run(self, priceData):
        """
        Runs the RSI calculation on the provided price data.
        """
        print(datetime.datetime.now(), "indicator run started")
        ema = vbt.IndicatorFactory.from_pandas_ta('ema').run(priceData, length=self.window).ema
        print(datetime.datetime.now(), "indicator run completed")
        return ema
    
if __name__ == "__main__":
    # Example usage
    rsi = MXT_EMA(window=14)
    input_params_names = rsi.getInputParams()
    
    print(f"Input parameters: {input_params_names}")
    print(datetime.datetime.now(), "Testing MXT_EMA")
    print("This is a custom RSI indicator example using vectorbt.")    
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=2)
    
    btc_price = vbt.YFData.download(
        ["BTC-USD","ETH-USD"],
        missing_index='drop',
        start=start_time,
        end=end_time,
        interval="1m").get("Close")

    ema_values = rsi.run(btc_price)
    print(ema_values)
    print(datetime.datetime.now(), "MXT_EMA test completed")