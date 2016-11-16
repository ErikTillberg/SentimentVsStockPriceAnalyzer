from pymongo import MongoClient
from marketplace_sentiment import get_sentiment_from_text

client = MongoClient()
db = client.TwitterData

collection = db['wells fargo filtered']
#get count of collection
#print(db.command("collstats", "microsoft")['count'])

#get element in collection
#print(collection.find()[0])

collSize = db.command("collstats", "wells fargo filtered")['count']

import yaml
with open('../api_keys.yaml', 'r') as f:
    api_keys = yaml.load(f)
#
apikey = api_keys['marketplace']['apikey']

for i in range(0, collSize):
    if (i%1000 == 0):
        print "progress: " + str(i)
    try:
        obj = collection.find()[i]
        sent = get_sentiment_from_text(obj['text'], apikey)
        collection.update_one({
        '_id': obj['_id']
        },{
        '$set': {
            'sentiment': sent
            }
        })
    except:
        print "Couldn't process"
