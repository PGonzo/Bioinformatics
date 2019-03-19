#!/usr/bin/env python
# coding: utf-8

#load notebook with code below uncommented if size of file is too large for memory:
#jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000000

import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize #package for flattening json in pandas df
import flatten_json
import objectpath

#load json
with open("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/Sleep_ReBLAST.json") as f:
    data = json.load(f)

#put json into pandas df
raw = json_normalize(data["BlastOutput2"], sep="_")
df = pd.DataFrame(raw)


### loop through df to extract node and taxids for each ###

df_final = pd.DataFrame(columns=["nodename", "hit_number", "taxid", "description"])

for x in range(len(df)):
    nodename = df["report_results_search_query_title"].iloc[x]
    Hit = df["report_results_search_hits"].iloc[x]
    print("Working on", x)

    for hit_dict in Hit:
        hit_dict_descr = hit_dict["description"]
        hit_dict_num = hit_dict["num"]
        hit_dict_descr = hit_dict_descr[0]
        taxid = hit_dict_descr["taxid"]
        diction = {"nodename":[nodename], "hit_number": [hit_dict_num], "taxid": [taxid], "description":[hit_dict_descr]}
        df_temp = pd.DataFrame.from_dict(diction)
        df_final = df_final.append(df_temp)

print(df_final.head())

#get list of nodes with mus musculus taxid
df_final_mus = df_final.loc[df_final['taxid'] == 10090]
df_final_filter_unique = pd.DataFrame(df_final_mus.nodename.unique(), columns=["nodename"])

# download tab fasta to filter fasta
df_fasta = pd.read_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/Sleep_All_K75_blastedcontigs_cleaned_named_filteredTABAllFASTA.txt", sep="\t")

#rename column
df_fasta.rename(columns={"node": "nodename"}, inplace=True)

#filter out nodes with mus musculus from tab fasta 
df_fasta_cleaned = df_fasta[df_fasta["nodename"].isin(df_final_filter_unique["nodename"]) == False]
df_fasta_cleaned_r = df_fasta_cleaned[["nodename", "fasta"]]
df_fasta_cleaned_r.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/SleepMice_musremoved_finalfasta.txt", sep="\t", header=None, index=None)

#### clean gtf file ####

# download gtf to filter fasta
df_gtf = pd.read_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/Sleep_All_K75_blastedcontigs_cleaned_named_filtered_jgi.gtf", sep="\t", header=None)


# filter and write out gtf
df_gtf_cleaned = df_gtf[df_gtf[0].isin(df_final_filter_unique["nodename"]) == False]
df_gtf_cleaned.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/SleepMice_musremoved.gtf", sep="\t", header=None, index=None)

