import pandas as pd

users_id = []
fin = open("generated_data/user/users_fake_news.txt", "r")
for line in fin.readlines():
    users_id.append(line.rstrip("\n"))

users_id = users_id[:10]
counter = 0
frames = []
for user in users_id:
    counter += 1
    try:
        df = pd.read_csv("generated_data/tweet/"+str(user)+".csv")   
        df = df.drop(columns=['user_id', 'text'])
        df['label'] = ['1']*df.shape[0]
        df['user_mapped_id'] = [str(counter)]*df.shape[0]
        df = df.reindex(columns=['user_mapped_id', 'tweet_id', 'label'])
        # print(df.head)
        frames.append(df)
    except FileNotFoundError:
        continue

result = pd.concat(frames)
print(result.shape)
result.to_csv('coaid_ext_fake.csv', index=False)