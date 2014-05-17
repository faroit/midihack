#from mir.analyzer import Analyzer
import numpy as np
import mir
import midi
import time
import music21

stream = music21.stream.Stream()

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
                    loopIdx = mir.mir.findRepeat( numpyArray );
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
                    loopIdx = mir.mir.findRepeat( numpyArray );
                    if loopIdx[0] > -1:
                        print "Found loop at " + str(loopIdx[0])
                        print "Loop score:   " + str(loopIdx[1])


with midi.reader.Reader(stream) as myReader:
    myReader.register( myCallback )
    while True:
        time.sleep(0.001)
