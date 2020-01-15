from twitter import *
import pandas as pd
import utils
import numpy as np
import os
import sys
import pickle
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
           'geo_enabled', 'profile_image_url',
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

    for x in user_list:
        results = twitter.users.search(q = x)
        temp = [results[0][x] for x in feat_choices]
        temp = pd.DataFrame(temp).transpose()
        temp.columns = np.array(feat_choices)
        final_df = final_df.append(temp)

    return final_df


def classify_bot_or_not(in_df):
    
    classifier = pickle.load(open('bot_classifier.dat', 'rb'), encoding='latin1')
    
    feat_choices = ['default_profile', 'default_profile_image', 'favourites_count', 'followers_count',
           'friends_count', 'geo_enabled', 'listed_count', 'profile_use_background_image',
           'statuses_count', 'verified', 'protected', 'profile_background_tile', 'profile_background_color',
           'profile_sidebar_border_color', 'profile_sidebar_fill_color']
    in_df['label'] = np.zeros(shape=(in_df.shape[0])) 
    
    # Load standard scalar sklearn
    scaler = pickle.load(open('standardscaler.dat', 'rb'), encoding='latin1')
    test_features, test_labels = utils.feat_processing(in_df, feat_choices, scaler)

    prediction = classifier.predict(test_features)
    
    return prediction
if __name__ == '__main__':
    in_df = retrieve_user_info(sys.argv[1])
    prediction = classify_bot_or_not(in_df)
    if prediction == 1:
        print(in_df['screen_name'], 'is a bot!!')
    else:
        print(in_df['screen_name'], 'is a human.')

    
