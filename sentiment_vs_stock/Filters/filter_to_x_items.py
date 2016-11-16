import math
import logging

from pymongo import MongoClient

from ..mongo_helpers import loop_over_collection

def filter_to_x_items(collection_name, new_collection_name, approx_num_of_tweets, log_debugging=False):
	client = MongoClient()
	db = client.TwitterData
	#
	collection = db[collection_name]
	collection_to_save = db[new_collection_name]
	momentary_collection_size = db.command('collstats', collection_name)['count']
	#
	every_x_tweet = math.floor(momentary_collection_size/approx_num_of_tweets)
	#
	def process_record(record, collection, counter):
		if counter % every_x_tweet == 0:
			collection_to_save.insert_one(record)
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
	filter_to_x_items(collection_name, new_collection_name, approx_num_of_tweets, True)
#
