import pandas as pd
import re
import numpy as np
import nltk.data
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
from sklearn.cross_validation import train_test_split
from gensim.models import Word2Vec
from gensim.models.word2vec import Word2Vec
import sys

reload(sys)
sys.setdefaultencoding("utf8")

corpus = pd.read_csv('Sentiment_Analysis_Dataset_test.csv', 
                    index_col=0, 
                    header=0,
                    dtype=object,
                    usecols=['ItemID', 'Sentiment', 'SentimentText']) 
                    

corpus['SentimentText'] = corpus['SentimentText'].astype('str')  
corpus = corpus.dropna(subset=['Sentiment'], how='any')  

with open('test.tweettest.json') as f:
    data = f.readlines()
data = map(lambda x: x.rstrip(), data)
data_json_str = "[" + ','.join(data) + "]"
test = pd.read_json(data_json_str)

test['text'] = test['text'].apply(str) 

class Wrangler(object):

    def __init__(self):
        punctuation = list(string.punctuation)
        self.stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '@nba', 'nba', '#nba', '\u2026']
        emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""

        regex_str = [
            emoticons_str,
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
        ]

        self.tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    def tokenize(self, s):
        return self.tokens_re.findall(s)

    def preprocess(self, s, lowercase=False):
        tokens = self.tokenize(s.lower())
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens


wrangler = Wrangler() 
       
corpus['SentimentText'] = corpus['SentimentText'].apply(wrangler.preprocess)
test['text'] = test['text'].apply(wrangler.preprocess)




# Set values for various parameters
num_features = 300    # Word vector dimensionality                      
min_word_count = 40   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words




########################################################################
#Training and testing with model




model = Word2Vec.load("Sentiment_Analysis_Corpus")



def makeFeatureVec(words, model, num_features):
    featureVec = np.zeros((num_features,),dtype="float32")
    
    nwords = 0.
    index2word_set = set(model.index2word)

    for word in words:
        if word in index2word_set: 
            nwords = nwords + 1.
            featureVec = np.add(featureVec,model[word])

    featureVec = np.divide(featureVec,nwords)
    return featureVec
    
def getAvgFeatureVecs(tweets, model, num_features):

    counter = 0.

    tweetFeatureVecs = np.zeros((len(tweets),num_features),dtype="float32")

    for review in tweets:

       if counter%1000. == 0.:
           print "Review %d of %d" % (counter, len(tweets))

       tweetFeatureVecs[counter] = makeFeatureVec(review, model, num_features)

       counter = counter + 1.
    return tweetFeatureVecs



clean_train_tweets = []
for tweet in corpus['SentimentText']:
    clean_train_tweets.append(tweet)


trainDataVecs = getAvgFeatureVecs(clean_train_tweets, model, num_features)

print "Creating average feature vecs for test tweets"
clean_test_tweets = []

for tweet in test["text"]:
    clean_test_tweets.append(tweet)

testDataVecs = getAvgFeatureVecs(clean_test_tweets, model, num_features)

from sklearn.preprocessing import Imputer

#Vectorize
imp = Imputer(missing_values='NaN', strategy='median', axis=0)
trainDataVecs = imp.fit_transform(trainDataVecs)
testDataVecs = imp.fit_transform(testDataVecs)

# Fit a random forest to the training data, using 100 trees
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier( n_estimators = 100 )

print "Fitting a random forest to labeled training data..."
forest = forest.fit( trainDataVecs, corpus["Sentiment"] )

# Test & extract results 
result = forest.predict( testDataVecs )

# Write the test results 
output = pd.DataFrame( data={"id":test["id"], 
                "id":test["id"],
                "created_at":test["created_at"],
                "favorite_count":test["favorite_count"],
                "text":test["text"],
                "retweet_count":test["retweet_count"],
                "user_name":test["user_name"],
                "user_sentiment":test["user_sentiment"],
                "model_sentiment":result})
output.to_csv( "Word2Vec_AverageVectors.csv", index=False, quoting=3 )