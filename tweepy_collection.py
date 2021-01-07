import twitter_utilities as tu
import pandas as pd


pathToTwitterAuthData = "twitterAccess.txt"
pathToDevKeyAndSecret = "consumer_api_keys.txt"
pathToData = "~/Venv/Documents/dataset/CoAID/"
fn = "NewsFakeCOVID-19_tweets.csv"
# fn = "ClaimFakeCOVID-19_tweets.csv"
fake_news = pd.read_csv(pathToData+fn)
print(fake_news.shape)
ids = fake_news[['tweet_id']]
# ids = ids[:10]
print(ids, ids.shape)
api = tu.authentication(pathToDevKeyAndSecret, pathToTwitterAuthData)
# users collection done

users_id = []
fin = open("users_fake_claim.txt", "r")
for line in fin.readlines():
    print(line)
    users_id.append(line.rstrip("\n"))
fout_path = "data/tweet/"

''' retrieving retweetwers from fake news covid tweets
counter = 0
total_retweeters = []
for tweetid in ids['tweet_id']:
    try:
        # for page in tu.limit_handled(tweepy.Cursor(api.retweeters, tweetid).pages()):
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
