#function to convert sequence to its reverse complement.
def reverseComplement(sequence, isDNA=True):
    from string import maketrans
    
    if isDNA:
        sequence = sequence.replace('U', 'T')
        #maketrans function does in to out translation from character to character
        transTable = maketrans('ATCG', 'TACG')
    else: 
        sequence = sequence.replace('T', 'U')
        transTable = maketrans('AUGC', 'UAGC')
        
    complement = sequence.translate(transTable)
    reverseComp = complement[::-1]
    
    return reverseComp
