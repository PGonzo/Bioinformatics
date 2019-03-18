import pandas as pd
import csv
names = ["rep","family","model","length"]             #MSAT1_CE	SAT	Caenorhabditis elegans	226
df = pd.read_csv("celegansRepbase_rep_chrmsize.genome", sep="\t", names=names)




df["Strand"] = "+"



df["source"] = "Ensembl"
df["type"] = "exon"
df["dot"] = "."
df["dot2"] = "."
df["start"] = 1
df["length"] = df["length"]+1
df["chr"] = df["rep"]

df["gene_id"] = "gene_id \""+df["rep"]+"\";"+"transcript_id \""+df["rep"]+"\""
df = df[["chr", "source", "type", "start", "length", "dot", "Strand", "dot2", "gene_id"]]
#II	WormBase	gene	2280078	2280678	.	-	.	gene_id "WBGene00019592"; gene_source "WormBase"; gene_biotype "protein_coding";

df.to_csv("celegansRepbase_rep_chrmsize.gtf",sep="\t",header=None, quoting=csv.QUOTE_NONE, index=None)
