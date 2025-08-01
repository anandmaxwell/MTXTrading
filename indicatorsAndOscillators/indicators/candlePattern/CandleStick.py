
class CandleStick():

    def __init__(self, priceInfoRec):

        self.candleTrend=""
        self.type=""
        self.candleStrength=""
        self.candleBodyHeight=0
        self.upperWickLength=0
        self.lowerWickLength=0

        self.high = priceInfoRec.High
        self.low = priceInfoRec.Low
        self.open = priceInfoRec.Open
        self.close = priceInfoRec.Close

    def generateCandleStickDetails(self):
        print()

        self.__generateTrendDetail__()

        self.__calculateBodyHeight__()

        self.__calculateWickHeight__()

        self.__calculateRelativeStrenth__()

        self.__findCandleStickType__()

        return self

    #--------------------------------------------------
    #   Bullish or Bearish
    #--------------------------------------------------
    def __generateTrendDetail__(self):

        self.candleBodyHeight = self.high - self.low

        if self.open > self.close:
            self.candleTrend = "BEAR"
        elif self.close > self.open:
            self.candleTrend = "BULL"
        else:
            self.candleTrend = "NONE"
        print()
    
    #--------------------------------------------------
    #   Calculating Body Height
    #--------------------------------------------------
    
    def __calculateBodyHeight__(self):
        if self.candleTrend == "BULL":
            self.bodyHeight = self.close - self.open
        elif self.candleTrend == "BEAR":
            self.bodyHeight = self.open - self.close
        else:
            self.bodyHeight = 0
        print()
    
    #--------------------------------------------------
    #   Calculating wick Height
    #--------------------------------------------------
    
    def __calculateWickHeight__(self):
        if self.candleTrend == "BULL":
            self.upperWickLength = self.high - self.close
            self.lowerWickLength = self.open - self.low
        elif self.candleTrend == "BEAR":
            self.upperWickLength = self.high - self.open
            self.lowerWickLength = self.close - self.low

    #--------------------------------------------------
    #   Calculating relative Strenght
    #--------------------------------------------------
    
    def __calculateRelativeStrenth__(self):
        bodyWeight = (self.bodyHeight / self.candleBodyHeight) * 100
        pressure = 0
        if self.candleTrend == "BULL":
            pressure = self.lowerWickLength / 100
        elif self.candleTrend == "BEAR":
            pressure = self.upperWickLength / 100

        self.candleStrength = bodyWeight + pressure

    #--------------------------------------------------
    #   Calculating relative Strenght
    #--------------------------------------------------
    
    def __findCandleStickType__(self):
        if 100 >= self.candleStrength and self.candleStrength  <85:
            self.type ="MAROBOJU"
        elif 85 >= self.candleStrength and self.candleStrength  <50:
            self.type ="STRONG"
        elif 50 >= self.candleStrength and self.candleStrength  <30:
            self.type ="MEDIUM"
        elif 30 >= self.candleStrength and self.candleStrength  <10:
            self.type ="LOW"
        elif 10 >= self.candleStrength and self.candleStrength  <0:
            self.type ="DOJI"
        print()

    
            


