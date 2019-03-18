#function for reading fasta
def readFastaFile(filename):
    
    fileObj = open(filename, 'r')
    sequences = []
    seqFragments = []
    
    for line in fileObj:
        if line.startswith('>'):
            
            #found start of next sequence
            if seqFragments:
                sequence = ''.join(seqFragments)
                sequences.append(sequence)
            seqFragments = []
            
            else:
                #found more of exisiting sequence
                seq = line.rstrip # remove newline character
                seqFragments.append(seq)
                
        if seqFragments:
        sequence = "".join(seqFragments)
        sequences.append(sequence)
        
        fileObj.close()
        
        return sequences
