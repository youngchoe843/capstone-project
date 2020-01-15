## Import twittersearch API
from TwitterSearch import * ## please `pip install TwitterSearch` if not yet installed 
#import TwitterSearch
import pandas as pd
import numpy as np
import json ## to load json format into dict
import time ## to extract date/time from retrieved data
import utils
import pickle
from keras.models import load_model
import sys 

def search_user(username):
    """
        arg: twitter username
        return: list of tweets
    """
    
    ts = TwitterSearch(
    consumer_key = 'X2SwXG1wIBLJiJRUunqIXyaNz',
    consumer_secret = 'j0mtZ5BvcNE26rdRrySprP3iYhiAglUn8qtzGP5Rw4WXqm1lV8',
    access_token = '41741727-9JoDDAAoTUo47z8Zo8uCQ1t5WLcpWnoQVSrImoB7q',
    access_token_secret = 'dhEDyLezeg22qClu1qrIf3pVadN3n9KOxK8q72bCwvG42')

    try:
        tuo = TwitterUserOrder(username) # create a TwitterUserOrder
        # start asking Twitter about the timeline
        list_output = [] ## store retrieved tweets and their metadata in a list object
        for tweet in ts.search_tweets_iterable(tuo):
            ## extract and split date time into its individual varaiable
            date_output, time_output = utils.date_time_transform(tweet['created_at'])        

            ## extract relevant information from the tweet metadata
            output = [
                #['created_at', tweet['created_at']] ## date/time of tweet
                ['date', date_output]
                ,['time', time_output]
                ,['id_str', tweet['id_str']] ## user id
                ,['text',tweet['text']] ## actual tweet
                ,['user_friends_count', tweet['user']['friends_count']]
                ,['user_followers_count', tweet['user']['followers_count']]
                ,['user_location', tweet['user']['location']]
                ,['user_screen_name', tweet['user']['screen_name']]
                ,['user_verified', tweet['user']['verified']] ## if account is a verified account
                ,['coordinates', tweet['coordinates']]
                ,['retweet_count', tweet['retweet_count']]
                ]
            list_output.append(output)
            
        return list_output

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
        return None
    
def search_user_wrapper(user):

        
    user_results = search_user(user)
    len(user_results)
    
    output = []
    for i in range(len(user_results)):
        tempt = []
        for j in range(len(user_results[i])):
            tempt.append(user_results[i][j][1])
        output.append(tempt)

    ## create columns names
    fields =  ['date', 'time', 'id_str', 'text', 'user_friends_count', 'user_followers_count', 'user_location'
               ,'user_screen_name', 'user_verified','coordinates', 'retweet_count']

    ## transform temp_list into data frame for exportation
    df_output = pd.DataFrame(data = output, columns = fields)

    ## get date/time for 
    date_retrieved, time_retrieved = utils.date_time_transform2(time.ctime())
    file_name = '../data/tweets/search_user_' + user + '_' + str(date_retrieved) + '_' + str(time_retrieved) + '.csv'

#     df_output.to_csv(file_name,  sep = ',', index = False)
    return df_output['text']
    
def classify_political_tweets(in_df):
    tfidf = pickle.load(open('tfidf.dat', 'rb'))
    x = tfidf.transform(in_df)
    
    mlp = load_model('mlp.h5')
    prediction = mlp.predict_classes(x)
   
    return prediction 
    #print('Likelihood of a Russian bot: {0:.2f}%'.format(np.mean(prediction)*100))
    
    
if __name__ == '__main__':
    in_df = search_user_wrapper(sys.argv[1])
    classify_political_tweets(in_df) 
