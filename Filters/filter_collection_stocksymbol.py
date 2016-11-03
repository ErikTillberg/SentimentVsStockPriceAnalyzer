from pymongo import MongoClient
import math
import re
import json
import time

client = MongoClient()
db = client.TwitterData

db_name = 'apple'
search_term = 'AAPL'

collection = db[db_name]
collSize = db.command("collstats", db_name)['count']
collToSave = db[db_name+'_filtered_stocksymbol']

def matchToString(tweetText, searchTerms):
	#for each group of search terms
	matches = []
	for l in searchTerms:
		#for each word in that group
		for word in l:
			matchObj = re.match(r'(.*)' + word + '(.*?).*', tweetText, re.M|re.I)
			if (matchObj): #if it matched, return first element in the list.
				matches.append(l[0])
				#return l[0]
	# make sure there are no duplicates
	return list(set(matches))
#
start_time = time.time()
cursor = collection.find()
counter = 0
for record in cursor:
    if counter%1000==0:
        print 'progress: %d/%d tweets, %f seconds'%(counter, collSize, time.time()-start_time)
        #start_time = time.time()
    #
    counter += 1
    #
    #print matchToString(collection.find()[i]['text'], [[search_term]])
    try:
        #if len(matchToString(record['text'], [[search_term]])) != 0:
        if search_term in record['text']:
            pass
            collToSave.insert_one(record)
            #print record['text']
            #print ''
        #
    except Exception as e:
        pass
        #print e
    #
#
