from tweepy import Stream
from ingestion.database import twitterDB
from ingestion.api import API
from ingestion.sniffer import MySniffer
import time

# Init all the required objects
api = API()
db = twitterDB()
ts = time.strftime("%m%d%y %H:%M:%S", time.gmtime(time.time()))
db.load_coll(ts)

working = 1

while working == 1:
    print("For how many minutes do you want to get Tweets?")
    minutes = input(">")
    try:
        seconds = float(minutes)*60
        if (seconds < 30):
            print("Please enter a higher number.")
        else:
            working = 0
    except ValueError as e:
        print("Input %s is incorrect, please enter a number." % str(e))

sniffer = Stream(api.auth, MySniffer(api, db, seconds))

sniffer.filter(track = ['volkswagen', 'toyota', 'mercedes', 'general motors'], languages = ['en'])
