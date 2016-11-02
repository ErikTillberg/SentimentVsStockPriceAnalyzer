from pymongo import MongoClient
import math
import re
import json
import time

client = MongoClient()
db = client.TwitterData

db_name = 'tesla'

collection = db[db_name]
#get count of collection
#print(db.command("collstats", "microsoft")['count'])

#get element in collection
#print(collection.find()[0])
        
num = 50000
collSize = db.command("collstats", db_name)['count']

everyXTweet = math.floor(collSize/num) #14 for wells fargo

collToSave = db[db_name+' filtered']

start_time = time.time()
cursor = collection.find()
counter = 0

for record in cursor:
    if counter%10000==0:
        print 'progress: %d/%d tweets, %f seconds'%(counter, collSize, time.time()-start_time)
    counter += 1
    if counter % everyXTweet == 0:
        collToSave.insert_one(record)
        
