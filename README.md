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

[Tweet Sentiment Visualization] (https://www.csc.ncsu.edu/faculty/healey/tweet_viz/tweet_app/)
[Examples of Sentiment Analysis products] (http://help.sentiment140.com/other-resources) _From_ [_Sentiment140_](http://help.sentiment140.com/other-resources) 
[Realtime, Twitter sentiment analysis engine] (http://www.streamcrab.com/)
[Trending on Twitter: Social Sentiment Analytics] (http://www.bloomberg.com/company/announcements/trending-on-twitter-social-sentiment-analytics/)

## 3. Data ingestion: Tweets \& Stock Data
Data ingestion is _"the process of obtaining, importing, and processing data for later use or storage in a database."_ (Source: [WhatIs.com](http://whatis.techtarget.com/definition/data-ingestion) According to this definition we define the following processes as the inception of our own Twitter sentiment analysis tool:

1. Obtaining and processing tweets via Twitter API
2. Obtaining and processing stock prices via a public Financial Data provider
3. Storing the data in a MongoDB database

### 3.1. The Twitter API
One of the best features of Twitter is its [public API](https://dev.twitter.com/overview/documentation) which it's available to every Twitter user interested in application development. Thanks to this API, any Twitter user can create custom applications that would read the Twitter universe which mainly includes:

- [**Users:**](https://dev.twitter.com/overview/api/users) Entities that create the information via tweeting, retweeting, following, etc. They tend to represent people, companies or whatever entity interested in participating in the Twitter worldwide conversation.
- [**Tweets:**](https://dev.twitter.com/overview/api/tweets) Basic units of textual information created by Users.
 
 The Twitter API is well documented in the links above but for practical purposes is much more efficient to use an existing Twitter API library for Python. In [this link](https://dev.twitter.com/overview/api/twitter-libraries) we can find many libraries that are available for coding n many different languages.
 
 In our case, we have decided to use [Tweepy](https://github.com/tweepy/tweepy) created by Joshua Roesslein. This library is broadly used and we can find many examples of use.
