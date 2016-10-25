from pymongo import MongoClient
import math
import re
import json

client = MongoClient()
db = client.TwitterData

collection = db['tesla']
#get count of collection
#print(db.command("collstats", "microsoft")['count'])

#get element in collection
#print(collection.find()[0])
        
num = 50000
collSize = db.command("collstats", "tesla")['count']

everyXTweet = math.floor(collSize/num) #14 for wells fargo

collToSave = db['tesla filtered']
count = 0

for i in range(0, collSize):
    if i%10000==0:
        print 'progress: ' + str(i)
    if i % everyXTweet == 0
        collToSave.insert_one(collection.find()[i])
        
