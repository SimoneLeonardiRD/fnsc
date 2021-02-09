import requests
import json
import nlp_utilities as nu
import pandas as pd
from requests.auth import HTTPDigestAuth

# apikeyid1 = "gcjw87o39vjf"
# apipsw1 = "mui1ybrv21qnftw58ore"
apikeyid2 = "gcto8k0olyke"
apipsw2 = "qo45xliqhwf74dushhth"

fin = open("gate_cloud.txt","r")

#url_old = "https://cloud-api.gate.ac.uk/process-document/stance-classification-multilingual?key=gcjw87o39vjf&key=mui1ybrv21qnftw58ore"
url = "https://cloud-api.gate.ac.uk/process-document/stance-classification-multilingual"

headers = {
    'content-type': 'text/plain',
    'Accept':'application/gate+json'
}

tot_line = []
counter = 0
for line in fin.readlines():
    if len(line) == 1:  # empty lines
        continue
    tot_line.append(nu.clean_newline_and_tab(line))
    print(nu.clean_newline_and_tab(line))
    counter += 1


print(counter)
print(tot_line[0] + tot_line[1])
print(len(tot_line))
list_stance = []

for i in range(len(tot_line)):
    print(i)
    if ((i % 2) == 1):
        continue
    else:
        body = tot_line[i] + tot_line[i+1]
        r = requests.post(url, auth=HTTPDigestAuth(apikeyid2, apipsw2), data=body.encode('utf-8'), headers=headers)
        list_stance.append(
            nu.parse_stance_result_from_list(
                nu.requests.models.Response.json(r)))

print(list_stance)
print(len(list_stance))

'''
df = pd.read_csv("generated_data/news_matched/fake_uit_0_100.csv")  # "data/df/fake_uit_0.csv"
df["stance"] = list_stance
df.to_csv("generated_data/stance_fake_uit_0_100.csv", index=False)  # "data/stance/fake_uit_stance_0.csv"
'''
