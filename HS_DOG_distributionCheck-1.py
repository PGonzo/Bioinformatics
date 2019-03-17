#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# read in combined DOG csv from DOG algorithm
df = pd.read_csv("/Users/patrickgonzales/desktop/Linklab/Heatshock/combined_DOG.csv", sep="\t")
df.info()

# make dataframe subsets based on adjusted p values and fold change
# to test if the distribution of the length of DOGs are significantly different.
df_sigdiff = df[df['padj'] <= 0.05]
df_sigdiff_upHS = df_sigdiff[df_sigdiff['log2FoldChange'] > 0]
df_sigdiff_control = df_sigdiff[df_sigdiff['log2FoldChange'] < 0]
df_NOT_sigdiff = df[df['padj'] > 0.05]

# take a look at descriptive stats
print("Sigdiff up in HS: DOG-length stats\n", df_sigdiff_upHS['DOG_length'].describe())
print("\nSigdiff up in Control: DOG-length stats\n", df_sigdiff_control['DOG_length'].describe())
print("\nNot significantly different: DOG-length stats:\n", df_NOT_sigdiff['DOG_length'].describe())

# plot histograms with mean(solid) and standard deviation (dashed) lines for three dataframes.
# is distribution normal?
plt.figure(figsize=(20, 5))

plt.subplot(1, 3, 1)
plt.hist(df_NOT_sigdiff['DOG_length'], bins=30, edgecolor='black',
         linewidth=0.5, color='teal', alpha=0.8)
plt.axvline(df_NOT_sigdiff['DOG_length'].mean(), color="black", linestyle='solid', linewidth=3)
plt.axvline(df_NOT_sigdiff['DOG_length'].mean(
) + df_NOT_sigdiff['DOG_length'].std(), color="black", linestyle="dashed", linewidth=3)
plt.axvline(df_NOT_sigdiff['DOG_length'].mean(
) - df_NOT_sigdiff['DOG_length'].std(), color="black", linestyle='dashed', linewidth=3)
plt.ylabel('# of DOGs')
plt.xlabel('length of DOG')
plt.title('Distribution of DOG length: P value greater than 0.05')

plt.subplot(1, 3, 2)
plt.hist(df_sigdiff_upHS['DOG_length'], bins=30,
         edgecolor='black', linewidth=0.5, color='teal', alpha=0.8)
plt.axvline(df_sigdiff_upHS['DOG_length'].mean(), color='black', linestyle='solid', linewidth=3)
plt.axvline(df_sigdiff_upHS['DOG_length'].mean(
) + df_sigdiff_upHS['DOG_length'].std(), color='black', linestyle='dashed', linewidth=3)
plt.axvline(df_sigdiff_upHS['DOG_length'].mean(
) - df_sigdiff_upHS['DOG_length'].std(), color='black', linestyle='dashed', linewidth=3)
plt.ylabel('# of DOGs')
plt.xlabel('length of DOG')
plt.title('Distribution of DOG length in DOGs significantly increased in HS')

plt.subplot(1, 3, 3)
plt.hist(df_sigdiff_control['DOG_length'], bins=30,
         edgecolor='black', linewidth=0.5, color='teal', alpha=0.8)
plt.axvline(df_sigdiff_control['DOG_length'].mean(), color='black', linestyle='solid', linewidth=3)
plt.axvline(df_sigdiff_control['DOG_length'].mean(
) + df_sigdiff_control['DOG_length'].std(), color='black', linestyle='dashed', linewidth=3)
plt.axvline(df_sigdiff_control['DOG_length'].mean(
) - df_sigdiff_control['DOG_length'].std(), color='black', linestyle='dashed', linewidth=3)
plt.ylabel('# of DOGs')
plt.xlabel('length of DOG')
plt.title('Distribution of DOG length in DOGs significantly increased in Controls')
plt.tight_layout()
plt.show()

# distribution is not normal- use non-parametric test.
# Use Wilcoxon-rank sum test to test if the two groups are drawn from same distribution
# similar to T-test but for non-parametric data.
print("Not sigdiff vs Up in Control:\n", stats.ranksums(
    df_NOT_sigdiff['DOG_length'], df_sigdiff_control['DOG_length']))
print("\nNot sigdiff vs Up in HS:\n", stats.ranksums(
    df_NOT_sigdiff['DOG_length'], df_sigdiff_upHS['DOG_length']))
print("\nUp in Control vs Up in HS:\n", stats.ranksums(
    df_sigdiff_control['DOG_length'], df_sigdiff_upHS['DOG_length']))

