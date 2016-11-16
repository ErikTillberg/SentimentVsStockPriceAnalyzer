from pymongo import MongoClient

import logging

from ..mongo_helpers import loop_over_collection

def filter_to_only_stocksymbol(collection_name, new_collection_name, search_term, log_debugging=False):
	if collection_name == new_collection_name:
		raise Exception('You cannot filter a collection into itself!')
	#
	client = MongoClient()
	db = client.TwitterData
	collection_to_save = db[new_collection_name]
	#
	def process_record(record, collection, counter):
		try:
			if search_term in record['text']:
				print record['text']
				collection_to_save.insert_one(record)
			#
		except Exception as e:
			pass
			#print e
		#
	#
	loop_over_collection(collection_name, process_record, 1000)
#
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	#
	collection_name = 'apple'
	search_term = 'AAPL'
	new_collection_name = collection_name+'_filtered'
	#
	filter_to_only_stocksymbol(collection_name, new_collection_name, search_term, True)
#
