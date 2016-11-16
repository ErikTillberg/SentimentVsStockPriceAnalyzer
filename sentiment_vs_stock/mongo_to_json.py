import json
import logging
import os

from .mongo_helpers import loop_over_collection

_logger = logging.getLogger(__name__)

def mongo_to_json_file(collection_name, filename, log_debugging=False):
	def process_record(record, collection, counter):
		my_str = json.dumps({'text':record['text'], 'sentiment':record['sentiment'], 'timestamp_sec':int(int(record['timestamp_ms'])/1000), 'stock_changes':record['stock_changes']})
		f.write(my_str)
		f.write(',\n')
	#
	with open(filename, 'wb') as f:
		f.write('[\n')
		#
		loop_over_collection(collection_name, process_record, 10000)
		#
		f.seek(-2, os.SEEK_CUR)
		# erase last new line and comma characters
		f.write('\n')
		#
		f.write(']\n')
	#
#
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	#
	collection_name = 'walmart_filtered'
	#
	mongo_to_json_file(collection_name, collection_name+'.json', True)
#
