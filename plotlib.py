import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def kl_divergence(p, q):
    return (p*np.log(p/q)).sum()


def plot_dist(df, out_path, name):
    bins = 1024
    frequency = 150
    trait_name = ["Openness",
                  "Conscentiousness",
                  "Extraversion",
                  "Agreableness",
                  "Neuroticism"]
    o = df["o"]
    c = df["c"]
    e = df["e"]
    a = df["a"]
    n = df["n"]
    pos = 0
    ocean = [o, c, e, a, n]
    for trait in ocean:
        plt.title(str(trait_name[pos])+ " "+ str(name))
        plt.hist(trait, bins=bins, range=(1, 5))
        plt.ylabel("frequency")
        plt.xlabel("score")
        plt.axis([1, 5, 0, frequency])
        plt.grid()
        plt.draw()
        plt.savefig(str(out_path)+"distribution_"+str(trait_name[pos])+'.png', dpi=100)
        # plt.show()
        plt.close()
        pos = pos + 1


def statistics():
    df = pd.read_csv("ceo_tw_big5_01.csv", lineterminator='\n')
    print(df.shape, df.columns)
    fo = open("stat01.txt", "w")
    fo.write("Number of tweets: " + str(df.shape[0]) + "\n")
    res = df[['screenName', 'id_T']]\
        .groupby(['screenName'])\
        .agg(['count'])
    # print(res)
    # print(res.shape)
    # print(res.columns)
    fo.write("Number of authors: " + str(res.shape[0]) + "\n")
    fo.write("Avg tweet per author: " + str(res["id_T"].mean()))
    # print(df["o"].max(), df["o"].min(), df["o"].mean())
    fo.write("Openness max min std avg: " + str(df["o"].max()) + " "
             + str(df["o"].min()) + " "
             + str(df["o"].std()) + " "
             + str(df["o"].mean()) + "\n")
    fo.write("Agreableness max min std avg: " + str(df["c"].max()) + " "
             + str(df["c"].min()) + " "
             + str(df["c"].std()) + " "
             + str(df["c"].mean()) + "\n")
    fo.write("Extraversion max min std avg: " + str(df["e"].max()) + " "
             + str(df["e"].min()) + " "
             + str(df["e"].std()) + " "
             + str(df["e"].mean()) + "\n")
    fo.write("Agreableness max min std avg: " + str(df["a"].max()) + " "
             + str(df["a"].min()) + " "
             + str(df["a"].std()) + " "
             + str(df["a"].mean()) + "\n")
    fo.write("Neuroticism max min std avg: " + str(df["n"].max()) + " "
             + str(df["n"].min()) + " "
             + str(df["n"].std()) + " "
             + str(df["n"].mean()) + "\n")
    df['tweet_length'] = df['text'].str.len()
    fo.write("Tweet length max min avg: " + str(df['tweet_length'].max()) + " "
             + str(df['tweet_length'].min()) + " "
             + str(df['tweet_length'].mean()) + "\n")
    fo.write(str(df.isRetweet.value_counts()) + "\n")
    retw_perc = df.isRetweet.value_counts().loc[0.0]/df.shape[0]
    fo.write("Percentage of retweet items: " + str(retw_perc) + "\n")

    bins = 4096
    frequency = 300
    trait_name = ["Openness", "Conscentiousness",
                  "Extraversion", "Agreableness",
                  "Neuroticism"]
    pos = 0
    ocean = [df["o"], df["c"], df["e"], df["a"], df["n"]]
    for trait in ocean:
        plt.title("Distribution " + str(trait_name[pos]))
        plt.hist(trait, bins=bins, range=(1, 5))
        plt.ylabel("frequency")
        plt.xlabel("score")
        plt.axis([1, 5, 0, frequency])
        plt.grid()
        plt.draw()
        plt.savefig("./img/01/distribution_"+str(trait_name[pos])+'.png',
                    dpi=100)
        # plt.show()
        plt.close()
        pos = pos + 1
