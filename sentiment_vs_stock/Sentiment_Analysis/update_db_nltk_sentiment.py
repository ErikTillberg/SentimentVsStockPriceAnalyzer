from pymongo import MongoClient
from nltk_vader_sentiment_analysis import get_sentiment_from_text
import time

client = MongoClient()
db = client.TwitterData

collection_name = 'apple'

collection = db[collection_name+'_filtered_stocksymbol']
coll_size = db.command('collstats', collection_name+'_filtered_stocksymbol')['count']

start_time = time.time()
cursor = collection.find()
counter = 0

for record in cursor:
	if counter%1000==0:
		print 'progress: %d/%d tweets (%.2f), %f seconds'%(counter, coll_size, counter/float(coll_size), time.time()-start_time)
	#
	counter += 1
	try:
		sentiment = get_sentiment_from_text(record['text'])
		collection.update_one({
		'_id': record['_id']
		},{
		'$set': {
			'sentiment': sentiment
			}
		})
	except:
		pass
	#
#
