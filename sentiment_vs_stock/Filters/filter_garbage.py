from pymongo import MongoClient
import math
import re
import json
import time

client = MongoClient()
db = client.TwitterData
#
coll_name = "tesla filtered"
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

#convert all the timestamps in a collection to integers
conversionCursor = collection.find(modifiers = {"$snapshot": True})

print ("Converting string to integer")
counter = 0

#for item in conversionCursor:
#
#	if counter%1000==0:
#		print('conversion progress: %d/%d tweets'%(counter, collSize))
 #   #
	#counter += 1
#
#	time = item['timestamp_ms']
#	item['timestamp_ms'] = int(item['timestamp_ms'])
#	collection.save(item)

print ("Starting filters...")
#end conversion, onto real work

cursor = collection.find()
counter = 0
#
filterURLs = True
filterSpam = True
spamCap = 100
#
for record in cursor:
    if counter%1000==0:
        print 'progress: %d/%d tweets'%(counter, collSize)
    #
    counter += 1
	
    #
    try:
		if filterURLs:
			urls = record['entities']['urls']
			#print urls
			if (len(urls) > 0): #if there are urls
				continue
		if filterSpam:
			#find userID in record
			id = record['user']['id']
			#find time it was tweeted
			time = int(record['timestamp_ms'])
			#add one hour
			timeMax = str(time + 3600*1000)
			time = str(time)
			#fetch all the tweets by that user within the next hour
			userTweetsWithinHour = collection.find({'$and': [{'user.id': id}, {'timestamp_ms': {'$lt': timeMax, '$gt': time}}]})
			count = userTweetsWithinHour.count()
			
			#if they tweeted more than some spamCap (defined at top), then skip this tweet
			#print ('count: ' + count)
			if (count > spamCap): 
				continue
			
		#if tweet passes all the filters, happy times, add to new collection.
		#print('saving tweet')
		collToSave.insert_one(record)

		
    except Exception as e:
        pass
        print e
    #
#
