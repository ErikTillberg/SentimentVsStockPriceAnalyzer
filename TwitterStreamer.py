#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Import mongoDB
from pymongo import MongoClient

from alchemy_sentiment import get_sentiment_score_from_text

import json

import threading
import logging
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

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, searchTerm):
        self.searchTerm = searchTerm
        self._logger = logging.getLogger(__name__)
    
    def on_data(self, data):
        try:
            tweet = json.loads(data)
            #
            collection = db[self.searchTerm]
            collection.insert_one(tweet)
            #
            print tweet['text'].encode('utf-8')
            #
            '''
            try:
                tweet['sentiment'] = get_sentiment_score_from_text(tweet['text'] , '')
                print tweet['sentiment']
            except:
                self._logger.exception('Could not gather sentiment from text.')
            '''
            #
            if tweet['filter_level'] != 'low':
                self._logger.info('Filter level: %s', tweet['filter_level'])
            #
            print ''
        except:
            self._logger.exception('Could not process Twitter data.')
        finally:
            return True
        #
    
    def on_error(self, status):
        self._logger.error('StreamListener error: %s', status)

class TweetFetcher:
    
    fetchers = []
    
    def __init__(self, searchTerm, extraTerms):
        TweetFetcher.fetchers.append(self)
        self.searchTerm = searchTerm
        self.extraTerms = extraTerms
        self._logger = logging.getLogger(__name__)
    
    def startTwitterSearch(self):
        l = StdOutListener(self.searchTerm)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, l)
        self.stream.filter(track = ([self.searchTerm]+self.extraTerms), async = True, languages=['en'])#, filter_level='medium')
        #
        #self.t = threading.Thread(target=stream.filter, kwargs={'track':[self.searchTerm], 'async':True})
        #self.t.start()
        #
        self._logger.debug('Starting stream.')
    
    def stopSearch(self):
        self.stream.disconnect()
        #
        self._logger.debug('Stopping stream.')
    
    @staticmethod
    def stopAll():
        for x in TweetFetcher.fetchers:
            x.stopSearch()
        #
    
if __name__ == '__main__':
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    #
    import color_stream_handler
    import time
	#
    stream_handler = color_stream_handler.ColorStreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)-6s : %(name)-25s : %(message)s'))
    file_log_handler = logging.FileHandler('twitter - %s.log'%time.strftime("%a, %d %b %Y %Hh%Mm%Ss",time.localtime()))
    file_log_handler.setFormatter(logging.Formatter('%(levelname)-6s : %(name)-25s : %(message)s'))
    #
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_log_handler)
    #
    logger = logging.getLogger(__name__)
    #
    ##############
    
    def ctrlCHandler(signal, frame):
        logger.debug('Exiting program (CTRL-C).')
        TweetFetcher.stopAll()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, ctrlCHandler)
    
    t = TweetFetcher('google', ['android', 'GOOGL', 'Alphabet Inc'])
    t.startTwitterSearch()
    
    while True:
        sleep(20)
    
