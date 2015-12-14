from pymongo import MongoClient
import pymongo
import pandas as pd

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
        self.collection_name = coll_name

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

    # Returns a tweet in the current collection that does not have a user input
    def calibrate_tweet(self):
        tweets = self.collection.find({"user_sentiment": {"$nin": [0,1]}}).sort([("id", pymongo.ASCENDING)])
        num_tweets = tweets.count()
        print("You have %d tweets to classify." %num_tweets)

        i = 0
        working = 1
        while (working == 1 and i < num_tweets):
            t = tweets[i]
            t_id = t['id']

            print("Please read the following tweet.")
            print(t['text'].encode('utf-8'))
            print("Please tell if it is a positive (1) or a negative (0) tweet. Type 2 if you want to get out.")
            option = input("?")
            try:
                option = int(option) #
                if (option >= 0 and option <= 1):
                    self.set_user_sentiment(t_id, option)
                    i += 1
                elif (option == 2):
                    working == 0
                    i = num_tweets
                else:
                    print("Option number not valid. Enter a 0 or a 1")
            except ValueError as e:
                print("Input %s is incorrect, please enter a number." % str(e))

    # Return tweets from the current collection with a particular word
    def get_tweets_with_word(self, word):
        re = ".*"+word+".*"
        tweets = self.collection.find({"text": {"$regex": re}}).sort([("id", pymongo.ASCENDING)])
        if(tweets.count() > 0):
            print("There are %d tweets with this word." % tweets.count())
            working = 1
            while working == 1:
                print("Please tell if these tweets are positive (1) or negative (0).")
                option = input("?")
                try:
                    option = int(option) #
                    if (option >= 0 and option <= 1):
                        for t in tweets:
                            id = t['id']
                            self.set_user_sentiment(id, option)
                        working = 0
                    else:
                        print("Option number not valid. Enter a 0 or a 1")
                except ValueError as e:
                    print("Input %s is incorrect, please enter a number." % str(e))
        else:
            print("No tweets found with this word.")



    def set_user_sentiment(self, id, option):
        result = self.collection.update_one(
                        {"id" : id},
                        {
                            "$set": {
                                "user_sentiment": option
                            }
                        }
                    )

    def export_csv_user_sentiment(self):
        file = self.collection_name+"-sentiment.csv"
        tweets = self.collection.find({
            "user_sentiment": {"$in": [0,1]}
        },{
            "text": 1,
            "user_sentiment": 1,
            "_id": 0
        }
        )
        if(tweets.count() > 1):
            df = pd.DataFrame(list(tweets))
            df.drop_duplicates()
            df.to_csv(file, encoding = 'utf-8', index = False)
        else:
            print("There were no classified tweets in colection %s" %self.collection_name)

    def export_csv_collection(self):
        file = self.collection_name+"-raw.csv"
        tweets = self.collection.find()
        if(tweets.count() > 1):
            df = pd.DataFrame(list(tweets))
            df.to_csv(file, encoding = 'utf-8', index = False)
        else:
            print("There were no tweets in colection %s" %self.collection_name)
