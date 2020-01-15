from twitter import *
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import *
import utils
import numpy as np
import os
import importlib
from xgboost import XGBClassifier
import sys
from ast import literal_eval

def retrieve_user_info(user_list):
    
    config = {'consumer_key': 'LoAQfbNqrofHMZst09Wz2tCPo',
        'consumer_secret': 'nJrk9n80xP7gRff9ZShXMblNkL8sa59y5EC4yOvNRL84SHfzcn',
        'access_token': '716510466336432128-zS6hz5aqe2CRTscBtiFOzbmaPdjgW7s',
        'access_token_secret': 's4K1QT1D05yfvAQ8aVbzgvstx41w1garuqfDeM99VFlkH'}
    
    twitter = Twitter(auth = OAuth(config["access_token"], config["access_token_secret"], config["consumer_key"],
                                   config["consumer_secret"]))

    feat_choices = ['name', 'screen_name', 'statuses_count', 'followers_count',
           'friends_count', 'favourites_count', 'listed_count', 'url', 'lang',
           'time_zone', 'location', 'default_profile', 'default_profile_image',
           'geo_enabled', 'profile_image_url', 'profile_banner_url',
           'profile_use_background_image',
           'profile_background_image_url_https', 'profile_text_color',
           'profile_image_url_https', 'profile_sidebar_border_color',
           'profile_background_tile', 'profile_sidebar_fill_color',
           'profile_background_image_url', 'profile_background_color',
           'profile_link_color', 'utc_offset', 'is_translator',
           'follow_request_sent', 'protected', 'verified', 'notifications',
           'description', 'contributors_enabled', 'following', 'created_at', 'id']

    final_df = pd.DataFrame()
    
    #user_list = literal_eval(user_list)
    user_list = user_list.split(',')

    if isinstance(user_list, basestring):
        try:
            results = twitter.users.search(q = user_list)
            for user in results:
                temp = dict((k.encode('utf-8'), user[k]) for k in user if k in feat_choices)
                for k in temp:
                    if type(temp[k]) == unicode:
                        temp[k] = temp[k].encode('utf-8')

            temp = pd.DataFrame.from_dict(temp, orient='index').transpose()
            final_df = final_df.append(temp)
        except:
            print 'no user information'
      
    else:
        for x in user_list:
            try:
                results = twitter.users.search(q = x)

                for user in results:
                    temp = dict((k.encode('utf-8'), user[k]) for k in user if k in feat_choices)
                    for k in temp:
                        if type(temp[k]) == unicode:
                            temp[k] = temp[k].encode('utf-8')

                temp = pd.DataFrame.from_dict(temp, orient='index').transpose()
                final_df = final_df.append(temp)
            except:
                print 'no user information'
                continue

    return final_df

