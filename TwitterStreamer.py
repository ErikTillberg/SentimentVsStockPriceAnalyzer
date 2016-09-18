#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Import mongoDB
from pymongo import MongoClient

import json

import threading

from time import sleep
import signal
import sys

#Variables that contains the user credentials to access Twitter API
access_token = "307572680-a6YbnrmtRf93c3QSBKWwJIy7t4xpvtUXBAsy60Ds"
access_token_secret = "ChU5dC8rHj3WGrTnTOpBvBuRksYJimIU1xYkHR3UbezhU"
consumer_key = "WbUsbhL6bVlnukhWaHevAgDRO"
consumer_secret = "NF97BBUFmqyr6xJUF0aIk4Rnyl0SHNkPkyaDPZSOHIpjCnXZ7Z"

client = MongoClient()
db = client.TwitterData

keywords = []

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, searchTerm):
        self.searchTerm = searchTerm

    def on_data(self, data):
        tweet = json.loads(data)
        print data
        collection = db[self.searchTerm]
        collection.insert_one(tweet)
        return True

    def on_error(self, status):
        print status

class TweetFetcher:

    fetchers = []
    
    def __init__(self, searchTerm):
        TweetFetcher.fetchers.append(self)
        self.searchTerm = searchTerm
        
    def startTwitterSearch(self):
        l = StdOutListener(self.searchTerm)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, l)
        self.stream.filter(track = [self.searchTerm], async = True)
        
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
    
    t = TweetFetcher('microsoft')
    t.startTwitterSearch()
    t1 = TweetFetcher('apple')
    t1.startTwitterSearch()

    while True:
        sleep(0.1)
