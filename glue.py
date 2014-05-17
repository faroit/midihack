#from mir.analyzer import Analyzer
import midi
import time
import music21
import numpy as np

stream = music21.stream.Stream()

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

def myCallback():
    if False:
        #stream.quantize()
        copy = stream.chordify() 
#       copy.show('text')
        chordList = []; 
        sChords = copy
        sChordsFlat = sChords.flat
        for myChord in sChordsFlat:
            if "Chord" in myChord.classes:
                if 2 < len( myChord ) < 6: #and ( myChord.isTriad() ):
                    chordList.append(myChord.pitchedCommonName)
                    numpyArray = np.array(chordList)
                    loopIdx = findRepeat( numpyArray );
                    if loopIdx[0] > -1:
                        print "Found loop at " + str(loopIdx[0])
                        print "Loop score:   " + str(loopIdx[1])
    else:
        copy = stream #.chordify() 
#       copy.show('text')
        noteList = []; 
        #sChords = copy
        #sChordsFlat = sChords.flat
        for myNote in copy:
            #if "Chord" in myChord.classes:
            #    if 2 < len( myChord ) < 6: #and ( myChord.isTriad() ):
                    noteList.append( myNote )
                    numpyArray = np.array( noteList )
                    loopIdx = findRepeat( numpyArray );
                    if loopIdx[0] > -1:
                        print "Found loop at " + str(loopIdx[0])
                        print "Loop score:   " + str(loopIdx[1])

with midi.reader.Reader(stream) as myReader:
    myReader.register( myCallback )
    while True:
        time.sleep(0.001)
