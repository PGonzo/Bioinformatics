#python 3.5
#this file will turn a fasta into a gtf. Using the length as start and end coordinates
#this is useful for STAR to give it chrm sizes when making a rRNA fasta to map and throw out reads.

def make_fasta_dict(f1):
    "This takes a fasta in and makes a dictionary"
    with open(f1, "r") as infile:
        n = 0 # Length of rows
        mlist = []
        nlist = str(n) + "list"
        nlist = []
        fastanamelist = []
        fastadict = {}
        for line in infile:
            if ">" in line:
                n = n + 1
                ID = line[1:-1]
                fastanamelist.append(ID)
                IDlist = ID + "list"
                IDlist = []
            if ">" not in line:
                string = line[:-1]
                IDlist.append(string)
                Finishedstring = "".join(IDlist)
                if len(Finishedstring) > 1:             #Make sure string is there
                    fastadict[ID] = Finishedstring
        m = len(Finishedstring)   # Length of columns
        return fastadict

f1 = "celegansRepbase_rep.fa"
d = make_fasta_dict(f1)

with open(f1[:-3] + "_chrmsize.genome", "w") as outfile:
    for k in d:
        start = 1
        end = len(d[k]) - 1
        outfile.write(k + "\t" + str(len(d[k])) + "\n")


