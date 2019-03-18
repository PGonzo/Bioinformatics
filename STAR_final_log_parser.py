import pandas as pd
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt
import re
import os
import scipy.stats as stats
PATH = "pathtofile"
os.chdir(PATH)
os.path.basename


def get_star_output(filelist):
    """This function will return a df from STAR aligner"""
    df = pd.DataFrame(columns=["sample", "input", "unique", "multi", "tooManyMulti"])
    x = 0
    for f1 in filelist:
        with open(f1, "r") as infile:
            input_reads_list = []
            unique_reads_list = []
            multi_reads_list = []
            tooManyMulti_list = []
            for line in infile:
                if "Number of input reads" in line:
                    scl = [m.start() for m in re.finditer(r"\t", line)]
                    input_reads = line[scl[0]:].strip("\t")
                    input_reads_list.append(int(input_reads))
                if "Uniquely mapped reads number" in line:
                    scl = [m.start() for m in re.finditer(r"\t", line)]
                    unique_reads = line[scl[0]:].strip("\t")
                    unique_reads_list.append(int(unique_reads))
                if "Number of reads mapped to multiple loci" in line:
                    scl = [m.start() for m in re.finditer(r"\t", line)]
                    multi_reads = line[scl[0]:].strip("\t")
                    multi_reads_list.append(int(multi_reads))
                if "Number of reads mapped to too many loci" in line:
                    scl = [m.start() for m in re.finditer(r"\t", line)]
                    tooManyMulti_reads = line[scl[0]:].strip("\t")
                    tooManyMulti_list.append(int(tooManyMulti_reads))

            df.loc[x] = pd.Series({"sample": (os.path.basename(f1)), "unique": unique_reads_list[0],
                                   "input": input_reads_list[0], "multi": multi_reads_list[0], "tooManyMulti": tooManyMulti_list[0]})
        x = x + 1

    return df
    # get_star_output(control_TOTAL_STAROUT_list[0])


# put pair, single, and rev into get_star_output function.
df_pair = get_star_output(glob("*PLog.final.out"))
df_pair["total_mapped"] = (df_pair["unique"] + df_pair["multi"]).astype(int)
df_pair["unmapped"] = df_pair["input"] - df_pair["total_mapped"]
df_pair.sort_values(by="sample", inplace=True)
# df_pair.to_csv("Trem2_Pair_totalmap_unmap.tsv",sep="\t",index=None)

df_single = get_star_output(glob("*FULog.final.out"))
df_single["total_mapped"] = (df_single["unique"] + df_single["multi"]).astype(int)
df_single["unmapped"] = df_single["input"] - df_single["total_mapped"]
df_single.sort_values(by="sample", inplace=True)
# df_single.to_csv("Trem2_fwdsingle_totalmap_unmap.tsv",sep="\t",index=None)

df_rev = get_star_output(glob("*RULog.final.out"))
df_rev["total_mapped"] = (df_rev["unique"] + df_rev["multi"]).astype(int)
df_rev["unmapped"] = df_rev["input"] - df_rev["total_mapped"]
df_rev.sort_values(by="sample", inplace=True)
# df_rev.to_csv("Trem2_revsingle_totalmap_unmap.tsv",sep="\t",index=None)

# make new df and sum all columns together
final_df = pd.DataFrame()

# get list of sample names here
final_df['sample'] = ["list_of_samplenames"]

final_df["total_reads"] = df_pair['input'] + df_single['input'] + df_rev['input']
final_df["uniqueMapped"] = df_pair['unique'] + df_single['unique'] + df_rev['unique']
final_df["MultiMapped"] = df_pair['multi'] + df_single['multi'] + df_rev['multi']
final_df["tooManyMultitoMap"] = df_pair['tooManyMulti'] + \
    df_single['tooManyMulti'] + df_rev['tooManyMulti']
final_df["total_mapped"] = df_pair['total_mapped'] + \
    df_single['total_mapped'] + df_rev['total_mapped']
final_df["unmapped"] = df_pair['unmapped'] + df_single['unmapped'] + df_rev['unmapped']

final_df.to_csv(PATH+"final_all_starOutputsSummed.tsv", sep="\t", index=None)
