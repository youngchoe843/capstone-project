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
    # new_profile_image = str(str(in_df['profile_image_url'][0])[:-10] + '400x400.jpg')
    new_profile_image = 'https://twitter.com/' + in_df['screen_name'][0] + '/profile_image?size=original'
    in_df['profile_image_url'] = new_profile_image
    in_df['bot_or_not'] = bot_or_not
    in_df['bot_prob'] = bot_prob
    
    in_df['ttl_tweet'] = tweet_df.shape[0]
    num_RT, avg_tweet_len = utils.extract_tweet_feats(tweet_df)
    in_df['num_retweet'] = num_RT
    in_df['avg_tweet_len'] = avg_tweet_len

    top_words = utils.extract_top_words(tweet_df, 5)
    in_df['word1'],in_df['word2'],in_df['word3'],in_df['word4'],in_df['word5'] = top_words

    top_words_count = utils.extract_top_words_count(tweet_df, 5)
    in_df['word1_count'],in_df['word2_count'],in_df['word3_count'],in_df['word4_count'],in_df['word5_count'] = top_words_count
    
    latest_tweets = tweet_df[0:5]
    in_df['tweets1'],in_df['tweets2'],in_df['tweets3'],in_df['tweets4'],in_df['tweets5'] = latest_tweets

    in_df['political_score'] = 0
    # temp = [0]
    # columns = ["score"]
    bot_profile = pd.DataFrame([0], columns= ["score"])
    political_profile = pd.DataFrame([0], columns= ["score"])
    
    if bot_or_not == 1:
        name = in_df['screen_name'].values[0]
        #in_df = pd.concat([in_df, tweet_info], axis=1)
        # Go to the second classifier
        if tweet_df.shape[0] == 0:
            print('Cannot classify the account because it has no tweet history')
            in_df['error'] = "No Profile"

        else:
            print(name, 'is a bot')  
            rus_bot_prob = classify_political_tweets(tweet_df)
            in_df['error'] = "Profile"
            in_df['political_profile'] = rus_bot_prob
            if rus_bot_prob >= 0.4:
                in_df['political_profile'] = "High"
            elif rus_bot_prob < 0.4 and bot_prob > 0.2:
                in_df['political_profile'] = "Medium"
            else:
                in_df['political_profile'] = "Low"
    else:
        print(in_df['screen_name'].values[0], 'is a human.')
        in_df['error'] = "Profile"
        in_df['political_score'] = 0
        in_df['political_profile'] = "Low"

    output_info = {}
    output_info["twitter_data"] = in_df.to_dict(orient="records")[0]
    print(output_info)
    responses = jsonify(output_info)

    return (responses)

if __name__ == '__main__':
   print ("GO TO URL http://18.221.137.114")
   app.run(host="0.0.0.0", port=80, debug=False)
