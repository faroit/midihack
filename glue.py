from __future__ import division
import mir
import live
import midi
import time
import music21
import numpy as np
from functools import partial

def rgb(r, g, b, a):
    return (r << 16) + (g << 8) + b

mode = 0
track = 0

def myCallback(stream, conn):
    global mode
    global track

    if len(stream) < 1:
        return

    if not conn.song.session_record:
        conn.song.trigger_session_record()

    if mode == 1:
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
                        conn.song.trigger_session_record()
                        conn.song.tracks[track].name = "Chords"
                        conn.song.tracks[track].color = rgb(100, 0, 255, 255)
                        conn.song.tracks[track].arm = False
                        track += 1
                        conn.song.tracks[track].arm = True
                        for i in range(len(stream.notes)):
                            stream.pop(0)
                        mode = 0
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
                conn.song.trigger_session_record()
                conn.song.tracks[track].name = "Roll"
                conn.song.tracks[track].color = rgb(237, 67, 37, 255)
                conn.song.tracks[track].arm = False
                track += 1
                conn.song.tracks[track].arm = True
                for i in range(len(stream.notes)):
                    stream.pop(0)
                mode = 1

    print mode, track

stream = music21.stream.Stream()

with midi.reader.Reader(stream) as myReader:
    conn = live.live.LiveConnection()
    conn.song.tracks[0].arm = True
    conn.song.tracks[1].arm = False
    conn.song.tracks[2].arm = False
    conn.song.tracks[3].arm = False
    myReader.register(partial(myCallback, stream, conn))
    while True:
        time.sleep(0.001)
