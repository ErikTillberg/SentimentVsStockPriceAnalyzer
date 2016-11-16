from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from pymongo import MongoClient

import json
import logging
import re

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, searchTerms):
        self.searchTerms = searchTerms
        self.client = MongoClient()
        self.db = self.client.TwitterData
        self._logger = logging.getLogger(__name__)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            #Search the list of words:
            matchedWords = self.matchToString(tweet['text'])
            if (len(matchedWords) != 0):
                for x in matchedWords:
                    collection = self.db[x]
                    collection.insert_one(tweet)
                #
            #if a match wasn't found, the text must have appeared in an imbedded link.
            else:
                collection = self.db['unmatched']
                collection.insert_one(tweet)

            print matchedWords
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

    #method checks through list of lists of search words, matching each to the string. If it finds a match it returns the
    #first item in the list it matched to.
    def matchToString(self, tweetText):
        #for each group of search terms
        matches = []
        for l in self.searchTerms:
            #for each word in that group
            for word in l:
                matchObj = re.match(r'(.*)' + word + '(.*?).*', tweetText, re.M|re.I)
                if (matchObj): #if it matched, return first element in the list.
                    matches.append(l[0])
                    #return l[0]
        # make sure there are no duplicates
        return list(set(matches))

    def on_error(self, status):
        self._logger.error('StreamListener error: %s', status)

class TweetFetcher:

    fetchers = []

    def flatten(self, listOfLists):
        "Flatten one level of nesting"
        return [x for sublist in listOfLists for x in sublist]

    def __init__(self, searchTerms, access_token, access_token_secret, consumer_key, consumer_secret):
        TweetFetcher.fetchers.append(self)
        self.searchTerms = searchTerms
        self._logger = logging.getLogger(__name__)
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def startTwitterSearch(self):
        l = StdOutListener(self.searchTerms)
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        self.stream = Stream(auth, l)

        #Flatten the list of search terms, searching for every word.
        self.stream.filter(track = self.flatten(self.searchTerms), async = False, languages=['en'])#, filter_level='medium')

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
