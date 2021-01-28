import twitter_utilities as tu
import pandas as pd
import nlp_utilities as nu


pathToTwitterAuthData = "twitterAccess.txt"
pathToDevKeyAndSecret = "consumer_api_keys.txt"
api = tu.authentication(pathToDevKeyAndSecret, pathToTwitterAuthData)

pathToData = "~/Venv/Documents/dataset/CoAID/"
outputPath = "data/user/"
output_user_file = "users_real_news.txt"

# fn = "NewsFakeCOVID-19_tweets.csv"
rn = "NewsRealCOVID-19_tweets.csv"
# fake_news = pd.read_csv(pathToData+fn)
real_news = pd.read_csv(pathToData+rn)
print(real_news.shape)
# ids = fake_news[['tweet_id']]
ids = real_news[['tweet_id']]
ids = ids[5000:10000]
tu.store_users(api, ids, outputPath+output_user_file)
'''
users_id = []
fin = open("users_fake_news.txt", "r")
for line in fin.readlines():
    users_id.append(line.rstrip("\n"))
fout_path = "data/tweet/"

since_id = fake_news["tweet_id"].min()  # time span matching CoAid
# max_id = fake_news["tweet_id"].max()
print(since_id)  # , max_id)
users_id = users_id[:200]
#tu.store_timelines2(api, users_id, fout_path, since_id)  # , max_id)
#print("timelines stored")

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
df_fake_news = df_fake_news.fillna('0').astype('object')
df_real_news = df_real_news.fillna('0').astype('object')
nu.parse_match_count(df_fake_news, df_real_news, users_id)

df_detected = pd.read_csv("data/df/fake_uit_0.csv")
nu.stance_detection_create_file(
    df_fake_news.fillna('0'), df_detected, fake=True)
'''