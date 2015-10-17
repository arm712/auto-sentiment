import tweepy
from pymongo import MongoClient
from tweepy.parsers import JSONParser

from ingestion import ingestion


# Keys for Twitter API
consumer_key = 'EfbgNEMgmXNSweNDcWmoaSwm0'
consumer_secret = 'u3HlNeQNhG4whVzbilCxvswfJTMLG4ppxisaqtB4exHvGgDxsc'
access_token_key = '3940337423-CC2NFNG4zX9t3Z4Hl5vAbseYmlhlz6CXbuDlQNr'
access_token_secret = 'tmK2f3ZPrOWSkqY2bzu9St0LqDzJVIp5IV8PWPwENh69z'

# Initiating the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth, parser = JSONParser())

# Initiating the MongoDB client
client = MongoClient()
db = client.twitter_db # Main Database

# Getting the users for Ford, Fiat & GM
ford_user = api.get_user("Ford")
fiat_user = api.get_user("fcagroup")
gm_user = api.get_user("GM")

users = [ford_user, fiat_user, gm_user]
n_tweets = 0

for user in users:
	tweets = ingestion.read_tweets(api, user['id'])
	n_tweets += len(tweets)
	ingestion.save_collection_json(db, tweets, user['name'])

print '%d Tweets succesfully saved in MongoDB' % (n_tweets)