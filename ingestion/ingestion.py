import json

'''
Read_tweets : reads all the tweets of an specific user id
'''

def read_tweets(api, user_id):
    newest_id = 1 # The id of the newest tweet read (always greater than the oldest)
    oldest_id = 0 # The id of the oldest tweet read (always lower than the oldest)

    # While we are receiving new tweets
    while newest_id -oldest_id > 0:
        # First option: This is the first time we read tweets
        if oldest_id == 0:
            tweets = api.user_timeline(id = user_id, count = 200) # Take 200 tweets
            newest_id = tweets[0]['id'] # Update the newest id
            oldest_id = tweets[len(tweets)-1]['id'] # Update the oldest id

        # Second option: This is not the first time we read tweets
        else:
            new_tweets = api.user_timeline(id = user_id, count = 200,
                                            max_id = oldest_id) # Take 200 tweets previous to the oldest tweet
            tweets.extend(new_tweets) # Append the new tweets to the list
            newest_id = new_tweets[0]['id'] # Update the newest id
            oldest_id = new_tweets[len(new_tweets)-1]['id'] # Update the oldest id

    return tweets

'''
Save_db: Saves all the tweets in an specific MongoDB collection as JSON
'''
def save_collection_json (db, elements, name):
    for element in elements:
        db[name].insert(element)





