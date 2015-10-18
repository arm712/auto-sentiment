import tweepy
from tweepy import Stream

from ingestion.database import twitterDB
from ingestion.api import API
from ingestion.sniffer import MySniffer

# Init API and DB
api = API()
db = twitterDB()

# Setting up the keywords
keywords = ["Ford", "Fiat", "GM", "VW", "Toyota", "General Motors", "Volkswagen"]

sniffer = Stream(api.auth, MySniffer(db))
sniffer.filter(keywords)