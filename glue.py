import numpy as np
import mir
import midi
import time
import music21
from functools import partial


def myCallback(stream):
    if False:
        # stream.quantize()
        copy = stream.chordify()
        # copy.show('text')
        chordList = []
        sChords = copy
        sChordsFlat = sChords.flat
        for myChord in sChordsFlat:
            if "Chord" in myChord.classes:
                if 2 < len(myChord) < 6:  # and ( myChord.isTriad() ):
                    chordList.append(myChord.pitchedCommonName)
                    numpyArray = np.array(chordList)
                    idx, score = mir.mir.findRepeat(numpyArray)
                    if idx > -1:
                        print "Found loop at " + str(idx)
                        print "Loop score:   " + str(score)
    else:
        copy = stream
        noteList = []
        for myNote in copy:
            noteList.append(myNote)
            numpyArray = np.array(noteList)
            idx, score = mir.mir.findRepeat(numpyArray)
            if idx > -1:
                print "Found loop at " + str(idx)
                print "Loop score:   " + str(score)


stream = music21.stream.Stream()

with midi.reader.Reader(stream) as myReader:
    myReader.register(partial(myCallback, stream))
    while True:
        time.sleep(0.001)
