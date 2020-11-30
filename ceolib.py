import matplotlib.pyplot as plt
import numpy as np


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
