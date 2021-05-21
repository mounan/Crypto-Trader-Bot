from TwitterBot import TwitterBot
from utils import *
from BinanceBot import BinanceBot

# tb = TwitterBot("elonmusk")
# keywords = ["BTC", "DOGE", 'crypto', 'bitcoin', 'coin', 'decentralize', 'hash']
# tb.get_and_analyze(30, keywords)

# bnb = BinanceBot()
# symbol = "DOGEBTC"
# pprint_dict(bnb.avg_price(symbol))
# latest_ask_price = bnb.book_ticker(symbol)['askPrice']
# print(latest_ask_price)


class CryptoBot(TwitterBot, BinanceBot):
    """A bot does Binance trades which can be triggered by Twitter user's tweet like @elonmusk. 
    """
    def __init__(self, screen_name, **kwargs):
        """Construct a CryptoBot with screen name of a twitter user

        Args:
            screen_name (str): Screen name of the twitter user you want to track
        """   
        super().__init__(screen_name, **kwargs)
        

    @property
    def keywords(self):
        return self.__keywords
    
    @keywords.setter
    def keywords(self, keywords:list):
        if not isinstance(keywords, list):
            raise TypeError('keywords must be a list of string')
        if not keywords and not isinstance(keywords[0], str):
            raise TypeError('keywords must contain strings')
        self.__keywords = keywords


    def track_and_analyze(self):
        return super().track_and_analyze(self.__keywords)
    
    def get_and_analyze(self, count):
        return super().get_and_analyze(count, self.__keywords)

    def trade_by_tweeting(self, symbol:str, action:str, quantity:int, price=None, auto_price=False, with_sentiment_analysis=False,):
        keywords = self.__keywords
        if auto_price:
            pass


# cb = CryptoBot("elonmusk")
# cb.keywords = ['doge', 'btc', 'bitcoin', 'egod', 'crypto', 'decentral']
# print(cb.avg_price("DOGEBTC"))
# cb.test()




