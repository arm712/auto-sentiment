# Leveraging Twitter sentiment of auto manufacturing companies to predict changes in stock prices.

**Authors:**
- Andrew Miller
- Caroline Morris
- Huyen Le
- Jonathan Creem (Coordinator)
- Max Almodovar
 
## 1. Introduction
 Since its inception in 2006, Twitter has become an established social media outlet for corporations and other organizations. Because of its large scale and diverse user base, the ability to leverage the sentiment of Tweets provides for a unique avenue into the conscious of potential consumers. It is this information we hope to exploit.
     
 By focusing on the sentiment of potential consumers of different auto manufacturing companies we believe we can predict changes in their stock value (and/or volumes).
    	 
 There are two goals we would like to accomplish upon the completion of this project. One would be to engineer an accurate predictive model, and the second is to design two dynamic visualization tools to depict the large quantity of data produced by Twitter. One will be a heat map showing the global reach Tweets referencing the car manufactures and the other will be a linear sentiment scale showing the implied favorability and un-favorability of the companies. 

## 2. Twitter sentiment analysis products
_(Some text related to this products)_

- [Tweet Sentiment Visualization] (https://www.csc.ncsu.edu/faculty/healey/tweet_viz/tweet_app/)
- [Examples of Sentiment Analysis products] (http://help.sentiment140.com/other-resources) _From_ [_Sentiment140_]
(http://help.sentiment140.com/other-resources) 
- [Realtime, Twitter sentiment analysis engine] (http://www.streamcrab.com/)
- [Trending on Twitter: Social Sentiment Analytics] (http://www.bloomberg
.com/company/announcements/trending-on-twitter-social-sentiment-analytics/)

## 3. Data ingestion: Tweets \& Stock Data
Data ingestion is _"the process of obtaining, importing, and processing data for later use or storage in a database
"_ (Source: [WhatIs.com](http://whatis.techtarget.com/definition/data-ingestion)). According to this definition we 
define the following processes as the inception of our own Twitter sentiment analysis tool:

1. Obtaining and processing tweets via Twitter API
2. Obtaining and processing stock prices via a public Financial Data provider
3. Storing the data in a MongoDB database

### 3.1. The Twitter API
One of the best features of Twitter is its [public API](https://dev.twitter.com/overview/documentation) which it's available to every Twitter user interested in application development. Thanks to this API, any Twitter user can create custom applications that would read the Twitter universe which mainly includes:

- [**Users:**](https://dev.twitter.com/overview/api/users) Entities that create the information via tweeting, retweeting, following, etc. They tend to represent people, companies or whatever entity interested in participating in the Twitter worldwide conversation.
- [**Tweets:**](https://dev.twitter.com/overview/api/tweets) Basic units of textual information created by Users.
 
The Twitter API is well documented in the links above but for practical purposes is much more efficient to use an
existing Twitter API library for Python. In [this link](https://dev.twitter.com/overview/api/twitter-libraries) we 
can find many libraries that are available for coding n many different languages. For our project, we have chosen to
use [Tweepy](https://github.com/tweepy/tweepy) created by Joshua Roesslein. This library is broadly used and we can 
find many examples of its use on the Internet.
 
#### 3.1.1. Different approaches to obtain and process tweets
With the Tweepy library we can easily obtain tweets from a user timeline. The first important part is to obtain the 
[access tokens](https://dev.twitter.com/oauth/overview/application-owner-access-tokens) that allow access to Twitter API capabilities. 

```python 
  # Keys for Twitter API
  consumer_key = 'CONSUMER_KEY'
  consumer_secret = 'CONSUMER_SECRET'
  access_token_key = 'ACCESS_TOKEN_KEY'
  access_token_secret = 'ACCESS_TOKEN_SECRET'
```
Once we have the tokens, we can initiate our `api` with the code below. Note that we use a JSONParser in a way that 
all the information obtained via the API is presented in JSON format. This way is much better and efficient when we 
planned to store the info on a DB.       

```python
import tweepy
from tweepy.parsers import JSONParser

# Initiating the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth, parser = JSONParser())
```
At this moment we face the first important decision of our project. As we are trying to obtain tweets related to 
automobile companies we have 2 options to do so:

1. Extract all the tweets from the company timeline.
2. Extract all the tweets referring to the company.

The first option is very manageable in terms of coding, with the only drawback of forcing the user to make multiple 
requests to Twitter API. First, we obtain the user id of the companies that we want to analyze:

```python
# Getting the users for different companies
ford_user = api.get_user("Ford")
fiat_user = api.get_user("fcagroup")
gm_user = api.get_user("GM")
toyota_user = api.get_user("Toyota")
vw_user = api.get_user("VW")
```
By using the function below, we can easily read all the tweets of any of the Twitter users defined above. 

```python
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
            # Take the previous 200 tweets
            new_tweets = api.user_timeline(id = user_id, count = 200, max_id = oldest_id)             
            tweets.extend(new_tweets) # Append the new tweets to the list
            newest_id = new_tweets[0]['id'] # Update the newest id
            oldest_id = new_tweets[len(new_tweets)-1]['id'] # Update the oldest id

    return tweets
```
While in terms of coding this approach is very simple, there is a major disadvantage in terms of accuracy of the 
results. If we try to measure the Twitter sentiment on a particular company by using only its own tweets, we would be
measuring the self-sentiment of the company. Although this approach may be interesting in terms of understanding the
self-esteem of the company, we need external data to determine correlations with stock prices. Since a company stock 
price is mainly derived from external factors, it is important to include some external sentiment in the equation. 
This points us to the second option.

The second option is based on "sniffing" data out of the Twitter universe by looking for particular terms in the 
Tweets that may refer to the companies of study. In this [website](http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/) 
we find a good example of how to get real time tweets via a `StreamListener()`. The code is easily replicable and 
would include different words to track tweets related to our auto companies.
 
Same as with the first approach, this option has a very important limitation. The "sniffing" process gathers tweets 
from the present and the future (depending on how long you execute it), but not from the past. Historical data in 
twitter cannot be gathered unless you hire a company to do so, which is very expensive for the purposes of our study. 

### 3.2. Historical stock prices 
We will use [Yahoo Finance](http://finance.yahoo.com/) as the provider of financial data. Once a company security is 
chosen, Yahoo Finance allows the user to easily download all the historical prices in a csv file. We will use this 
csv files for our tool, that way we will develop knowledge on how to ingest data from APIs and files. For reading 
these csv files, we will use [pandas](http://pandas.pydata.org/pandas-docs/stable/generated/pandas
.read_csv.html).

### 3.3. MongoDB
Gathering tweets from Twitter generates a lot of semi-structured information in the form of JSON files. Hence, it 
seems reasonable to use a NoSQL tool like [MongoDB](https://www.mongodb.org/) to store these information. We will follow the tutorials on [this 
website](http://stats.seandolinar.com/collecting-twitter-data-storing-tweets-in-mongodb/). Basically we need a couple
 of steps in our code:

```python
# Step 1: Setting up the MongoDB client
client = MongoClient()
db = client.twitter_db # Pointer to the twitter database
```
```python
# Step 2: Save the tweets related to an specific user in its specific collection
def save_collection_json (db, tweets, user_name):
    for tweet in tweets:
        db[user_name].insert(tweet)
```

 