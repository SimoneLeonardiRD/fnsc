import pandas as pd
import numpy as np

'''
df1 = pd.read_csv("generated_data/news_matched/count_0_100.csv")
df2 = pd.read_csv("generated_data/news_matched/count_100_200.csv")
df3 = pd.read_csv("generated_data/news_matched/count_200_500.csv")
rdf1 = pd.read_csv("generated_data/news_matched/count_0_100_real.csv")
rdf2 = pd.read_csv("generated_data/news_matched/count_100_500_real.csv")

frames = [df1, df2, df3, rdf1, rdf2]

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
#print(dunkn.shape)

print(dfake.shape[0]/df.shape[0])
print(dreal.shape[0]/df.shape[0])

dfake['label'] = ['1']*dfake.shape[0]
dreal['label'] = ['0']*dreal.shape[0]
dunkn['label'] = ['0']*dunkn.shape[0]

dlab = pd.concat([dfake, dreal, dunkn])
dlab = dlab[['user_id', 'label']]

user_id_fake = np.arange(0, 164, 1)
col = {
        'user_id': [],
        'label': []
    }
dfaddfake = pd.DataFrame(col).astype('object')
dfaddfake['user_id'] = user_id_fake
dfaddfake['label'] = ['1']*dfaddfake.shape[0]
dlab2 = pd.concat([dlab, dfaddfake])
#print(dlab2.shape)
#print(dlab2.head())
#print(dlab2.sample(10))

dlab2.to_csv("user_label.csv", index=False)
# print(dfake[['user_id']]) # stampare su file come df
# estrarre lista utenti fake vs (real+ incerti)
derr = pd.DataFrame(col).astype('object')
for user in dlab2['user_id']:
    dus = pd.read_csv("generated_data/tweet_drive/"+str(user)+".csv")
    if(dus.shape[0] < 50):
        # print("empty", user)
        print(dus.shape[0], user)
        row = {
            'user_id': str(user),
            'label': 0
        }
        derr = derr.append(row, ignore_index=True)

derr.to_csv("user_empty.csv", index=False)
print(dlab2.shape)
print(derr.shape)
cond = dlab2['user_id'].isin(derr['user_id'])
dlab2.drop(dlab2[cond].index, inplace=True)
print(dlab2.head())
#dclean = pd.concat([dlab2, derr]).drop_duplicates(keep=False)
dlab2.to_csv("user_label_clean.csv")
print(dlab2.shape)
'''
'''
df = pd.read_csv("output_test/user_label_clean.csv")
print(df.head())
print(df.shape)
df = df[:624]
user_id = df['user_id']
total_tweet = 0.0
for user in user_id:
    #print(user)
    dfu = pd.read_csv("generated_data/tweet_drive/"+str(user)+".csv")
    total_tweet += dfu.shape[0]
    #print(df.shape[0])
print(str(total_tweet/df.shape[0]))
'''

df = pd.read_csv("generated_data/news_matched/count_200_500.csv")
df1 = df[df['percentage_fake'] > 0]
print(df1.head())
totalf = df['percentage_fake'].sum()
print("fake", str(totalf/df1.shape[0]))
df = pd.read_csv("generated_data/news_matched/count_100_500_real.csv")
df2 = df[df['percentage_real'] > 0]
print(df2.head())
totalr = df['percentage_real'].sum()
print("real", str(totalr/df1.shape[0]))
#rslt_df = dataframe[dataframe['Percentage'] > 80]

#total = df['statuses_count'].sum()
#print(total)
#print(str(total/df.shape[0]))