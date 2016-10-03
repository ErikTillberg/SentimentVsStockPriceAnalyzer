#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Import mongoDB
from pymongo import MongoClient

from alchemy_sentiment import get_sentiment_score_from_text

import json

import threading
import pickle
from time import sleep
import signal
import sys

#Variables that contains the user credentials to access Twitter API

access_token =
access_token_secret =
consumer_key =
consumer_secret =

client = MongoClient()
db = client.TwitterData

keywords = []

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, searchTerm):
        self.searchTerm = searchTerm

    def on_data(self, data):
        tweet = json.loads(data)
        #try:
            #tweet['sentiment'] = get_sentiment_score_from_text(tweet['text'] , '')
            #print tweet['sentiment']
        #except:
            #print 'Could not gather sentiment from text'
        collection = db[self.searchTerm]
        collection.insert_one(tweet)
        print tweet['text'].encode('utf-8')
        return True

    def on_error(self, status):
        print status

class TweetFetcher:

    fetchers = []

    def __init__(self, searchTerm, extraTerms):
        TweetFetcher.fetchers.append(self)
        self.searchTerm = searchTerm
        self.extraTerms = extraTerms

    def startTwitterSearch(self):
        l = StdOutListener(self.searchTerm)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, l)
        self.stream.filter(track = ([self.searchTerm]+self.extraTerms), async = True)

        #self.t = threading.Thread(target=stream.filter, kwargs={'track':[self.searchTerm], 'async':True})
        #self.t.start()
    def stopSearch(self):
        self.stream.disconnect()

if __name__ == '__main__':

    def ctrlCHandler(signal, frame):
        print 'exiting'
        for i in range(0, len(TweetFetcher.fetchers)):
            TweetFetcher.fetchers[i].stopSearch()
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrlCHandler)

    t = TweetFetcher('microsoft', ['windows 10'])
    t.startTwitterSearch()
    #t1 = TweetFetcher('microsoft')
    #t1.startTwitterSearch()

    while True:
        sleep(0.1)
