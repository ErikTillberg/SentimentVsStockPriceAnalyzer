from pymongo import MongoClient
import math
import re
import json
import time
import numpy as np
from stock_data import parse_stock_data, get_stock_data, get_stock_table_string

stock_name = 'TSLA'
collection_name = 'tesla filtered_filtered_no_garbage'
interval_seconds = 3600
#
###############
#
response = get_stock_data(interval_seconds, 30, stock_name)
print response['header']
print response['data']
table = parse_stock_data(response['data'], interval_seconds)
print get_stock_table_string(table)
print

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
#print table[10][0]+2352
#print get_stock_val(table[10][0]+2352, table, 'before')

###############

client = MongoClient()
db = client.TwitterData


collection = db[collection_name+'_filtered']
coll_size = db.command('collstats', collection_name+'_filtered')['count']

start_time = time.time()
cursor = collection.find()
counter = 0

for record in cursor:
	if counter%1000==0:
		print 'progress: %d/%d tweets (%.2f), %f seconds'%(counter, coll_size, counter/float(coll_size), time.time()-start_time)
	#
	counter += 1
	timestamp = float(record['timestamp_ms'])/1000.0
	try:
		stock_changes = {}
		try:
			stock_changes['1'] = get_stock_val(timestamp+3600*1, table, 'after')-get_stock_val(timestamp, table, 'before')
		except Exception as e:
			print e
			stock_changes['1'] = None
		#
		try:
			stock_changes['2'] = get_stock_val(timestamp+3600*2, table, 'after')-get_stock_val(timestamp, table, 'before')
		except:
			stock_changes['2'] = None
		#
		try:
			stock_changes['12'] = get_stock_val(timestamp+3600*12, table, 'after')-get_stock_val(timestamp, table, 'before')
		except:
			stock_changes['12'] = None
		#
		try:
			stock_changes['24'] = get_stock_val(timestamp+3600*24, table, 'after')-get_stock_val(timestamp, table, 'before')
		except:
			stock_changes['24'] = None
		#
		try:
			stock_changes['48'] = get_stock_val(timestamp+3600*48, table, 'after')-get_stock_val(timestamp, table, 'before')
		except:
			stock_changes['48'] = None
		#
		collection.update_one({
		'_id': record['_id']
		},{
		'$set': {
			'stock_changes': stock_changes
			}
		})
	except Exception as e:
		print e
		pass
	#
#
