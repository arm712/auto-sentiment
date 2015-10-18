import pymongo
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

    # Saves a particular element in an specified collection
    def save_element(self, element, coll_name):
        self.database[coll_name].insert(element)

    # Loads all the elements from an specified collection
    def load_coll(self, coll_name):
        return self.database[coll_name]