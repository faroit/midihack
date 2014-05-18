from __future__ import division
import mir
import live
import midi
import time
import music21
import numpy as np
from functools import partial


def myCallback(stream, conn):
    if len(stream) < 1:
        return

#    if not conn.song.session_record:
#        conn.song.trigger_session_record()
    if False:
        # stream.quantize()
        copy = stream.chordify()
        # copy.show('text')
        chordList = []
        sChords = copy
        sChordsFlat = sChords.flat
        lastChord = ""
        for myChord in sChordsFlat:
            if "Chord" in myChord.classes:
                if 2 <= len(myChord) < 6 and  lastChord != myChord.pitchedCommonName: 
                    lastChord = myChord.pitchedCommonName;
                    chordList.append(myChord.pitchedCommonName)
                    numpyArray = np.array(chordList)
                    correlation = mir.mir.corrSequence(numpyArray)
                    print correlation
                    idx, score = mir.mir.findRepeat(correlation)
                    if idx is not None:
                        print "Found loop at " + str(idx)
                        print "Loop score:   " + str(score)
                        time.sleep(60 / 480 * (sChordsFlat[idx].offset -
                                               sChordsFlat[idx-1].offset))
                       # conn.song.trigger_session_record()
                        for i in range(len(stream.notes)):
                            stream.pop(0)
    else:
        copy = stream
        noteList = []
        lastNote = ""
        for myNote in copy:
            if lastNote != myNote:
                noteList.append(myNote)
                lastNote = myNote
            else:
                continue
            numpyArray = np.array(noteList)
            correlation = mir.mir.corrSequence(numpyArray)
            print correlation
            idx, score = mir.mir.findRepeat(correlation)
            if idx is not None:
                print "Found loop at " + str(idx)
                print "Loop score:   " + str(score)

                # print 60 / 480 * (copy.notes[idx].offset - copy[idx-1].offset)
                time.sleep(60 / 480 * (copy.notes[idx].offset -
                                       copy[idx-1].offset))
                # conn.song.trigger_session_record()
                for i in range(len(stream.notes)):
                    stream.pop(0)


stream = music21.stream.Stream()

with midi.reader.Reader(stream) as myReader:
#    conn = live.live.LiveConnection()
    conn = None
    myReader.register(partial(myCallback, stream, conn))
    while True:
        time.sleep(0.001)
