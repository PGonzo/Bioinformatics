#!/usr/bin/env python
# coding: utf-8

# In[1]:


#load notebook with this:
#jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000000
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize #package for flattening json in pandas df
import flatten_json
import objectpath


# In[6]:


#load json
with open("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/Sleep_ReBLAST.json") as f:
    data = json.load(f)

#put json into pandas df
raw = json_normalize(data["BlastOutput2"], sep="_")
df = pd.DataFrame(raw)


# ### loop through df to extract node and taxids for each

# In[195]:


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


# In[198]:


df_final.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/SleepMice_jsonParsed.csv", header=True)


# ### cleaning Fasta

# In[279]:


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


# ### clean gtf file

# In[282]:


# download gtf to filter fasta
df_gtf = pd.read_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/Sleep_All_K75_blastedcontigs_cleaned_named_filtered_jgi.gtf", sep="\t", header=None)


# In[291]:


# filter and write out gtf
df_gtf_cleaned = df_gtf[df_gtf[0].isin(df_final_filter_unique["nodename"]) == False]
df_gtf_cleaned.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/SleepMice/contigs/SleepMice_musremoved.gtf", sep="\t", header=None, index=None)


# ### Trem2 data

# In[ ]:


#load json
with open("/Users/patrickgonzales/Desktop/Linklab/Microbiome/Trem2/trem2_ReBLAST.json") as t:
    data2 = json.load(t)
    
#put json into pandas df
raw2 = json_normalize(data2["BlastOutput2"], sep="_")
df2 = pd.DataFrame(raw2)

#looping through df
df_finals = pd.DataFrame(columns=["nodename", "hit_number", "taxid", "description"])

for x in range(len(df)):
    nodename = df2["report_results_search_query_title"].iloc[x]
    Hit = df2["report_results_search_hits"].iloc[x]
    print("Working on", x)

    for hit_dict in Hit:
        #print(hit_dict)
        hit_dict_descr = hit_dict["description"]
        hit_dict_num = hit_dict["num"]
        hit_dict_descr = hit_dict_descr[0]
        taxid = hit_dict_descr["taxid"]
        #print(type(hit_dict_descr))
        #print(hit_dict_descr)
        #print(taxid)
        #print(type(hit_dict_num))
        #print(hit_dict_num)
        diction = {"nodename":[nodename], "hit_number": [hit_dict_num], "taxid": [taxid], "description":[hit_dict_descr]}
        df_temp = pd.DataFrame.from_dict(diction)
        df_final = df_finals.append(df_temp)

print(df_finals.head())

df_finals.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/Trem2/trem2_jsonParsed.csv", header=True)


# In[ ]:


#get list of nodes with mus musculus taxid
df_final2_mus = df_finals.loc[df_finals['taxid'] == 10090]
df_final2_filter_unique = pd.DataFrame(df_final2_mus.nodename.unique(), columns=["nodename"])

# download tab fasta to filter fasta
df_fasta2 = pd.read_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/Trem2/All_K25_blastedcontigs_named_filteredTABAllFASTA.txt", sep="\t")

#rename column
df_fasta2.rename(columns={"node": "nodename"}, inplace=True)

#filter out nodes with mus musculus from tab fasta 
df_fasta2_cleaned = df_fasta2[df_fasta2["nodename"].isin(df_final2_filter_unique["nodename"]) == False]
df_fasta2_cleaned_r = df_fasta2_cleaned[["nodename", "fasta"]]
df_fasta2_cleaned_r.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/Trem2/trem2_musremoved_finalfasta.txt", sep="\t", header=None, index=None)


# In[ ]:


# download gtf to filter fasta
df_gtf2 = pd.read_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/Trem2/All_K25_blastedcontigs_named_filtered_jgi.gtf", sep="\t", header=None)

# filter and write out gtf
df_gtf2_cleaned = df_gtf2[df_gtf2[0].isin(df_final2_filter_unique["nodename"]) == False]
df_gtf2_cleaned.to_csv("/Users/patrickgonzales/Desktop/Linklab/Microbiome/Trem2/trem2_musremoved.gtf", sep="\t", header=None, index=None)

