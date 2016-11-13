from pymongo import MongoClient
import math
import re
import json
import time

client = MongoClient()
db = client.TwitterData
#
coll_name = "microsoft"
#
collection = db[coll_name]
collSize = db.command("collstats", coll_name)['count']
collToSave = db[coll_name+'_filtered_no_garbage']
#
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
#
for record in cursor:
    if counter%1000==0:
        print 'progress: %d/%d tweets, %f seconds'%(counter, collSize, time.time()-start_time)
    #
    counter += 1
    #
    try:
		if (len(record['entities']['urls']) == 0): #if there are no urls detected
			collToSave.insert_one(record)
			
    except Exception as e:
        pass
        #print e
    #
#
