from twitter import *
import pandas as pd
import utils
import numpy as np
import os
import io
import time
import sys
import pickle
import json
import TwitterSearch
from ast import literal_eval
from bot_classifier_python3 import *
from second_classifier import *
from sklearn.externals import joblib
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS,cross_origin


# human example: katyperry
# bot example: pixelsorter
# no tweet example:  ChoeStacia

app = Flask(__name__)
CORS(app,resources = {r"/result":{"origins":"*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('/')
# def student():
#    return render_template("index1.html")

@app.route('/result',methods = ['POST', 'GET', 'OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def result():
   #if request.method == 'POST' or request.method == 'OPTIONS':
    result = request.form

    # ImmutableMultiDict([('Name', u'ChoeStacia')]))
    # in_df = retrieve_user_info(result['Name'])
    try:
        test_json = request.get_json()
        test_json = json.dumps(test_json)
        print(test_json)
        test = pd.read_json(test_json, orient='records')
    except Exception as e:
        raise e

    if test.empty:
        return(bad_request())

    in_df = retrieve_user_info(test.values[0][0])
    tweet_df = search_user_wrapper(test.values[0][0])
    bot_or_not, bot_prob = classify_bot_or_not(in_df)
    in_df['bot_or_not'] = bot_or_not
    in_df['bot_prob'] = bot_prob
    
    in_df['ttl_tweet'] = tweet_df.shape[0]
    num_RT, avg_tweet_len = utils.extract_tweet_feats(tweet_df)
    in_df['num_retweet'] = num_RT
    in_df['avg_tweet_len'] = avg_tweet_len
    
    if bot_or_not == 1:
        name = in_df['screen_name'].values[0]
        #in_df = pd.concat([in_df, tweet_info], axis=1)
        # Go to the second classifier
        if tweet_df.shape[0] == 0:
            print('Cannot classify the account because it has no tweet history')
            #predtmp = pd.DataFrame({'response': ['NA(no_tweets)']})
            # bot_profile = pd.DataFrame({'score': [100]})
            # political_profile = pd.DataFrame({'score': [0]})
            bot_profile = {'score': bot_prob}
            political_profile = {'score': 0}
        else:
            print(name, 'is a bot')  
            # rus_bot_prob = classify_political_tweets(tweet_df)
            # rus_bot_prob = np.mean(classify_political_tweets(tweet_df))*100
            rus_bot_prob = classify_political_tweets(tweet_df)
            #in_df['rus_bot_prob'] = rus_bot_prob
            # bot_profile = pd.DataFrame({'score': [100]})
            # political_profile = pd.DataFrame({'score': [rus_bot_prob]})
            bot_profile = {'score': bot_prob}
            political_profile = {'score': rus_bot_prob}
            # predtmp = pd.DataFrame({'score': [bot_or_not], 'probability_russian_bot':[prob_russian]})
    else:
        print(in_df['screen_name'].values[0], 'is a human.')
        # predtmp = pd.DataFrame({'response': ['human'], 'probability_russian_bot':[prob_russian]})
        # bot_profile = pd.DataFrame({'score': [0]})
        # political_profile = pd.DataFrame({'score': [0]})
        bot_profile = {'score': bot_prob}
        political_profile = {'score': 0}
    
    print(bot_profile)
    print(political_profile)    
    
    output_info = {}
    print(in_df)
    output_info["twitter_data"] = in_df.to_dict(orient="records")[0]
    output_info["bot_profile"] = bot_profile
    output_info["political_profile"] = political_profile
    responses = jsonify(output_info)

    return (responses)

if __name__ == '__main__':
   print ("GO TO URL http://18.221.137.114")
   app.run(host="0.0.0.0", port=80, debug=False)
