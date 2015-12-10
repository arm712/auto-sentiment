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
                    dtype=object)
                    

corpus['SentimentText'] = corpus['SentimentText'].astype('str')  
corpus = corpus.dropna(subset=['Sentiment'], how='any')  


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


# Import the built-in logging module and configure it so that Word2Vec 
# creates nice output messages

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

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

# Fit a random forest to the training data, using 100 trees
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier( n_estimators = 100 )


X = trainDataVecs
y = corpus["Sentiment"]

X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2)
rf = forest
rf.fit(X_train,y_train)
y_pred = rf.predict(X_test)

print metrics.accuracy_score(y_test, y_pred), 'train/test split random forest'