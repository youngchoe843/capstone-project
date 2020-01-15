import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
import re
import time
import numpy as np
import operator

def date_time_transform(date_time):
    date_time_deconstruct = time.strptime(date_time, "%a %b %d %H:%M:%S +0000 %Y")
    date_output = str(date_time_deconstruct.tm_year) + '/' + str(date_time_deconstruct.tm_mon) + '/' + str(date_time_deconstruct.tm_mday)
    time_output = str(date_time_deconstruct.tm_hour) + ':' + str(date_time_deconstruct.tm_min)
    return date_output, time_output

def date_time_transform2(date_time):
    date_time_deconstruct = time.strptime(date_time, "%a %b %d %H:%M:%S %Y")
    date_output = str(date_time_deconstruct.tm_year) + str(date_time_deconstruct.tm_mon) + str(date_time_deconstruct.tm_mday)
    time_output = str(date_time_deconstruct.tm_hour) + str(date_time_deconstruct.tm_min)
    return date_output, time_output

def extract_top_words(tweet_df, num_words=5):
    # Construct stop words
    stop_words = []
    f = open('english2.txt', 'r')
    for line in f.readlines():
        stop_words.append(line.strip())
    
    stop_words.extend(['https','amp','rt','co','just','much','back','will','one','can','day','many','get','http','now',
                   're','ur','go','also','ly','com','us'])
    cv =CountVectorizer(stop_words=stop_words)
    temp=cv.fit_transform(tweet_df.astype(str).str.lower())
    most_freq_idx = np.argsort(np.asarray(np.sum(temp.todense(),axis=0))[0])[-num_words:][::-1]
    out = []
    for i in most_freq_idx:
        out.append(cv.get_feature_names()[i])

   
    return out

def extract_top_words_count(tweet_df, num_words=5):
    # Construct stop words
    stop_words = []
    f = open('english2.txt', 'r')
    for line in f.readlines():
        stop_words.append(line.strip())
    
    stop_words.extend(['https','amp','rt','co','just','much','back','will','one','can','day','many','get','http','now',
                   're','ur','go','also','ly','com','us'])
    cv =CountVectorizer(stop_words=stop_words)
    temp=cv.fit_transform(tweet_df.astype(str).str.lower())
    # most_freq_idx = np.argsort(np.asarray(np.sum(temp.todense(),axis=0))[0])[-num_words:][::-1]
    # out = []
    # for i in most_freq_idx:
    #     out.append(cv.get_feature_names()[i])

    # tags = cv.vocabulary_
    # sorted_tags = sorted(tags.items(), key=operator.itemgetter(1))
    counts = np.sort(np.asarray(np.sum(temp.todense(),axis=0))[0])[-num_words:][::-1]
    # print(sorted_tags[0:5])

    return counts 

def extract_tweet_feats(all_tweets):
    all_tweets = all_tweets.fillna(0)
    # Capture how often a tweet contains retweet
    contain_RT = pd.to_numeric(all_tweets.str.contains('RT'))
    num_RT = contain_RT.sum()
    # Capture an average tweet length
    tweet_len = all_tweets.str.len()
    avg_tweet_len = tweet_len.mean()

    # Average of all tweets
    #avg_tweets = all_tweets.mean()
    return num_RT, avg_tweet_len

def clean_tweets(tweet_df):
    #tweet_df = tweet_df.apply(lambda x: x.lower())
    #tweet_df = tweet_df.apply(lambda row: re.findall('[\w]+', row))
    #tweet_df = tweet_df.str.replace(r'[0-9]+','')
    #tweet_df = tweet_df.str.replace(r'_','')
    #tweet_df = tweet_df.str.replace(r' [a-zA-Z] ',' ')
    #tweet_df = tweet_df.str.replace(r'http','')
    return tweet_df
    
def feat_processing(all_users, feat_choices, scaler=None):
    # Feature selection
    features = all_users.loc[:, feat_choices]
    labels = all_users['label']
    
    # Capture whether an account has language profile
    if 'lang' in feat_choices:
        features.loc[:,'lang'] = all_users.loc[:,'lang'].isnull()
        
    # Capture whether an account has location
    if 'location' in feat_choices:
        features.loc[:,'location'] = all_users.loc[:,'location'].isnull()
        
    if 'profile_background_color' in feat_choices:
        features.loc[:,'profile_background_color'] = all_users['profile_background_color'].str.match('0000FF')
        
    if 'profile_sidebar_border_color' in feat_choices:
        features.loc[:, 'spam_sidebar_color'] = all_users['profile_sidebar_border_color'].str.match('C0DEED')
        features.loc[:, 'real_sidebar_color'] = all_users['profile_sidebar_border_color'].str.match('000000')
        features.drop('profile_sidebar_border_color', axis=1, inplace=True)
        
    if 'profile_banner_url' in feat_choices:
        features.loc[:, 'profile_banner_url'] = all_users['profile_banner_url'].isnull()
        
    if 'profile_sidebar_fill_color' in feat_choices:
        features.loc[:,'profile_sidebar_fill_color'] = all_users['profile_background_color'].str.match('DDEEF6')
    
    feat_names = features.columns
    
    # Average tweet length
    # Fill na to zero
    features = features.fillna(0)

    # Standardize features
    if scaler is None:
        # Train a standard scaler
        scaler = StandardScaler()
        features = scaler.fit_transform(features)
        return features, labels, scaler, feat_names
    else:
        features = scaler.transform(features)
        return features, labels

class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])
    
class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of 
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec[w] * self.word2weight[w]
                         for w in words if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])