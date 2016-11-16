from sentiment_vs_stock.Streamers.TwitterStreamer import TweetFetcher

from misc.logging_helper import setup_logging

import signal
import sys

if __name__ == '__main__':
    setup_logging('twitter_streamer')
    #
    ##############
    #
    import yaml
    with open('settings.yaml', 'r') as f:
        settings = yaml.load(f)
    #
    access_token = settings['apikeys']['twitter']['access_token']
    access_token_secret = settings['apikeys']['twitter']['access_token_secret']
    consumer_key = settings['apikeys']['twitter']['consumer_key']
    consumer_secret = settings['apikeys']['twitter']['consumer_secret']
    #
    ##############
    #
    def ctrlCHandler(signal, frame):
        logger.debug('Exiting program (CTRL-C).')
        TweetFetcher.stopAll()
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrlCHandler)

    t = TweetFetcher(settings['twitter_streamer']['search_terms'], access_token, access_token_secret, consumer_key, consumer_secret)

    t.startTwitterSearch()

    while True:
        sleep(20)
