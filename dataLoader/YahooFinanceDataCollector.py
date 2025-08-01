# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 07:34:17 2025

@author: achuw
"""
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


import yfinance as yf

import pandas as pd

class YahooFinanceDataCollector:    
    
    def __init__(self, ticker , 
                 interval , 
                 period = 'none', 
                 startDate ='none' , 
                 endDate='none'):
        
        self.ticker = ticker
        self.interval = interval
        self.period = period
        self.startDate = startDate
        self.endDate = endDate

    

   #///////////////////////////////////////////////////////////
   #   Function for the collecting the data
   #///////////////////////////////////////////////////////////
    def collectDate(self):

        logger.info("Started downloading the data for " + self.ticker)

        priceData = yf.download(self.ticker,
                                period=self.period,
                                interval= self.interval, 
                                group_by='tickers',
                                auto_adjust='True')
        
        #.................................................
        #   Changing the index date Time to Indian Time
        #.................................................
        priceData.index =  priceData.index.tz_convert('Asia/Kolkata')

        
        print("This is the type of priceData" + str(type(priceData)))
        
        
        #.................................................
        # We got the company  infromation
        #.................................................
        tickerDF = pd.DataFrame(priceData)
        logger.info("This is the type of tickerDF" + str(type(tickerDF)))
        print("These are the column" )
        print( tickerDF.columns)
        
        #.................................................
        # Need to get only the  price
        #.................................................
        tickerDFPriceIfo = tickerDF[self.ticker]

        print("This is the type of tickerDFPriceIfo" + str(type(tickerDFPriceIfo)))

        logger.info("downloading the data is completed " + self.ticker)        
        logger.info("Total recorded fetched ----------->" + str(len(tickerDFPriceIfo)))

        return tickerDFPriceIfo
        
    
if __name__ == '__main__': 
    logger.info("WE are testing the code")                    
    # self-test code
    # When run for testing only
    ticker ="SCODATUBES.NS" # 15-July chart is interesting
    #ticker ="BHEL.NS"
    period = "3d"
    interval = "1m"
    # startdte ='2025-07-10'
    # endDate ='2025-07-11'


    #.................................................
    # Need to get only the  price
    #.................................................
    yahooFinanceDataCollector = YahooFinanceDataCollector(ticker, period=period , interval = interval)
    tickerDFPrice = yahooFinanceDataCollector.collectDate()
    print(tickerDFPrice)
