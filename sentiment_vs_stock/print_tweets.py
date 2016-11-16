from pymongo import MongoClient
from nltk_vader_sentiment_analysis import get_sentiment_from_text
import math
import re
import json
import time

client = MongoClient()
db = client.TwitterData

collection_name = 'costco'
collection = db[collection_name]

cursor = collection.find()
counter = 0

for record in cursor:
	if counter > 60:
		exit()
	#
	print record['text'].encode('utf-8')
	print get_sentiment_from_text(record['text'])
	print
	#
	counter += 1
#
