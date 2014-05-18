from __future__ import division
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
        self.callbacks = []

    def run(self):
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        self.start = time.time() * 1000
        self.i = 0
        while True:
            if self.quit:
                return
            msg = self.device.getMessage()
            if msg:
                self.append(msg)
            else:
                time.sleep(0.001)
            self.i += 1
            if self.i == 10:
                self.dispatch()

    def register(self, callback):
        self.callbacks.append(callback)

    def dispatch(self):
        for i in self.callbacks:
            i()

    def append(self, msg):
        if msg.isNoteOn():
            n = music21.note.Note()
            n.midi = msg.getNoteNumber()
            n.duration = music21.duration.Duration('16th')
            timestamp = self.ms_to_samples()
            self.stream.insert(timestamp, n)
            self.i = 0

    def ms_to_samples(self):
        diff = (time.time() * 1000) - self.start
        return diff * 480 / (60 * 1000)


class Reader(object):
    def __init__(self, stream=None):
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
        return self

    def __exit__(self, type, value, tb):
        for c in self.collectors:
            c.quit = True

    def register(self, callback):
        for i in self.collectors:
            i.register(callback)

    def getStream(self):
        return self.stream


if __name__ == "__main__":
    stream = music21.stream.Stream()
    with Reader(stream):
        while True:
            pass
