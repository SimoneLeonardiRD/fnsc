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
users_id = users_id[10:20]
tu.store_timelines(api, users_id, fout_path, since_id)  # , max_id)


df = pd.read_csv(pathToData+"CoAID/05-01-2020/NewsFakeCOVID-19.csv")
df2 = pd.read_csv(pathToData+"CoAID/07-01-2020/NewsFakeCOVID-19.csv")
df3 = pd.read_csv(pathToData+"CoAID/09-01-2020/NewsFakeCOVID-19.csv")
df4 = pd.read_csv(pathToData+"CoAID/11-01-2020/NewsFakeCOVID-19.csv")
fake_news_list = [df["news_url"], df["news_url2"],
                  df["news_url3"], df["news_url4"],
                  df["news_url5"],
                  df2["news_url"], df2["news_url2"],
                  df2["news_url3"], df2["news_url4"],
                  df2["news_url5"],
                  df3["news_url"], df3["news_url2"],
                  df3["news_url3"], df3["news_url4"],
                  df3["news_url5"],
                  df4["news_url"], df4["news_url2"],
                  df4["news_url3"], df4["news_url4"],
                  df4["news_url5"]]
flat_list = []
for sublist in fake_news_list:
    for item in sublist:
        if pd.isna(item) is False:
            flat_list.append(item)
print(len(flat_list))

dfr = pd.read_csv(pathToData+"CoAID/05-01-2020/NewsRealCOVID-19.csv")
dfr2 = pd.read_csv(pathToData+"CoAID/07-01-2020/NewsRealCOVID-19.csv")
dfr3 = pd.read_csv(pathToData+"CoAID/09-01-2020/NewsRealCOVID-19.csv")
dfr4 = pd.read_csv(pathToData+"CoAID/11-01-2020/NewsRealCOVID-19.csv")
real_news_list = [dfr["news_url"], dfr2["news_url"],
                  dfr3["news_url"], dfr4["news_url"]]
flat_real = []
for sublist in real_news_list:
    for item in sublist:
        if pd.isna(item) is False:
            flat_real.append(item)
print(len(flat_real))

nu.parse_match_count(flat_list, flat_real, users_id)
