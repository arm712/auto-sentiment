import tweepy
from tweepy.parsers import JSONParser

# This class creates an instance of the Twitter API
class API(object):

    # Initiates the API
    def __init__(self):
        # Keys for Twitter API (maybe reading it from a .txt)
        self.consumer_key = 'EfbgNEMgmXNSweNDcWmoaSwm0'
        self.consumer_secret = 'u3HlNeQNhG4whVzbilCxvswfJTMLG4ppxisaqtB4exHvGgDxsc'
        self.access_token_key = '3940337423-CC2NFNG4zX9t3Z4Hl5vAbseYmlhlz6CXbuDlQNr'
        self.access_token_secret = 'tmK2f3ZPrOWSkqY2bzu9St0LqDzJVIp5IV8PWPwENh69z'

        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token_key, self.access_token_secret)

        self.api = tweepy.API(self.auth, parser = JSONParser())

    # From a list of user_names, it returns the corresponding User entities
    def get_users(self, user_names):
        users = []
        for user in user_names:
            users.append(self.api.get_user(user))

        return users

    # Returns all the tweets in the timeline of a particular user
    def read_tweets(self, user_id):
        newest_id = 1 # The id of the newest tweet read (always greater than the oldest)
        oldest_id = 0 # The id of the oldest tweet read (always lower than the oldest)

        # While we are receiving new tweets
        while newest_id -oldest_id > 0:
            tweets = []
            try:
                # First option: This is the first time we read tweets
                if oldest_id == 0:
                    tweets = self.api.user_timeline(id = user_id, count = 200) # Take 200 tweets
                    newest_id = tweets[0]['id'] # Update the newest id
                    oldest_id = tweets[len(tweets)-1]['id'] # Update the oldest id

                # Second option: This is not the first time we read tweets
                else:
                    new_tweets = self.api.user_timeline(id = user_id, count = 200,
                                                    max_id = oldest_id) # Take 200 tweets previous to the oldest tweet
                    tweets.extend(new_tweets) # Append the new tweets to the list
                    newest_id = new_tweets[0]['id'] # Update the newest id
                    oldest_id = new_tweets[len(new_tweets)-1]['id'] # Update the oldest id
            except tweepy.error.RateLimitError:
                limit = len(tweets)
                msg = "Rate limit reached after reading %d tweets." % (limit)
                raise tweepy.error.RateLimitError(msg)

        return tweets

    def rate_limit_status(self):
        return self.api.rate_limit_status()['resources']['account']['/account/settings']['limit']