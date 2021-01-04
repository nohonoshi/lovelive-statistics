# coding: UTF-8

import tweepy
import pandas as pd
import numpy as np
import datetime as dt
import os

# import tweet member list
member_df = pd.read_csv('member.csv', encoding='utf-8')
key_df = pd.read_csv('api_key.csv', index_col=0)

Consumer_key = key_df.at['Consumer_key', 'Key']
Consumer_secret = key_df.at['Consumer_secret', 'Key']
Access_token = key_df.at['Access_token', 'Key']
Access_secret = key_df.at['Access_secret', 'Key']

os.mkdir('tweets')

# OAuth authentication
auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_secret)
api = tweepy.API(auth)

cols = ['Date', 'Text', 'Favorite']

# This list is used for
pages = np.array(range(1, 17, 1))

for member in member_df['id']:

    print('Collecting tweets of ' + member)

    tweet_df = pd.DataFrame(index=[], columns=cols)

    for page in pages:
        print('.', end='')
        results = api.user_timeline(screen_name=member, count=200, page=page)
        for r in results:
            tmp_se = pd.Series(
                [r.created_at, r.text, r.favorite_count], index=tweet_df.columns)
            tweet_df = tweet_df.append(tmp_se, ignore_index=True)

    tweet_df['Date'] += dt.timedelta(hours=9)

    tweet_df = tweet_df[~tweet_df['Text'].str.startswith(u'RT @')]
    tweet_df.to_csv("tweets\\" + member_df.query('id == @member')
                    ['Name'].values[0] + ".csv", encoding='utf-8')
