from pymongo import MongoClient
import math
import re
import json
import time
import datetime
from bson import json_util

client = MongoClient()
db = client.TwitterData

collection_name = 'tesla filtered_filtered_no_garbage_filtered'
filename = collection_name+'.json'
collection = db[collection_name]
coll_size = db.command("collstats", collection_name)['count']

cursor = collection.find()
counter = 0

with open(filename, 'w') as f:
	f.write('[\n')
	for record in cursor:
		#my_str = json.dumps(record, sort_keys=True, default=json_util.default)
		my_str = json.dumps({'text':record['text'], 'sentiment':record['sentiment'], 'timestamp_sec':int(int(record['timestamp_ms'])/1000), 'stock_changes':record['stock_changes']})
		f.write(my_str)
		if counter != coll_size-1:
			f.write(',\n')
		else:
			print 'skipped'
			f.write('\n')
		#
		counter += 1
	#
	f.write(']\n')
#
