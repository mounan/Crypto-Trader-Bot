from Exceptions import *
from time import *
from datetime import datetime
import requests
from utils import *
import inspect


class TwitterBot:
    """[summary]
    """        

    def __init__(self, screen_name, **kwargs):
        """[summary]

        :param screen_name: [description]
        :type screen_name: [type]
        """        
        super().__init__(**kwargs)
        self.__since_id = 0
        self.__screen_name = screen_name
        self.__base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        self.__keys = process_yaml('../config.yaml')
        self.__bearer_key = self.__keys['twitter_api']['bearer_key']
        print('='*100)
        print(
            f"The surveillance bot for @{screen_name} is ready. This is @{screen_name}'s latest tweet: ")
        pprint_dict(self.latest_cleaned_tweet())
        print("Please give the instructions")
        print('='*100)

    def _recent_tweets(self, count=1):
        """[summary]

        :param count: [description], defaults to 1
        :type count: int, optional
        :raises Exception: [description]
        :raises RequestException: [description]
        :return: [description]
        :rtype: [type]
        """        
        headers = {'Authorization': 'Bearer '+self.__bearer_key}
        url = f'{self.__base_url}?screen_name={self.__screen_name}&count={count}&tweet_mode=extended&include_rts=true'
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            if resp.json():
                return resp.json()
            else:
                raise Exception('Tweets not found.')
        else:
            raise RequestException(inspect.currentframe().f_code.co_name)

    def _latest_tweet(self):
        """[summary]

        :raises NoNewException: [description]
        :return: [description]
        :rtype: [type]
        """        
        if self.__since_id > 0:
            headers = {'Authorization': 'Bearer '+self.__bearer_key}
            url = f'{self.__base_url}?screen_name={self.__screen_name}&tweet_mode=extended&include_rts=true&exclude_replies=False&since_id={self.__since_id}&count=1'
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                if resp.json():
                    latest_tweet = resp.json()[0]
                    self.__since_id = latest_tweet['id']
                    return latest_tweet
                else:
                    raise NoNewException
            else:
                print(
                    f"Function '{inspect.currentframe().f_code.co_name}' requests failed, requesting agian.")
                return self._latest_tweet()
        elif self.__since_id == 0:
            try:
                latest_tweet = self._recent_tweets(count=1)[0]
            except Exception as e:
                print(e)
                return self._latest_tweet()
            else:
                self.__since_id = latest_tweet['id']
                return latest_tweet

    def _clean_tweet(self, tweet):
        """[summary]

        :param tweet: [description]
        :type tweet: [type]
        :return: [description]
        :rtype: [type]
        """        
        cleaned_tweet = {}
        cleaned_tweet['id'] = tweet['id']
        cleaned_tweet['created_at'] = tweet['created_at']
        cleaned_tweet['screen_name'] = tweet['user']['screen_name']
        cleaned_tweet['text'] = tweet['full_text']
        if 'media' in tweet['entities']:
            cleaned_tweet['media'] = []
            for m in tweet['entities']['media']:
                if 'media_url_https' in m:
                    cleaned_tweet['media'].append(m['media_url_https'])
        return cleaned_tweet

    def recent_cleaned_tweets(self, count):
        """[summary]

        :param count: [description]
        :type count: [type]
        :return: [description]
        :rtype: [type]
        """        
        raw_tweets = self._recent_tweets(count)
        cleaned_tweets = []
        for raw_tweet in raw_tweets:
            cleaned_tweets.append(self._clean_tweet(raw_tweet))
        return cleaned_tweets

    def latest_cleaned_tweet(self):
        """[summary]

        :raises e: [description]
        :return: [description]
        :rtype: [type]
        """        
        try:
            return self._clean_tweet(self._latest_tweet())
        except Exception as e:
            raise e

    def track_and_analyze(self, keywords):
        """[summary]

        :param keywords: [description]
        :type keywords: [type]
        """        
        while True:
            sleep(1)
            try: cleaned_tweet = self.latest_cleaned_tweet()
            except Exception as e: print(e)
            else:
                text = cleaned_tweet['text']
                if contains_either(text, keywords):
                    print('-'*80)
                    print('Text: '+clean_text(text))
                    analyze_sentiment(clean_text(text))
                else:
                    print('-'*80)
                    print('Text: '+clean_text(text))
                    print("##Couldn't find any keywords in this tweet##")

    def get_and_analyze(self, count, keywords=[]):
        """[summary]

        :param count: [description]
        :type count: [type]
        :param keywords: [description], defaults to []
        :type keywords: list, optional
        """        
        raw_tweets = self._recent_tweets(count=count)
        for raw_tweet in raw_tweets:
            text = self._clean_tweet(raw_tweet)['text']
            if contains_either(text, keywords):
                print('-'*70)
                print('Text: '+clean_text(text))
                analyze_sentiment(clean_text(text))
            else:
                print('-'*70)
                print('Text: '+clean_text(text))
                print("Couldn't find any keywords in this tweet")
