import os
import csv
import glob
import string
import sys

#template name
#templatename = sys.argv[1]
templatename = "star_templatePairedEnd.sh"
with open(templatename) as f:
    templatecontents = f.read()
    #this block is load template file

forward_Pairlist = sorted(glob.glob('*_1_FPUnmapped.out.mate1'))
reverse_Pairlist = sorted(glob.glob('*_1_FPUnmapped.out.mate2'))
forward_unpairlist = sorted(glob.glob('*_1_FUUnmapped.out.mate1'))
reverse_unpairlist = sorted(glob.glob('*_2_RUUnmapped.out.mate1'))
# print(forwardlist)
# print(reverselist)
for x in range(0,len(forward_Pairlist)):
        stringFP = str(forward_Pairlist[x])
        stringFP = stringFP[:-23]
        stringRP = str(reverse_Pairlist[x])
        stringRP = stringRP[:-23]
        stringFU = str(forward_unpairlist[x])
        stringFU = stringFU[:-23]
        stringRU = str(reverse_unpairlist[x])
        stringRU = stringRU[:-23]
        # print(stringF)
        # print(stringR)
        outputcontents = templatecontents.replace('replacedwordone', stringFP)
        outputcontents = outputcontents.replace('replacedwordtwo', stringRP)
        outputcontents = outputcontents.replace('replacedwordthree', stringFU)
        outputcontents = outputcontents.replace('replacedwordfour', stringRU)
        with open(stringFP  + '_star.sh', 'w') as g:
            g.write(outputcontents)
