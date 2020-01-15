
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


# human example: katyperry
# bot example: pixelsorter
# no tweet example:  ChoeStacia

app = Flask(__name__)

@app.route('/')
def student():
   return render_template("index1.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form

      # ImmutableMultiDict([('Name', u'ChoeStacia')]))
      in_df = retrieve_user_info(result['Name'])

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
      return render_template("result.html", output_info=output_info)


if __name__ == '__main__':
   print ("GO TO URL http://18.221.137.114")
   app.run(host="0.0.0.0", port=80, debug=False)
