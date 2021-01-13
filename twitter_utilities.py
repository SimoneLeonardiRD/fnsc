import tweepy
import os
import time
from pathlib import Path


def authentication(pathToDevKeyAndSecret, pathToTwitterAuthData):
    try:
        f = open(pathToDevKeyAndSecret, "r")
        # retrieving key and secret in a local file, not available on github
        # ask this info to the developer of the app
    except IOError:
        print("file with key and secret of Twitter app not found")
        print("ask to the developer\n")
        exit()
    else:
        print("file opening and information retrieving")

    # read my developer app key and secret from local file .gitignore
    consumer_key = f.readline().rstrip('\n')
    consumer_secret = f.readline().rstrip('\n')
    f.close()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    twitterAuthData = Path(pathToTwitterAuthData)  # here we find key and
    # secret of the user using the app on Twitter
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
        # already got auth data, read it from file
        twitterAuthData = open(pathToTwitterAuthData, "r")
        access_token = twitterAuthData.readline().rstrip('\n')
        access_token_secret = twitterAuthData.readline().rstrip('\n')
        twitterAuthData.close()

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print('Authentication completed with success')
    return api


def create_all_necessary_folders(pathToDataFolder, topic_selected):
    # --Create the Data collection folder if not exists--#
    if not os.path.exists(pathToDataFolder):
        os.makedirs(pathToDataFolder)


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
            # print(code_err)
            if int(code_err) == 401:
                return
            if int(code_err) == 429:
                print("Sleeping")
                time.sleep(15*60)
        except StopIteration:
            return


def store_users(api, ids):
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
    fout = open("users_fake_news.txt", "a")
    for user in users_from_tweetids:
        fout.write(str(user)+"\n")


def store_timelines(api, users_id, fout_path, since_id):  # , max_id):
    counter = 0
    for user in users_id[12:20]:
        print(str(counter))
        counter += 1
        fout = open(fout_path+str(user), "w")
        for status in limit_handled(tweepy.Cursor(api.user_timeline,
                                    user_id=user, since_id=since_id).items()):
            # max_id=max_id
            fout.write(str(status.id)+"\t")
            new_tweet = ""
            tweet_cleaned = status.text.split("\n")
            for sintagma in tweet_cleaned:
                new_tweet = new_tweet + " " + sintagma
            new_tweet2 = ""
            tweet_cleaned2 = new_tweet.split("\t")
            for sintagma2 in tweet_cleaned2:
                new_tweet2 = new_tweet2 + " " + sintagma2
            fout.write(new_tweet2 + "\n")
        fout.close()


''' retrieving retweetwers from fake news covid tweets
counter = 0
total_retweeters = []
for tweetid in ids['tweet_id']:
    try:
        # for page in tu.limit_handled(tweepy.Cursor(
        #                              api.retweeters, tweetid).pages()):
        #    print(page)
        retweeters_100 = api.retweeters(int(tweetid))
        print(retweeters_100)
        if len(retweeters_100) > 0:
            counter = counter + 1
            for user_id in retweeters_100:
                total_retweeters.append(user_id)
    except tweepy.RateLimitError:
        time.sleep(15*60)
    except tweepy.TweepError as e:
        print(e)
print(str(counter))
fout = open("retweeters.txt", "a")
# fout = open("claim_retweeters.txt", "w")
for user in total_retweeters:
    fout.write(str(user)+"\n")
'''

'''
retweeters_df = pd.read_csv("retweeters.txt", header=None)
print(retweeters_df)
retweeters_df.columns = ['user_id']
print(retweeters_df, retweeters_df.shape)
retweeters = retweeters_df['user_id']
duplicated = retweeters_df[retweeters_df.duplicated(['user_id'])]
duplicated = pd.unique(duplicated['user_id'])
print("duplicated", duplicated)
retweeters = pd.unique(retweeters)
print("len retweeters", len(retweeters))
retweeters = retweeters[:10]
print("retweeters", retweeters)
print(len(duplicated))
duplicated = duplicated[2:]
tu.retrieve_and_store_tweet_tab_back("./retweeters_timeline/", duplicated, api)
# moved to hpc
'''
