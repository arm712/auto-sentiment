import pandas as pd
import re
import numpy as np
import nltk.data
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
from gensim.models.word2vec import Word2Vec

corpus = pd.read_csv('Sentiment_Analysis_Dataset2.csv', 
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
print corpus.head(5)


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

# Initialize and train the model (this will take some time)
from gensim.models import word2vec
print "Training model..."
model = word2vec.Word2Vec(corpus['SentimentText'], workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

# If you don't plan to train the model any further, calling 
# init_sims will make the model much more memory-efficient.
model.init_sims(replace=True)

# It can be helpful to create a meaningful model name and 
# save the model for later use. You can load it later using Word2Vec.load()
model_name = "Full_Corpus_v1"
model.save(model_name)
