import math
class MarketTrendAnalyzer:  
    def __init__(self, priceInfoDF):
        self.priceInfoDF = priceInfoDF
        self.trend = None
        self.trendStrength = None
        self.trendDuration = None
        

    def analyzeMarketTrend(self):
        self.__calculateTrend__()
        self.__calculateTrendStrength__()
        self.__calculateTrendDuration__()

        return {
            'trend': self.trend,
            'trendStrength': self.trendStrength,
            'trendDuration': self.trendDuration
        }
    
    def __calculateTrend__(self):
    

