from google.cloud import language_v1
from time import time
from time import sleep
import emoji
import yaml
import requests
import json
import re
from google.oauth2 import service_account
from utils import *


class TwitterBot:

    def __init__(self, screen_name, **kwargs):
        super().__init__(**kwargs)
        self.__since_id = 0
        self.__screen_name = screen_name
        self.__base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        self.__keys = process_yaml('../config.yaml')
        self.__bearer_key = self.__keys['twitter_api']['bearer_key']
        print('='*80)
        print(
            f"The surveillance bot for @{screen_name} is ready. This is @{screen_name}'s latest tweet: ")
        self.pprint_tweet(self.latest_cleaned_tweet())
        print("Please give the instructions")
        print('='*80)

    def _latest_tweets(self, count=1):
        headers = {'Authorization': 'Bearer '+self.__bearer_key}
        url = f'{self.__base_url}?screen_name={self.__screen_name}&count={count}&tweet_mode=extended&include_rts=true'
        resp = requests.get(url, headers=headers)
        return resp.json()

    def _clean_tweet(self, tweet):
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

    def latest_cleaned_tweets(self, count):
        tweets = self._latest_tweets(count)
        cleaned_tweets = []
        for tweet in tweets:
            cleaned_tweets.append(self._clean_tweet(tweet))
        return cleaned_tweets

    def latest_cleaned_tweet(self):
        if len(tweets := self._latest_tweets()):
            tweet = tweets[0]
            tweet = self._clean_tweet(tweet)
            if tweet['id'] <= self.__since_id:
                return False
            self.__since_id = tweet['id']
            return tweet
        else:
            sleep(1)
            return self.latest_cleaned_tweet()

    def pprint_tweet(self, cleaned_tweet):
        pprint_dict(cleaned_tweet)

    def track_and_analyze(self, keywords):
        while True:
            sleep(1)
            if t := self.latest_cleaned_tweet():
                text = t['text']
                if contains_either(text, keywords):
                    print('-'*80)
                    print('Text: '+clean_text(text))
                    analyze_sentiment(clean_text(text))
                else:
                    print('-'*80)
                    print('Text: '+clean_text(text))
                    print("##Couldn't find the keywords in this tweet##")

    def get_and_analyze(self, count, keywords=[]):
        tweets = self.latest_cleaned_tweets(count=count)
        for tweet in tweets:
            text = tweet['text']
            if contains_either(text, keywords):
                print('-'*70)
                print('Text: '+clean_text(text))
                analyze_sentiment(clean_text(text))
            else:
                print('-'*70)
                print('Text: '+clean_text(text))
                print("Couldn't find the keywords in this tweet")
