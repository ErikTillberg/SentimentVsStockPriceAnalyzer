from pymongo import MongoClient

import time
import logging

_logger = logging.getLogger(__name__)

def loop_over_collection(collection_name, process_record_func, log_msg_every_x_tweets=None):
	client = MongoClient()
	db = client.TwitterData
	#
	collection = db[collection_name]
	momentary_collection_size = db.command('collstats', collection_name)['count']
	#
	cursor = collection.find()
	#
	start_time = time.time()
	counter = 0
	#
	for record in cursor:
		if log_msg_every_x_tweets is not None and counter%log_msg_every_x_tweets == 0:
			_logger.info('progress: %d/%d tweets (%.2f), %f seconds'%(counter, momentary_collection_size, counter/float(momentary_collection_size), time.time()-start_time))
		#
		if process_record_func(record, collection, counter) is False:
			break
		#
		counter += 1
	#
#