import tweepy
from ingestion.database import twitterDB
from ingestion.api import API

# Init API and DB
api = API()
db = twitterDB()

# Getting the users for Ford, Fiat, GM, Volkswagen & Toyota
company_names = ["Ford", "fcagroup", "GM", "VW", "Toyota"]
users = api.get_users(company_names)

n_tweets = 0
limit = api.rate_limit_status()
print "The API does not allow to download more than %d twitters." % (limit)

for user in users:
	print "Reading twitter for %s...." % (user['name'])
	try:
		tweets = api.read_tweets(user['id'])
		n_tweets += len(tweets)
		db.save_coll(tweets, user['name'])
	except tweepy.error.RateLimitError as e:
		print e.message
		break
print '%d Tweets succesfully saved in MongoDB' % (n_tweets)