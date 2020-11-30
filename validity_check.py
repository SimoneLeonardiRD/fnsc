import pandas as pd
from numpy import cov
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import seaborn as sn
import matplotlib.pyplot as plt

import numpy as np
from numpy import array
from numpy import mean
from numpy import cov
from numpy.linalg import eig
from scipy import stats

import scipy
import ceolib as cl

# df = pd.read_csv("data/PT/fake_pt.csv", header=None)
df = pd.read_csv("data/PT/real_pt.csv", header=None)
df.columns = ['o', 'c', 'e', 'a', 'n']
# cl.plot_dist(df, "images/fake_PT/", "fake")
cl.plot_dist(df, "images/real_PT/", "real")

for trait in ['o', 'c', 'e', 'a', 'n']:
    print( trait + " mean std " + str(df[trait].mean()) + " " + str(df[trait].std()))
    print( trait + " max min " + str(df[trait].max()) + " " + str(df[trait].min()))


'''
kl = cl.kl_divergence(df3_filt['OPN_pred'], df3_filt['o'])
print("Openness KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['CON_pred'], df3_filt['c'])
print("Conscentiousness KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['EXT_pred'], df3_filt['e'])
print("Extraversion KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['AGR_pred'], df3_filt['a'])
print("Agreableness KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['NEU_pred'], df3_filt['n'])
print("Neuroticism KL divergenge: ", kl)
print("-----------------------------------------")
kl = cl.kl_divergence(df3_filt['o'], df3_filt['OPN_pred'])
print("Openness KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['c'], df3_filt['CON_pred'],)
print("Conscentiousness KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['e'], df3_filt['EXT_pred'])
print("Extraversion KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['a'], df3_filt['AGR_pred'])
print("Agreableness KL divergenge: ", kl)
kl = cl.kl_divergence(df3_filt['n'], df3_filt['NEU_pred'])
print("Neuroticism KL divergenge: ", kl)
'''

