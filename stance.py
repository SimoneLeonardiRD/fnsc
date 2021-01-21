import json
import pandas as pd

with open('data/stance/resultFile.json') as f:
    data = json.load(f)

# print(json.dumps(data, indent=4, sort_keys=True))
# print(data["entities"]["TweetStance"][0]["stance_class"])
# print(data["entities"]["TweetStance"][1]["stance_class"])

list_stance = []

for elem in data["entities"]["TweetStance"]:
    print(elem["stance_class"])
    list_stance.append(elem["stance_class"])

df = pd.read_csv("data/df/fake_uit_0.csv")
df["stance"] = list_stance
df.to_csv("data/stance/fake_uit_stance_0.csv", index=False)

f.close()