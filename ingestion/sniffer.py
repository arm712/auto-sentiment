# Code from http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

import pymongo
from tweepy import Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json

# Sniffs tweets from twitter and saves them in a MongoDB
class MySniffer(StreamListener):

    # Initiates the sniffer passing the database to use
    def __init__(self, db):
        self.database = db

    # What to do if data is read
    def on_data(self, data):
        while (self.api.rate_limit_status()['resources']['account']['/account/settings']['limit']) != 0:
            try:
                tweet = json.loads(data)
                self.database['sniffed_data'].insert(tweet)
                return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                pass
            return True
        exit()

    def on_error(self, status):
        print(status)
        return True
