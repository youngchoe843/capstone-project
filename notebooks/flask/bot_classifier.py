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
            if (temp.loc[:,'screen_name'] == x).bool():
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

                if (temp.loc[:,'screen_name'] == x).bool():
                    final_df = final_df.append(temp)
                else:
                    print 'Unable to retrieve user: %s' % x
            except:
                print 'no user information'
                continue

    return final_df


def classify(in_df):
    
    classifier = pickle.load(open('bot_classifier.dat', 'rb'))
    
    feat_choices = ['default_profile', 'default_profile_image', 'favourites_count', 'followers_count',
           'friends_count', 'geo_enabled', 'listed_count', 'profile_use_background_image',
           'statuses_count', 'verified', 'protected', 'profile_background_tile', 'profile_background_color',
           'profile_sidebar_border_color', 'profile_sidebar_fill_color']
    in_df['label'] = np.zeros(shape=(in_df.shape[0])) 
    
    # Load standard scalar sklearn
    scaler = pickle.load(open('standardscaler.dat', 'rb'))
    test_features, test_labels = utils.feat_processing(in_df, feat_choices, scaler)

    prediction = classifier.predict(test_features)
    
    for x in range(len(prediction)):
        if prediction[x] == 1:
            print '%s is a bot!!' % in_df['screen_name'].iloc[x]
        else:
            print '%s is a human.' % in_df['screen_name'].iloc[x]
            
if __name__ == '__main__':
    in_df = retrieve_user_info(sys.argv[1])
    classify(in_df)            
    