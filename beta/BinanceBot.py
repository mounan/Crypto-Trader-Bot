import requests
from time import time
import hmac
import hashlib
from utils import *

class BinanceBot:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__keys = process_yaml('../config.yaml')
        self.__secret_key = self.__keys['binance_api']['secret_key']
        self.__api_key = self.__keys['binance_api']['api_key']
        self.__base_url = 'https://api.binance.com'
        self.__headers = {'X-MBX-APIKEY':self.__api_key}
        print("₿"*70)
        print("|| Your Binance bot is ready. Please give orders. Hail the Bitcoin! ||")
        print("₿"*70)
        
    def timestamp_str(self):
        return str(int(time()*1000))

    def signature(self, message):
        return hmac.new(bytes(self.__secret_key , 'latin-1'), msg = bytes(message , 'latin-1'), digestmod = hashlib.sha256).hexdigest()

    def trade_request(self, post_par):
        ts = self.timestamp_str()
        post_par_with_ts = post_par+'&timestamp='+ts
        sign = self.signature(post_par_with_ts) 
        test_trade_url = self.__base_url + f'/api/v3/order?{post_par_with_ts}&signature={sign}'
        return requests.post(test_trade_url, headers=self.__headers)

    def trade(self, symbol, action, quantity):
        pass

    def avg_price(self, symbol):
        url = self.__base_url + f'/api/v3/avgPrice?&symbol={symbol}'
        return requests.get(url, headers=self.__headers).json()
    
    def book_ticker(self, symbol):
        url = self.__base_url + f'/api/v3/ticker/bookTicker?&symbol={symbol}'
        return requests.get(url, headers=self.__headers).json()

    def trade_history(self, symbol):
        ts = self.timestamp_str()
        post_par_with_ts = 'symbol=' + symbol + '&timestamp=' + ts
        sign = self.signature(post_par_with_ts) 
        url = self.__base_url + f'/api/v3/myTrades?{post_par_with_ts}&signature={sign}'
        return requests.get(url, headers=self.__headers).json()