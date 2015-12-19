import pandas as pd
import re
import numpy as np
import sys
import string
import nltk.data
from nltk.corpus import stopwords
from gensim.models.word2vec import Word2Vec
import logging
from sklearn.cross_validation import train_test_split
from sklearn.metrics import average_precision_score
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier

##########################
#Initial
##########################

#Provides countdown of Word2vec model building progress
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

reload(sys)
sys.setdefaultencoding("utf8")

#Word2Vec parameters
num_features = 200    # Word vector dimensionality                      
min_word_count = 5   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words

##########################
####### Methods
#########################

#Method for cleaning text
class Wrangler(object):

    def __init__(self):
        punctuation = list(string.punctuation)
        self.stop = stopwords.words('english') + punctuation + ['url', 'URL']
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
        tokens_stop = [token for token in tokens if token not in self.stop]
        return tokens

#Vectorization methods
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

    for tweet in tweets:

       if counter%1000. == 0.:
           print "Tweet %d of %d" % (counter, len(tweets))

       tweetFeatureVecs[counter] = makeFeatureVec(tweet, model, num_features)

       counter = counter + 1.
    return tweetFeatureVecs

###############################################    
######### Import data
###############################################

#Import main corpus for model
corpus = pd.read_csv('Sentiment_Analysis_Dataset.csv', 
                    index_col=0, 
                    dtype=object)                    


#Import updated small corpus for that day
small_corpus = pd.read_csv('Sentiment_Analysis_Dataset_Calibrated_Date.csv', 
                    index_col=0, 
                    dtype=object)                    

#Import ingested tweets for that day 
with open('Date.json') as f:
    data = f.readlines()
data = map(lambda x: x.rstrip(), data)
data_json_str = "[" + ','.join(data) + "]"
test = pd.read_json(data_json_str)

#################################
######## Main
###############################

#Clean and tokenize all text
wrangler = Wrangler() 

corpus['SentimentText'] = corpus['SentimentText'].astype('str')  
corpus = corpus.dropna(subset=['Sentiment'], how='any')
corpus['SentimentText'] = corpus['SentimentText'].apply(wrangler.preprocess)

small_corpus['SentimentText'] = small_corpus['SentimentText'].astype('str') 
small_corpus = small_corpus.dropna(subset=['Sentiment'], how='any')
small_corpus['SentimentText'] = small_corpus['SentimentText'].apply(wrangler.preprocess)

test['text'] = test['text'].apply(str)  
test['text'] = test['text'].apply(wrangler.preprocess)

# Initialize and train the model 
print "Training model..."
model = word2vec.Word2Vec(corpus['SentimentText'], workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)


model.init_sims(replace=True)

model_name = "Trained_Model_Annotated"
model.save(model_name)

#Vectorization
model = Word2Vec.load("Trained_Model_Annotated")

print "Creating average feature vecs for small corpus tweets"
clean_train_tweets = []
for tweet in small_corpus['SentimentText']:
    clean_train_tweets.append(tweet)

trainDataVecs = getAvgFeatureVecs(clean_train_tweets, model, num_features)

print "Creating average feature vecs for ingested tweets"
clean_test_tweets = []
for tweet in test["text"]:
    clean_test_tweets.append(tweet)

testDataVecs = getAvgFeatureVecs(clean_test_tweets, model, num_features)

imp = Imputer(missing_values='NaN', strategy='median', axis=0)
trainDataVecs = imp.fit_transform(trainDataVecs)
testDataVecs = imp.fit_transform(testDataVecs)


# Random Forest Classification

forest = RandomForestClassifier( n_estimators = 100 )

print "Fitting a random forest to labeled training data..."
forest = forest.fit( trainDataVecs, corpus["Sentiment"] )
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
output.to_csv("Date.csv", 
                index=False, 
                cols=('_id','created_at','favorite_count', \
                'model_sentiment', 'retweet_count', 'text', \
                'user_name', 'user_sentiment'))
                
#Assess corpus accuracy
X = trainDataVecs
Y = corpus["Sentiment"]

X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2)
rf = forest
rf.fit(X_train,y_train)
y_pred = rf.predict(X_test)
y_test = map(int, y_test)
y_pred = map(int, y_pred)

print metrics.accuracy_score(y_test, y_pred), ' accuracy of train/test split random forest'
print metrics.roc_curve(y_test, y_pred, pos_label=1), 'ROC curve on random forest'
print roc_auc_score(y_test, y_pred), 'ROC AUC curve on random forest'
print average_precision_score(y_test, y_pred), 'average precision curve on random forest'
print matthews_corrcoef(y_test, y_pred) , 'matthews correlation coefficient on random forest'  



















