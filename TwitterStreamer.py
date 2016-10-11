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

class ExceptionLogger(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    #
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # see here: http://stackoverflow.com/a/16993115/3731982
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        #
        self._logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    #

def _install_thread_excepthook():
    '''
    Workaround for sys.excepthook thread bug
    From http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    '''
    import threading
    init_old = threading.Thread.__init__
    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run
        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    threading.Thread.__init__ = init

if __name__ == '__main__':
    _install_thread_excepthook()
    sys.excepthook = ExceptionLogger().handle_exception
    #
    ##############
    #
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
    #
    import yaml
    with open('api_keys.yaml', 'r') as f:
        api_keys = yaml.load(f)
    #
    access_token = api_keys['twitter']['access_token']
    access_token_secret = api_keys['twitter']['access_token_secret']
    consumer_key = api_keys['twitter']['consumer_key']
    consumer_secret = api_keys['twitter']['consumer_secret']
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
    
