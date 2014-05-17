import sys
import time
import rtmidi
import music21
import threading

class ReaderThread(threading.Thread):
    def __init__(self, device, port, stream):
        threading.Thread.__init__(self)
        self.stream = stream
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False

    def run(self):
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            if self.quit:
                return
            msg = self.device.getMessage()
            if msg:
                self.append(msg)
            else:
                time.sleep(0.1)

    def append(self, msg):
        if msg.isNoteOn():
            n = music21.note.Note()
            n.midi = msg.getNoteNumber()
            n.duration = music21.duration.Duration('half')
            self.stream.append(n)


class Reader():
    def __init__(self, stream):
        if stream is not None:
            self.stream = stream
        else:
            stream = music21.stream.Stream()

    def __enter__(self):
        dev = rtmidi.RtMidiIn()
        self.collectors = []
        for i in range(dev.getPortCount()):
            device = rtmidi.RtMidiIn()
            print 'OPENING', dev.getPortName(i)
            collector = ReaderThread(device, i, self.stream)
            collector.start()
            self.collectors.append(collector)

    def __exit__(self, type, value, tb):
        for c in self.collectors:
            c.quit = True

    def getStream(self):
        return self.stream


if __name__ == "__main__":
    stream = music21.stream.Stream()
    with Reader(stream):
        while True:
            pass