import music21
import numpy as np

def corrSequence( seq ):
    myCorr = np.zeros([len(seq),1]);
    for i in range(0,len(seq)):
        myCorr[i] = np.sum(seq == np.roll(seq, i))
    return myCorr/len(seq)

def findRepeat( seq ):
    
    if len( seq ) == 1:
        return [-1, -1]
    else:
        # compute "string correlation"
        corrSeqBool  = corrSequence( seq );

        # return index of loop start
        loopStartIdx = corrSeqBool[1:].argmax() + 1;

        # interpret "correlation"  as score value
        loopScore    = corrSeqBool[loopStartIdx];
        #print loopScore    
        thresh = 1;
        if loopScore >= thresh:
            loop = loopStartIdx;
        else:
            loop = -1

        return [loop, loopScore]