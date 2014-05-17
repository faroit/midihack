from __future__ import division
#import music21
from music21 import *
import numpy as np

#import rtmidi
def corrSequence( seq ):
    myCorr = np.zeros([len(seq),1]);
    for i in range(0,len(seq)):
        myCorr[i] = np.sum(seq == np.roll(seq, i))
    return myCorr/len(seq)

def findRepeat( seq ):
    
    if len( seq ) == 1:
        return -1
    else:
        # compute "string correlation"
        corrSeqBool  = corrSequence( seq );

        # return index of loop start
        loopStartIdx = corrSeqBool[1:].argmax() + 1;

        # interpret "correlation"  as score value
        loopScore    = corrSeqBool[loopStartIdx];
        print loopScore    
        thresh = 0;
        if loopScore >= thresh:
            loop = loopStartIdx;
        else:
            loop = -1

        return loop
 
#s = converter.parse('./data/6.mid')

#s.plot('pianoroll')
s = converter.parse('./data/verySimple2bars.mid')
chordList = [];
sChords = s.chordify()
sChordsFlat = sChords.flat
for myChord in sChordsFlat:
    if "Chord" in myChord.classes:
        chordList.append(myChord.pitchedCommonName)
        numpyArray = np.array(chordList)
        print findRepeat( numpyArray )
#        print xChord.pitchClasses
#        print xChord.intervalVector


#cc.show('text')
#s.show('text')

#print harmony.chordSymbolFigureFromChord(chord.Chord(['C3','E3','G3'])) #standard example

#print findRepeat()
