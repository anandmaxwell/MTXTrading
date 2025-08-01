

import datetime
import vectorbt as vbt
import pandas as pd

class MXT_RSI():
    """
    Custom RSI class that extends vectorbt's RSI to include additional functionality.
    """

    def __init__(self,  window: int =14 ):
        print(datetime.datetime.now(), "MXTRSI init")
        self.window = window
        print(datetime.datetime.now(), "MXTRSI init completed")
  
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
        print(datetime.datetime.now(), "RSI run started")
        rsi = vbt.RSI.run(priceData, window=self.window ,)
        ema_20 = vbt.IndicatorFactory.from_pandas_ta('ema').run(priceData, length=20).ema
        
        print(datetime.datetime.now(), "RSI run completed")
        return rsi
    
if __name__ == "__main__":
    # Example usage
    rsi = MXT_RSI(window=14)
    input_params_names = rsi.getInputParams()
    
    print(f"Input parameters: {input_params_names}")
    print(datetime.datetime.now(), "Testing MXTRSI")
    print("This is a custom RSI indicator example using vectorbt.")    
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=2)
    
    btc_price = vbt.YFData.download(
        ["BTC-USD","ETH-USD"],
        missing_index='drop',
        start=start_time,
        end=end_time,
        interval="1m").get("Close")

    rsi_values = rsi.run(btc_price).rsi
    print(rsi_values)
    print(datetime.datetime.now(), "MXTRSI test completed")