
import logging
logger = logging.getLogger(__name__)

import numpy
from indicators.candlePattern.CandleStick import CandleStick

class CandleStickInfoGenerator():

    def __init__(self, priceInfoDF):
        self.priceInfoDF = priceInfoDF

    def generateCandleStickInfo(self):

        logger.info("Generating ")

        self.priceInfoDF.loc[:, 'candleTrend'] = 100
        self.priceInfoDF.loc[:, 'type'] = numpy.nan

        self.priceInfoDF.loc[:, 'candleStrength'] = 0
        self.priceInfoDF.loc[:, 'candleBodyHeight'] = 0
        self.priceInfoDF.loc[:, 'upperWickLength'] = 0
        self.priceInfoDF.loc[:, 'lowerWickLength'] = 0

        for index, priceInfo in self.priceInfoDF.iterrows():        
            candleStick = CandleStick(priceInfo).generateCandleStickDetails()
            self.priceInfoDF['candleTrend'] = candleStick.candleTrend
            self.priceInfoDF['type'] = candleStick.type
            self.priceInfoDF['candleStrength'] = candleStick.candleStrength
            self.priceInfoDF['candleBodyHeight'] = candleStick.candleBodyHeight
            self.priceInfoDF['upperWickLength'] = candleStick.upperWickLength
            self.priceInfoDF['lowerWickLength'] = candleStick.lowerWickLength

        return self.priceInfoDF

