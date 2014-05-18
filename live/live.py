import time
import rpyc
from functools import partial


class RegisterListener():
    def __init__(self, object, attribute, callback, *args):
        self.callback = partial(callback, *args)
        self.object = object
        self.attribute = attribute

    def __enter__(self):
        getattr(self.object,
                'add_' + self.attribute + '_listener')(self.callback)

    def __exit__(self, type, value, tb):
        getattr(self.object,
                'remove_' + self.attribute + '_listener')(self.callback)


class LiveConnection(object):
    def __init__(self, host='127.0.0.1', port=17744):
        try:
            self.conn = rpyc.connect(host, port)
            self.live = self.conn.root.Live.Application.get_application()
            self.song = self.live.get_document()
        except IOError:
            print "Could not connect to Ableton, is it running?"
