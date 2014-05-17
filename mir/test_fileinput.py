from __future__ import division
#import music21
from music21 import *

#import rtmidi


def findRepeat():
    if (0):
        loop = 1
    else:
        loop = 0
    return loop

s = converter.parse('./data/6.mid')
#s.plot('pianoroll')
#converter.parseData('./data/verySimple2bars.mid')
cc = s.chordify()
y = cc.flat
for x in y:
	if "Chord" in x.classes:
		print x.pitchedCommonName 

#cc.show('text')
#s.show('text')

#print harmony.chordSymbolFigureFromChord(chord.Chord(['C3','E3','G3'])) #standard example

#print findRepeat()
