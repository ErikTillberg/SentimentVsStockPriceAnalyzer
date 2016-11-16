from pymongo import MongoClient

import math
import re
import json
import time
import logging
import numpy as np

from . import stock_data
from ..mongo_helpers import loop_over_collection

_logger = logging.getLogger(__name__)

def add_stock_price_changes_to_collection(collection_name, stock_name, stock_interval_seconds, log_debugging=False):
	# adds the stock change in-place
	#
	response = stock_data.get_stock_data(stock_interval_seconds, 30, stock_name)
	if log_debugging:
		_logger.debug(response['header'])
		_logger.debug(response['data'])
	#
	table = stock_data.parse_stock_data(response['data'], response['columns'], stock_interval_seconds)
	if log_debugging:
		_logger.debug(stock_data.get_stock_table_string(table['data'], table['columns']))
	#
	table = table['data']
	#
	def get_stock_val(timestamp, table, before_or_after):
		# may throw an exception when using 'after'
		table_times = [x[0] for x in table]
		time_offsets = np.array(table_times)-timestamp
		zero_crossings = np.where(np.diff(np.sign(time_offsets)))[0]
		# http://stackoverflow.com/a/3843124
		#
		if before_or_after == 'before':
			add_index_offset = 0
		elif before_or_after == 'after':
			add_index_offset = 1
		else:
			raise Exception('Must use "before" or "after".')
		#
		if len(zero_crossings) == 1:
			return table[zero_crossings[0]+add_index_offset][1]
		elif len(zero_crossings) > 1:
			# for this bug: "This doesn't work when there is a zero in the array. It will detect them twice! Example: a = [2,1,0,-1,2] will give array([1, 2, 3])"
			return table[zero_crossings[1]+add_index_offset][1]
		#
	#
	def process_record(record, collection, counter):
		timestamp = float(record['timestamp_ms'])/1000.0
		try:
			time_steps = [1, 2, 12, 24, 48]
			stock_changes = {}
			for x in time_steps:
				try:
					stock_changes[str(x)] = get_stock_val(timestamp+3600*x, table, 'after')-get_stock_val(timestamp, table, 'before')
				except Exception as e:
					_logger.exception(e)
					stock_changes[str(x)] = None
				#
			#
			collection.update_one(
					{
						'_id': record['_id']
					},
					{
						'$set': {
							'stock_changes': stock_changes
						}
					})
		except Exception as e:
			_logger.exception(e)
			pass
		#
	#
	loop_over_collection(collection_name, process_record, 1000)
#
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	#
	stock_name = 'WMT'
	collection_name = 'walmart_filtered'
	stock_interval_seconds = 3600
	#
	add_stock_price_changes_to_collection(collection_name, stock_name, stock_interval_seconds, True)
#
