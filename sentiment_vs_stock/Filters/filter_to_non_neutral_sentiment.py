from pymongo import MongoClient

import math
import logging

from ..Sentiment_Analysis.nltk_vader_sentiment_analysis import get_sentiment_from_text
from ..mongo_helpers import loop_over_collection

_logger = logging.getLogger(__name__)

def filter_to_non_neutral_sentiment(collection_name, new_collection_name, approx_num_of_tweets=None, log_debugging=False):
	# this function also adds the sentiment to the new collection
	#
	if collection_name == new_collection_name:
		raise Exception('You cannot filter a collection into itself!')
	#
	client = MongoClient()
	db = client.TwitterData
	#
	collection = db[collection_name]
	collection_to_save = db[new_collection_name]
	momentary_collection_size = db.command('collstats', collection_name)['count']
	#
	if approx_num_of_tweets is None:
		# try to get every non-neutral tweet in the collection
		every_x_tweet = 1
	else:
		every_x_tweet = math.floor(momentary_collection_size/approx_num_of_tweets)
	#
	class nonlocal: pass
	nonlocal.use_next_tweet = False
	# this is a hack because Python 2 does not support the nonlocal keyword
	# http://stackoverflow.com/a/8448011
	#
	def process_record(record, collection, counter):
		if nonlocal.use_next_tweet:
			try:
				sentiment = get_sentiment_from_text(record['text'])
				if sentiment['neu'] != 1.0:
					record['sentiment'] = sentiment
					collection_to_save.insert_one(record)
					nonlocal.use_next_tweet = False
			except:
				_logger.exception('Error while getting sentiment and entering into collection.')
			#
		else:
			if counter % every_x_tweet == 0:
				try:
					sentiment = get_sentiment_from_text(record['text'])
					if sentiment['neu'] != 1.0:
						record['sentiment'] = sentiment
						collection_to_save.insert_one(record)
					else:
						nonlocal.use_next_tweet = True
				except:
					_logger.exception('Error while getting sentiment and entering into collection.')
				#
			#
		#
	#
	loop_over_collection(collection_name, process_record, 1000)
#
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	#
	collection_name = 'apple'
	new_collection_name = collection_name+'_filtered'
	approx_num_of_tweets = 50000
	#
	filter_to_non_neutral_sentiment(collection_name, new_collection_name, approx_num_of_tweets, True)
#
