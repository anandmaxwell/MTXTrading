from indicators.candlePattern.CandleStickInfoGenerator import CandleStickInfoGenerator

from dataLoader.YahooFinanceDataCollector import YahooFinanceDataCollector


#/////////////////////////////////////////
# Input
#/////////////////////////////////////////
ticker ="BHEL.NS"
period = "1d"
interval = "1m"
startdte ='2025-07-10'
endDate ='2025-07-11'


#...................................................................................
# Need to get only the  price
#...................................................................................
yahooFinanceDataCollector = YahooFinanceDataCollector(ticker, period=period , interval = interval)
tickerDFPrice = yahooFinanceDataCollector.collectDate()

print(tickerDFPrice)

print(CandleStickInfoGenerator(tickerDFPrice).generateCandleStickInfo())