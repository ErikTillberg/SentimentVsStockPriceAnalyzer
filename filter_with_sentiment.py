from pymongo import MongoClient
import math
import re
import json
import time
from nltk_vader_sentiment_analysis import get_sentiment_from_text

client = MongoClient()
db = client.TwitterData

db_name = 'apple'

collection = db[db_name]
#get count of collection
#print(db.command("collstats", "microsoft")['count'])

#get element in collection
#print(collection.find()[0])
        
num = 50000
collSize = db.command("collstats", db_name)['count']

everyXTweet = math.floor(collSize/num) #14 for wells fargo
print 'everyXTweet: %d'%(everyXTweet)

collToSave = db[db_name+'_filtered']
collSize2 = db.command("collstats", db_name+'_filtered')['count']
if collSize2 != 0:
	print "Collection %s is not empty. Aborting!"%(db_name+'_filtered')
	exit()
#

start_time = time.time()
cursor = collection.find()
counter = 0

use_next_tweet = False

for record in cursor:
	if counter%10000==0:
		print 'progress: %d/%d tweets, %f seconds'%(counter, collSize, time.time()-start_time)
	counter += 1
	if use_next_tweet:
		sentiment = get_sentiment_from_text(record['text'])
		if sentiment['neu'] != 1.0:
			record['sentiment'] = sentiment
			collToSave.insert_one(record)
			use_next_tweet = False
		#
	else:
		if counter % everyXTweet == 0:
			sentiment = get_sentiment_from_text(record['text'])
			if sentiment['neu'] != 1.0:
				record['sentiment'] = sentiment
				collToSave.insert_one(record)
			else:
				use_next_tweet = True
			#
        #
	#
#
