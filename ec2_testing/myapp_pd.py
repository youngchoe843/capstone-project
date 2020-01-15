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
    classifier = pickle.load(open('bot_classifier.dat', 'rb'), encoding='latin1')

    feat_choices = ['name', 'screen_name', 'statuses_count', 'followers_count','description','created_at',
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
    in_df['label'] = np.zeros(shape=(in_df.shape[0]))

    # Load standard scalar sklearn
    scaler = pickle.load(open('standardscaler.dat', 'rb'), encoding='latin1')
    test_features, test_labels = utils.feat_processing(in_df, feat_choices, scaler)
    prediction = classifier.predict(test_features)

    output_info = {}
    output_info["twitter_data"] = in_df.to_dict(orient="records")[0]
    final_predictions = pd.DataFrame()
    if prediction == 1:
        name = in_df['screen_name'].values[0]
	# Go to the second classifier
        in_df = search_user_wrapper(result['Name'])
        if in_df.shape[0] == 0:
            print('Cannot classify the account because it has no tweet history')
            predtmp = pd.DataFrame({'response': ['NA(no_tweets)']})
        else:
            print(name, 'is a bot!!')
            prob_russian = np.mean(classify_political_tweets(in_df))*100
            predtmp = pd.DataFrame({'response': ['bot'], 'probability_russian_bot':[prob_russian]})

    else:
        print(in_df['screen_name'].values[0], 'is a human.')
        predtmp = pd.DataFrame({'response': ['human']})
	
    final_predictions = final_predictions.append(predtmp)
    output_info["predictions"] = predtmp.to_dict(orient="records")[0]
    # return render_template("result.html", output_info=output_info)
    responses = jsonify(output_info)
    return (responses)


if __name__ == '__main__':
   print ("GO TO URL http://18.221.137.114")
   app.run(host="0.0.0.0", port=80, debug=False)
