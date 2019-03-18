#write multiple sequence into multiple fasta records
def writeFastaSeqs(comments, sequences, fastaFile, width=60):
    fileObj = open(fastaFile, 'w')
    
    for i, seq in enumerate(sequences):
    
        numLines = 1 + (len(seq)-1)//width
        seqLines = [seq[width*x:width*(x+1)] for x in range(numLines)]

        seq = '\n'.join(seqLines)
        fileObj.write('> %s\n%s\n' % (comments[i], seq))
    
    fileObj.close()
