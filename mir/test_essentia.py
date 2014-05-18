from __future__ import division
#import music21
from music21 import *
import essentia.standard
import numpy as np


def stretch(data, bins, interpolation_type='linear'):
        ip1d = interpolate.interp1d(np.arange(data.shape[0]),
                                    data,
                                    kind=interpolation_type)
        return ip1d(np.linspace(0, data.shape[0] - 1, bins))


def onsets2BPM(stream21):
    onsets = []
    for i in stream.notes:
        onsets.append(i.offset)

    onsets = numpy.array(onsets)

    onsets = stretch(onsets, 44100)
    onsets = essentia.array(onsets)

    getTempo = essentia.standard.TempoTapDegara()

    return

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
        ##print loopScore
        thresh = 1;
        if loopScore >= thresh:
            loop = loopStartIdx;
        else:
            loop = -1

        return loop

def analyzeStream( seq ):
    ""
    pass

#s = converter.parse('./data/6.mid')

#s.plot('pianoroll')
s = converter.parse('./data/lessSimple2bars.mid')
#s = converter.parse('./data/verySimple2bars.mid')
chordList = [];
sChords = s.chordify()
sChordsFlat = sChords.flat
for myChord in sChordsFlat:
    if "Chord" in myChord.classes:
        if 2 < len( myChord ) < 6: #and ( myChord.isTriad() ):
            chordList.append(myChord.pitchedCommonName)
            numpyArray = np.array(chordList)
            print findRepeat( numpyArray )
#        print xChord.pitchClasses
#        print xChord.intervalVector


#cc.show('text')
#s.show('text')

#print harmony.chordSymbolFigureFromChord(chord.Chord(['C3','E3','G3'])) #standard example

#print findRepeat()
