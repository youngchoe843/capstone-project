from bot_classifier_python3 import *
from second_classifier import *
import utils

if __name__ == '__main__':
    
    in_df = retrieve_user_info(sys.argv[1])
    tweet_df = search_user_wrapper(sys.argv[1])
    bot_or_not = classify_bot_or_not(in_df)
    in_df['bot_or_not'] = bot_or_not
    
    num_RT, avg_tweet_len = utils.extract_tweet_feats(tweet_df)
    in_df['num_retweet'] = num_RT
    in_df['avg_tweet_len'] = avg_tweet_len
    
    if bot_or_not == 1:
        name = in_df['screen_name'].values[0]
        #in_df = pd.concat([in_df, tweet_info], axis=1)
        # Go to the second classifier
        if tweet_df.shape[0] == 0:
            print('Cannot classify the account because it has no tweet history')
        else:
            print(name, 'is a bot!!')  
            rus_bot_prob = classify_political_tweets(tweet_df)
            in_df['rus_bot_prob'] = rus_bot_prob
    else:
        print(in_df['screen_name'].values[0], 'is a human.')
        
    in_df.to_csv('user_info_results.csv')
    