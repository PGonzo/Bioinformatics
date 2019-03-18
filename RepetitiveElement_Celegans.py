#!/usr/bin/env python
# coding: utf-8

#Purpose: Take list of specific Repetitive elements, get information nucleotide length, number of occurences in genome, and expression levels across genome.

import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#import data
df_repeat = pd.read_csv("/Volumes/MePortDrive/LinkLab/Ahringer_ATAC/ws220_repeats.txt",
                       sep="\t", names=["chrom", "start", "end", "repeat","RE"])

df_tom = pd.read_csv("/Volumes/MePortDrive/LinkLab/Ahringer_ATAC/tom_repeats.txt",
                       sep="\t")

#merge repeats of interest with whole repeats file
df_tomsRepeats = df_repeat.merge(df_tom, on="repeat")

#convert start and end into integers
df_tomsRepeats['start'] = df_tomsRepeats.start.astype("int", inplace = True)
df_tomsRepeats['end'] = df_tomsRepeats.end.astype("int", inplace = True)

#make length column
df_tomsRepeats['length'] = df_tomsRepeats['end'] - df_tomsRepeats['start']

#make dataframe for number of occurences of repeats
df_occur = pd.DataFrame(df_tomsRepeats.repeat.value_counts()).reset_index()

#rename columns
df_occur.columns = ['repeat', 'occurence']

#plot repeat occurences
sns_plot = plt.figure(figsize=[15,10])
sns.barplot(x='repeat', y='occurence', data=df_occur)
plt.xticks(rotation=45)
plt.title("Repetitive Element Occurrences in Genome", fontweight="bold", fontsize='20')
plt.xlabel("Repeat Candidates", fontweight="bold", fontsize=12)
plt.ylabel("# of Occurrences", fontweight="bold", fontsize=12)
#sns_plot.savefig("/Users/patrickgonzales/Desktop/TomRepeats_REoccurences.png")
plt.show()

#import specific repeats
df_tomsRepeats.to_csv("/Users/patrickgonzales/Desktop/TomRepeats.csv")

#plot length 
sns_plot = plt.figure(figsize=[20,10])
sns.swarmplot(x='repeat', y='length', data=df_tomsRepeats)
plt.xticks(rotation=45)
plt.title("Repetitive Element Lengths", fontweight="bold", fontsize='20')
plt.xlabel("Repeat Candidates", fontweight="bold", fontsize=12)
plt.ylabel("Repeat Lengths", fontweight="bold", fontsize=12)
plt.ylim([0,4000])
#sns_plot.savefig("/Users/patrickgonzales/Desktop/TomRepeats_swarmplot.png")
plt.show()

#plot length 
sns_plot = plt.figure(figsize=[20,10])
sns.boxplot(x='repeat', y='length', data=df_tomsRepeats)
plt.xticks(rotation=45)
plt.title("Repetitive Element Lengths", fontweight="bold", fontsize='20')
plt.xlabel("Repeat Candidates", fontweight="bold", fontsize=12)
plt.ylabel("Repeat Lengths", fontweight="bold", fontsize=12)
plt.ylim([0,4000])
#sns_plot.savefig("/Users/patrickgonzales/Desktop/TomRepeats_boxplot.png")
plt.show()


# #bedtools command to merge to bedfiles together based on coordinates
# bedtools merge -d 15 -c 4,5,6,7,8,9,10,11,12 -o mean,distinct,first,last,distinct,distinct,distinct,sum,distinct -i fileforMerging.bed > Merged_ATAC_repeat.bed

#import data
df_cluster = pd.read_csv("/Volumes/MePortDrive/LinkLab/Ahringer_ATAC/ATAC_cluster_overlapRE.txt",sep="\t")
df_cluster.head()

#determine ATAC peak size distribution by repeat
repeatList = list(df_cluster.RE_repeat.unique())
repeatList

#setup plot
sns_plot3 = plt.figure(figsize=[25,30])

#loopit
for rep,num in zip(repeatList, range(1,27)):
    x = df_cluster[df_cluster["RE_repeat"]== rep]
    plt.subplot(5,6,num)
    sns.distplot(x['ATAC_peakSize'],kde=False, rug=True)
    plt.ylabel("# of Occurrences")
    plt.title("Distribution of ATAC Peak sizes:\n" + rep, fontweight="bold")
    plt.tight_layout()
plt.show()

#sns_plot3.savefig("/Users/patrickgonzales/Desktop/TomRepeats_ATACpeakSizeDistributionoverREs.png")

#setup plot
sns_plot3 = plt.figure(figsize=[25,30])

#loopit
for rep,num in zip(repeatList, range(1,27)):
    x = df_cluster[df_cluster["RE_repeat"]== rep]
    plt.subplot(5,6,num)
    sns.distplot(x['pct_RE_covered'],kde=False, rug=True, color="green")
    plt.ylabel("# of Occurrences")
    plt.title("Distribution of pct_coverage over REs:\n" + rep, fontweight="bold")
    plt.tight_layout()
plt.show()

#sns_plot3.savefig("/Users/patrickgonzales/Desktop/TomRepeats_ATAC_coverage_overREs.png")

#slice repeat list by factor of 9 for visualization purposes
re_list1 = repeatList[0:10]
re_list2 = repeatList[10:19]
re_list3 = repeatList[19:27]

#setup plot
sns_plot4 = plt.figure(figsize=[20,20], dpi=100)

#loopit
for rep,num in zip(re_list1, range(1,10)):
    x = df_cluster[df_cluster["RE_repeat"]== rep]
    plt.subplot(3,3,num)
    sns.distplot(x['pct_RE_covered'],kde=False, rug=True, color="green")
    plt.ylabel("# of Occurrences")
    plt.title("Distribution of pct_coverage over REs:\n" + rep, fontweight="bold", fontsize=14)
    plt.tight_layout()
plt.show()

#setup plot
sns_plot5 = plt.figure(figsize=[20,20], dpi=100)

#loopit
for rep,num in zip(re_list2, range(1,10)):
    x = df_cluster[df_cluster["RE_repeat"]== rep]
    plt.subplot(3,3,num)
    sns.distplot(x['pct_RE_covered'],kde=False, rug=True, color="green")
    plt.ylabel("# of Occurrences")
    plt.title("Distribution of pct_coverage over REs:\n" + rep, fontweight="bold", fontsize=14)
    plt.tight_layout()
plt.show()

#sns_plot5.savefig("/Users/patrickgonzales/Desktop/TomRepeats_ATAC_coverage_overREslist2.png")


