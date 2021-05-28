from TwitterBot import TwitterBot
from utils import *
from BinanceBot import BinanceBot
from time import *


class AutoTrader(TwitterBot, BinanceBot):
    """[summary]

    :param TwitterBot: [description]
    :type TwitterBot: [type]
    :param BinanceBot: [description]
    :type BinanceBot: [type]
    """

    def __init__(self, screen_name, **kwargs):
        """[summary]

        :param screen_name: [description]
        :type screen_name: [type]
        """
        super().__init__(screen_name, **kwargs)

    @property
    def keywords(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self.__keywords

    @keywords.setter
    def keywords(self, keywords: list):
        """[summary]

        :param keywords: [description]
        :type keywords: list
        :raises TypeError: [description]
        :raises TypeError: [description]
        """
        if not isinstance(keywords, list):
            raise TypeError('keywords must be a list of string')
        if not keywords and not isinstance(keywords[0], str):
            raise TypeError('keywords must contain strings')
        self.__keywords = keywords

    def track_and_analyze(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return super().track_and_analyze(self.__keywords)

    def get_and_analyze(self, count):
        """[summary]

        :param count: [description]
        :type count: [type]
        :return: [description]
        :rtype: [type]
        """
        return super().get_and_analyze(count, self.__keywords)

    def order_by_tweets(self, test: bool, symbol: str, quantity: int, growth_rate=None, auto_price=False, timeout=5, with_sentiment_analysis=False,):
        """[summary]

        :param test: [description]
        :type test: bool
        :param symbol: [description]
        :type symbol: str
        :param quantity: [description]
        :type quantity: int
        :param growth_rate: [description], defaults to None
        :type growth_rate: [type], optional
        :param auto_price: [description], defaults to False
        :type auto_price: bool, optional
        :param timeout: [description], defaults to 5
        :type timeout: int, optional
        :param with_sentiment_analysis: [description], defaults to False
        :type with_sentiment_analysis: bool, optional
        :return: [description]
        :rtype: [type]
        """

        keywords = self.__keywords

        if auto_price:
            growth_rate = 0.08
        elif not growth_rate:
            print("Please set the growth rate or set auto_price to True.")
            return False

        try:
            while True:
                sleep(1)
                try:
                    t = self.latest_cleaned_tweet()
                except Exception as e:
                    print(e, end="\r")
                else:
                    text = t['text']
                    if contains_either(text, keywords):
                        print('-'*80)
                        print('Ordered by this tweet:')
                        print('Text: '+clean_text(text))
                        buy_price = self.get_latest_price(symbol)
                        buy_resp = self.order_request(
                            test, symbol, quantity, price=buy_price, action="BUY")
                        sleep(1.5)
                        if buy_resp.status_code == 200:
                            sell_price = buy_price * (1+growth_rate)
                            sell_resp = self.order_request(
                                test, symbol, quantity, price=sell_price, action="SELL")
                            pprint_json(buy_resp.json())
                            pprint_json(sell_resp.json())
                    else:
                        print('-'*80)
                        print('Text: '+clean_text(text))
                        print("## Couldn't find any keywords in this tweet ##")
                        print('-'*80)
        except: 
            print("")
            print("[ Program terminated. ]")
