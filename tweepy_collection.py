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
users_id = users_id[2:10]
# tu.store_timelines2(api, users_id, fout_path, since_id)  # , max_id)


df = pd.read_csv(pathToData+"CoAID/05-01-2020/NewsFakeCOVID-19.csv")
df2 = pd.read_csv(pathToData+"CoAID/07-01-2020/NewsFakeCOVID-19.csv")
df3 = pd.read_csv(pathToData+"CoAID/09-01-2020/NewsFakeCOVID-19.csv")
df4 = pd.read_csv(pathToData+"CoAID/11-01-2020/NewsFakeCOVID-19.csv")
frames = [df, df2, df3, df4]
df_fake_news = pd.concat(frames, ignore_index=True)
dfr = pd.read_csv(pathToData+"CoAID/05-01-2020/NewsRealCOVID-19.csv")
dfr2 = pd.read_csv(pathToData+"CoAID/07-01-2020/NewsRealCOVID-19.csv")
dfr3 = pd.read_csv(pathToData+"CoAID/09-01-2020/NewsRealCOVID-19.csv")
dfr4 = pd.read_csv(pathToData+"CoAID/11-01-2020/NewsRealCOVID-19.csv")
framesr = [dfr, dfr2, dfr3, dfr4]
df_real_news = pd.concat(framesr, ignore_index=True)
nu.parse_match_count(df_fake_news, df_real_news, users_id)
'''
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

print(df.shape, df2.shape, df3.shape, df4.shape)
frames = [df, df2, df3, df4]

result = pd.concat(frames, ignore_index=True)
print(result.shape)

detected = pd.read_csv("fake_uit.csv")

#print(detected.head())
#print(result["title"])


result = result.fillna('0')

df = df.fillna('0')
nu.stance_detection_create_file(df, detected, fake=True)
'''