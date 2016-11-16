from pymongo import MongoClient

import time
import logging

from ..mongo_helpers import loop_over_collection

'''
def _matchToString(tweetText, searchTerms):
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
'''
#
def filter_to_no_url_and_no_spam(collection_name, new_collection_name, spam_cap=100, filter_URLs=True, filter_spam=True, log_debugging=False):
	if collection_name == new_collection_name:
		raise Exception('You cannot filter a collection into itself!')
	#
	client = MongoClient()
	db = client.TwitterData
	collection_to_save = db[new_collection_name]
	#
	'''
	#convert all the timestamps in a collection to integers
	conversionCursor = collection.find(modifiers = {"$snapshot": True})

	momentary_collection_size = db.command('collstats', collection_name)['count']
	print ("Converting string to integer")
	counter = 0

	#for item in conversionCursor:
	#
	#	if counter%1000==0:
	#		print('conversion progress: %d/%d tweets'%(counter, momentary_collection_size))
	 #   #
		#counter += 1
	#
	#	time = item['timestamp_ms']
	#	item['timestamp_ms'] = int(item['timestamp_ms'])
	#	collection.save(item)

	print ("Starting filters...")
	#end conversion, onto real work
	'''
	#
	def process_record(record, collection, counter):
		try:
			if filter_URLs:
				urls = record['entities']['urls']
				if (len(urls) > 0): #if there are urls
					return
				#
			#
			if filter_spam:
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
				#
				#if they tweeted more than some spam_cap (defined at top), then skip this tweet
				#print ('count: ' + count)
				if (count > spam_cap): 
					return
				#
			#if tweet passes all the filters, happy times, add to new collection.
			#print('saving tweet')
			collection_to_save.insert_one(record)
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
	new_collection_name = collection_name+'_filtered'
	spam_cap = 100
	filter_URLs = True
	filter_spam = True
	#
	filter_to_no_url_and_no_spam(collection_name, new_collection_name, spam_cap, filter_URLs, filter_spam, True)
#
