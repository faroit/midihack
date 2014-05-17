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
        self.stream.append(msg)


class Reader():
    def __enter__(self):
        dev = rtmidi.RtMidiIn()
        self.collectors = []
        self.stream = []
        for i in range(dev.getPortCount()):
            device = rtmidi.RtMidiIn()
            print 'OPENING', dev.getPortName(i)
            collector = ReaderThread(device, i, self.stream)
            collector.start()
            self.collectors.append(collector)

    def __exit__(self):
        for c in self.collectors:
            c.quit = True

    def getStream(self):
        return self.stream


if __name__ == "__main__":
    with Reader():
        while True:
            pass