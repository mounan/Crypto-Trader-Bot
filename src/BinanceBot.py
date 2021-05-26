import requests
from time import time
import hmac
import hashlib
from utils import *


class BinanceBot:
    """[summary]
    """    

    def __init__(self, **kwargs):
        """[summary]
        """        
        super().__init__(**kwargs)
        self.__keys = process_yaml('../config.yaml')
        self.__secret_key = self.__keys['binance_api']['secret_key']
        self.__api_key = self.__keys['binance_api']['api_key']
        self.__base_url = 'https://api.binance.com'
        self.__headers = {'X-MBX-APIKEY': self.__api_key}
        print('='*100)
        print("₿ Your Binance bot is ready. Please give orders. Hail the Bitcoin! ₿")
        print('='*100)

    def timestamp_str(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """        
        return str(int(time()*1000))

    def signature(self, message):
        """[summary]

        :param message: [description]
        :type message: [type]
        :return: [description]
        :rtype: [type]
        """        
        return hmac.new(bytes(self.__secret_key, 'latin-1'), msg=bytes(message, 'latin-1'), digestmod=hashlib.sha256).hexdigest()

    def order_request(self, test, symbol, quantity, action=None,  price=None,):
        """[summary]

        :param test: [description]
        :type test: [type]
        :param symbol: [description]
        :type symbol: [type]
        :param quantity: [description]
        :type quantity: [type]
        :param action: [description], defaults to None
        :type action: [type], optional
        :param price: [description], defaults to None
        :type price: [type], optional
        :return: [description]
        :rtype: [type]
        """        
        test_str = '/test' if test else ''
        round_size = self.get_round_size(symbol)
        if not price:
            price = self.get_latest_price(symbol)
        price = round(price, round_size)
        post_par = f'symbol={symbol}&side={action}&quantity={quantity}&type=LIMIT&timeInForce=GTC&price={price}&recvWindow=1000&newOrderRespType=RESULT'
        ts = self.timestamp_str()
        post_par_with_ts = post_par+'&timestamp='+ts
        sign = self.signature(post_par_with_ts)
        test_trade_url = self.__base_url + \
            f'/api/v3/order{test_str}?{post_par_with_ts}&signature={sign}'
        return requests.post(test_trade_url, headers=self.__headers)

    def avg_price(self, symbol):
        """[summary]

        :param symbol: [description]
        :type symbol: [type]
        :return: [description]
        :rtype: [type]
        """        
        url = self.__base_url + f'/api/v3/avgPrice?&symbol={symbol}'
        return requests.get(url, headers=self.__headers).json()

    def book_ticker(self, symbol):
        """[summary]

        :param symbol: [description]
        :type symbol: [type]
        :return: [description]
        :rtype: [type]
        """        
        url = self.__base_url + f'/api/v3/ticker/bookTicker?&symbol={symbol}'
        return requests.get(url, headers=self.__headers).json()

    def get_latest_price(self, symbol):
        """[summary]

        :param symbol: [description]
        :type symbol: [type]
        :return: [description]
        :rtype: [type]
        """        
        return float(self.book_ticker(symbol)['askPrice'])

    def trade_history(self, symbol):
        """[summary]

        :param symbol: [description]
        :type symbol: [type]
        :return: [description]
        :rtype: [type]
        """        
        ts = self.timestamp_str()
        post_par_with_ts = 'symbol=' + symbol + '&timestamp=' + ts
        sign = self.signature(post_par_with_ts)
        url = self.__base_url + \
            f'/api/v3/myTrades?{post_par_with_ts}&signature={sign}'
        return requests.get(url, headers=self.__headers).json()

    def get_round_size(self, symbol):
        """[summary]

        :param symbol: [description]
        :type symbol: [type]
        :return: [description]
        :rtype: [type]
        """        
        resp = requests.get(
            f"https://api.binance.com/api/v3/exchangeInfo?symbol={symbol}")
        tick_size = resp.json()['symbols'][0]['filters'][0]['tickSize']
        return tick_size.find('1')-1
