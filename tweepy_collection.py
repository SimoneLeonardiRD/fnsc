import twitter_utilities as tu
import pandas as pd
import nlp_utilities as nu


pathToTwitterAuthData = "twitterAccess.txt"
pathToDevKeyAndSecret = "consumer_api_keys.txt"
api = tu.authentication(pathToDevKeyAndSecret, pathToTwitterAuthData)

pathToData = "~/Venv/Documents/dataset/CoAID/"
fn = "NewsFakeCOVID-19_tweets.csv"
# fn = "ClaimFakeCOVID-19_tweets.csv"
fake_news = pd.read_csv(pathToData+fn)
print(fake_news.shape)
ids = fake_news[['tweet_id']]
# ids = ids[:10]
# print(ids, ids.shape)

users_id = []
fin = open("users_fake_news.txt", "r")
for line in fin.readlines():
    users_id.append(line.rstrip("\n"))
fout_path = "data/tweet/"

since_id = fake_news["tweet_id"].min()  # time span matching CoAid
# max_id = fake_news["tweet_id"].max()
print(since_id)  # , max_id)
tu.store_timelines(api, users_id, fout_path, since_id)  # , max_id)

'''
df = pd.read_csv(pathToData+"NewsFakeCOVID-19.csv")
fake_news_list = [df["news_url"], df["news_url2"],
                  df["news_url3"], df["news_url4"],
                  df["news_url5"]]
flat_list = []
for sublist in fake_news_list:
    for item in sublist:
        if pd.isna(item) is False:
            flat_list.append(item)
print(len(flat_list))


nu.parse_match_count(flat_list, users_id)
'''
