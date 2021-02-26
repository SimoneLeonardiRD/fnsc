import pandas as pd
df1 = pd.read_csv("generated_data/news_matched/count_0_100.csv")
df2 = pd.read_csv("generated_data/news_matched/count_100_200.csv")
df3 = pd.read_csv("generated_data/news_matched/count_200_500.csv")
rdf1 = pd.read_csv("generated_data/news_matched/count_0_100_real.csv")

frames = [df1, df2, df3, rdf1]

df = pd.concat(frames)

#print(df.head())
print(df.shape)
dfake = df[(df['fake_count'] > df['real_count'])]
#print(dfake)
print(dfake.shape)
dreal = df[(df['fake_count'] < df['real_count'])]
#print(dreal)
print(dreal.shape)
dunkn = df[(df['fake_count'] == df['real_count'])]
#print(dunkn)
print(dunkn.shape)

print(dfake.shape[0]/df.shape[0])
print(dreal.shape[0]/df.shape[0])

print(dfake[['user_id']]) # stampare su file come df
# estrarre lista utenti fake vs (real+ incerti)