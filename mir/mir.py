import music21
import numpy as np

def corrSequence( seq ):
    myCorr = np.zeros([len(seq),1]);
    for i in range(0,len(seq)):
        myCorr[i] = np.sum(seq == np.roll(seq, i))
    return myCorr/len(seq)


def findRepeat(seq):
    if len(seq) == 1:
        return None, -1
    else:
        loopStartIdx = seq[1:].argmax() + 1
        loopScore    = seq[loopStartIdx]

        thresh = 1
        if loopScore >= thresh:
            loop = loopStartIdx;
        else:
            loop = None

        return loop, loopScore