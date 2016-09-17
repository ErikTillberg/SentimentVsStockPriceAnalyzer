#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Import mongoDB
from pymongo import MongoClient

import json

#Variables that contains the user credentials to access Twitter API 
access_token = "307572680-a6YbnrmtRf93c3QSBKWwJIy7t4xpvtUXBAsy60Ds"
access_token_secret = "ChU5dC8rHj3WGrTnTOpBvBuRksYJimIU1xYkHR3UbezhU"
consumer_key = "WbUsbhL6bVlnukhWaHevAgDRO"
consumer_secret = "NF97BBUFmqyr6xJUF0aIk4Rnyl0SHNkPkyaDPZSOHIpjCnXZ7Z"

client = MongoClient()
db = client.TwitterData

keywords = []

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        db.tweets.insert_one(tweet)
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[' ', 'javascript', 'ruby', 'apple', 'tesla', 'cody'])
