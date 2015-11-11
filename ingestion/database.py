from pymongo import MongoClient

# This class creates an instance of our MongoDB
class twitterDB(object):

    # Initiates the client to our database
    def __init__(self):
        self.client = MongoClient()
        self.database = self.client.twitter_db

    # Saves a list of elements in an specified collection
    def save_coll(self, elements, coll_name):
        for element in elements:
            self.database[coll_name].insert(element)

    # Saves a particular element
    def save_element(self, element):
        data = {}
        data['id'] = element['id']
        data['created_at'] = element['created_at']
        data['favorite_count'] = element['favorite_count']
        data['retweet_count'] = element['retweet_count']
        data['text'] = element['text']
        data['user_name'] = element['user']['screen_name']
        data['model_sentiment'] = {}
        data['user_sentiment'] = {}
        self.collection.insert(data)

    # Loads an specified collection
    def load_coll(self, coll_name):
        self.collection = self.database[coll_name]

    # Loads the tweet from the current collection
    def load_tweets(self):
        tweets = []
        docs = self.collection.find()
        for d in docs:
            tweets.append(d)
        return tweets

    # Returns the collection names
    def get_collection_names(self):
        return self.database.collection_names()

    # Returns the number of tweets of the current collection
    def get_number_tweets(self):
        return self.collection.count()