def classify(in_df):
    
    cresci_dir_2017 = '../data/cresci_2017/'
    cresci_dir_2015 = '../data/cresci_2015/'
    varol = '../data/varol_users/'
    
    real_users_1 = pd.read_csv(os.path.join(cresci_dir_2017, 'genuine_accounts.csv/users.csv'), index_col=0)
    real_users_2 = pd.read_csv(os.path.join(cresci_dir_2015, 'E13/users.csv'), index_col=0)
    real_users_3 = pd.read_csv(os.path.join(cresci_dir_2015, 'TFP/users.csv'), index_col=0)
    real_users_4 = pd.read_csv(os.path.join(varol, 'varol_real.csv'), index_col=0)

    # real_tweets = pd.read_csv(os.path.join(cresci_dir_2017, 'genuine_accounts.csv/tweets.csv'), index_col=0, low_memory=False)
    spam_users_1 = pd.read_csv(os.path.join(cresci_dir_2017, 'social_spambots_1.csv/users.csv'), index_col=0)
    # spam_tweets_1 = pd.read_csv(os.path.join(cresci_dir_2017, 'social_spambots_1.csv/tweets.csv'), index_col=0, low_memory=False)
    spam_users_2 = pd.read_csv(os.path.join(cresci_dir_2017, 'social_spambots_2.csv/users.csv'), index_col=0)
    # spam_tweets_2 = pd.read_csv(os.path.join(cresci_dir_2017, 'social_spambots_2.csv/tweets.csv'), index_col=0, low_memory=False)
    spam_users_3 = pd.read_csv(os.path.join(cresci_dir_2017, 'social_spambots_3.csv/users.csv'), index_col=0)
    # spam_tweets_3 = pd.read_csv(os.path.join(cresci_dir_2017, 'social_spambots_3.csv/tweets.csv'), index_col=0, low_memory=False)
    spam_users_4 = pd.read_csv(os.path.join(cresci_dir_2017, 'traditional_spambots_1.csv/users.csv'), index_col=0)
    # spam_tweets_4 = pd.read_csv(os.path.join(cresci_dir_2017, 'traditional_spambots_1.csv/tweets.csv'), index_col=0, low_memory=False)
    spam_users_5 = pd.read_csv(os.path.join(cresci_dir_2017, 'traditional_spambots_2.csv/users.csv'), index_col=0)
    spam_users_6 = pd.read_csv(os.path.join(cresci_dir_2017, 'traditional_spambots_3.csv/users.csv'), index_col=0)
    spam_users_7 = pd.read_csv(os.path.join(cresci_dir_2017, 'traditional_spambots_4.csv/users.csv'), index_col=0)
    spam_users_8 = pd.read_csv(os.path.join(cresci_dir_2015, 'FSF/users.csv'), index_col=0)
    spam_users_9 = pd.read_csv(os.path.join(cresci_dir_2015, 'INT/users.csv'), index_col=0)
    spam_users_10 = pd.read_csv(os.path.join(cresci_dir_2015, 'TWT/users.csv'), index_col=0)
    spam_users_11 = pd.read_csv(os.path.join(varol, 'varol_fake.csv'), index_col=0)
    
    # Leave spam_user_3 for test
    spam_users_train = pd.concat(objs=[spam_users_1, spam_users_2, spam_users_3, spam_users_4, spam_users_5, spam_users_7,
                                      spam_users_8, spam_users_9, spam_users_10, spam_users_11])
    spam_users_test = spam_users_6

    # Concatenate cresci-2015 real users data
    real_users_train = pd.concat(objs=[real_users_1, real_users_3, real_users_2])
    real_users_test = pd.concat(objs=[real_users_4])
    
    real_users_train.loc[:,'label'] = np.zeros(shape=(real_users_train.shape[0])) 
    real_users_test.loc[:,'label'] = np.zeros(shape=(real_users_test.shape[0]))
    spam_users_test.loc[:,'label'] = np.ones(shape=(spam_users_test.shape[0]))
    spam_users_train.loc[:,'label'] = np.ones(shape=(spam_users_train.shape[0]))

    # concat the genuine users data with the spam data
    train_set = pd.concat([real_users_train, spam_users_train])
    test_set = pd.concat([real_users_test, spam_users_test])
    
    all_data = pd.concat(objs=[train_set, test_set])
    
    feat_choices = ['default_profile', 'default_profile_image', 'favourites_count', 'followers_count',
               'friends_count', 'geo_enabled', 'listed_count', 'profile_use_background_image',
               'statuses_count', 'verified', 'protected', 'profile_background_tile', 'profile_background_color',
               'profile_sidebar_border_color', 'profile_sidebar_fill_color']
    
    features, labels, scaler, feat_names = utils.feat_processing(all_data, feat_choices) 
    in_df['label'] = np.zeros(shape=(in_df.shape[0])) 
    test_features, test_labels = utils.feat_processing(in_df, feat_choices, scaler)

    gb_classifier = XGBClassifier()
    gb_classifier.fit(features, labels)
    prediction = gb_classifier.predict(test_features)

    temp = 0
    for x in prediction:
        if x == 1:
            print '%s is a bot!!' % in_df['screen_name'].iloc[temp]
        else:
            print '%s is a human.' % in_df['screen_name'].iloc[temp]
        temp += 1
        
if __name__ == '__main__':
    in_df = retrieve_user_info(sys.argv[1])
    classify(in_df)