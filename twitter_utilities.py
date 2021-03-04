import tweepy
import os
import time
from pathlib import Path
import pandas as pd


def authentication(pathToDevKeyAndSecret, pathToTwitterAuthData):
    try:
        f = open(pathToDevKeyAndSecret, "r")
    except IOError:
        print("file with key and secret of Twitter app not found")
        print("ask to the developer or register your app\n")
        exit()

    consumer_key = f.readline().rstrip('\n')
    consumer_secret = f.readline().rstrip('\n')
    f.close()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    twitterAuthData = Path(pathToTwitterAuthData)  
    if(not twitterAuthData.is_file() or
       os.stat(pathToTwitterAuthData).st_size == 0):
        # no previous authentication data, need to autenthicate via browser
        try:
            redirect_url = auth.get_authorization_url()
            print("Redirect url:", redirect_url)
        except tweepy.TweepError:
            print('Error! Failed to get request token.')

        verifier = input('Verifier:')
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print('Error! Failed to get access token.')

        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        twitterAuthData = open(pathToTwitterAuthData, "w")
        twitterAuthData.write(auth.access_token+"\n" +
                              auth.access_token_secret+"\n")
        twitterAuthData.close()

    else:
        twitterAuthData = open(pathToTwitterAuthData, "r")
        access_token = twitterAuthData.readline().rstrip('\n')
        access_token_secret = twitterAuthData.readline().rstrip('\n')
        twitterAuthData.close()

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print('Authentication completed with success')
    return api


def limit_handled(cursor):
    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError:
            print("Sleeping")
            time.sleep(15*60)
        except tweepy.TweepError as e:
            print(e)
            code_elem = str(e).split(" ")
            code_err = code_elem[-1]
            if code_err == '429':
                print("Sleeping")
                time.sleep(15*60)
            else:
                return
        except StopIteration:
            return


def store_users(api, ids, output_file):
    print("Searching users...\n")
    users_from_tweetids = []
    for tweetid in ids['tweet_id']:
        try:
            status = api.get_status(int(tweetid), trim_user=True)
            users_from_tweetids.append(status.user.id)
        except tweepy.RateLimitError:
            print("sleeping")
            time.sleep(15*60)
        except tweepy.TweepError as e:
            print(e)
            continue

    users_from_tweetids = set(users_from_tweetids)
    users_from_tweetids = list(users_from_tweetids)
    fout = open(output_file, "a")
    for user in users_from_tweetids:
        fout.write(str(user)+"\n")
    print("All users stored\n")


def store_timelines_as_txt_cleaned(api, users_id, fout_path, since_id):
    counter = 0
    for user in users_id:
        print(str(counter))
        counter += 1
        fout = open(fout_path+str(user), "w")
        for status in limit_handled(tweepy.Cursor(api.user_timeline,
                                    user_id=user, since_id=since_id,
                                    tweet_mode="extended").items()):
            fout.write(str(status.id)+"\t")
            if (status.full_text.startswith("RT @") is True):
                try:
                    status = status.retweeted_status
                except:
                    status = status
            new_tweet = ""
            tweet_cleaned = status.full_text.split("\n")
            for sintagma in tweet_cleaned:
                new_tweet = new_tweet + " " + sintagma
            new_tweet2 = ""
            tweet_cleaned2 = new_tweet.split("\t")
            for sintagma2 in tweet_cleaned2:
                new_tweet2 = new_tweet2 + " " + sintagma2
            fout.write(new_tweet2 + "\n")
        fout.close()


def store_timelines_as_df(api, users_id, fout_path, since_id):
    print("Collecting users timelines since " + str(since_id) + "\n")
    counter = 1
    for user in users_id:
        try:
            open(fout_path+str(user)+".csv", "r")
            print("already downloaded")
            continue
        except FileNotFoundError:
            print("new user")
        print(str(counter)+"/"+str(len(users_id)))
        counter += 1
        data = {'user_id': [],
                'tweet_id': [],
                'text': []
                }
        df = pd.DataFrame(data)
        for status in limit_handled(tweepy.Cursor(api.user_timeline,
                                    user_id=user, since_id=since_id,
                                    tweet_mode="extended").items()):
            if (status.full_text.startswith("RT @") is True):
                try:
                    status = status.retweeted_status
                except:
                    status = status
            new_row = {
                'user_id': str(user),
                'tweet_id': str(status.id),
                'text': status.full_text
            }
            df = df.append(new_row, ignore_index=True)
        df.to_csv(fout_path+str(user)+".csv", index=False)
    print("Collection completed\n")
