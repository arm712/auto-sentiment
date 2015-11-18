# Code from http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

from tweepy.streaming import StreamListener
import json
import time

# Sniffs tweets from twitter and saves them in a MongoDB
class MySniffer(StreamListener):

    # Initiates the sniffer passing the database to use
    def __init__(self, api, db, time_limit):
        self.database = db
        self.api = api
        self.time = time.time()
        self.limit = time_limit

    # What to do if data is read
    def on_data(self, data):
        while(time.time() - self.time) < self.limit:
            try:
                tweet = json.loads(data)
                self.database.save_element(tweet)
                print (".")
                return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(11)
                #pass
        exit()

    def on_error(self, status):
        print(status)
        return True
