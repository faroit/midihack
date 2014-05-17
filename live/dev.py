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

if __name__ == "__main__":
    conn = rpyc.connect('127.0.0.1', 17744)
    live = conn.root.Live.Application.get_application()
    song = live.get_document()

    try:
        if not song.tracks[0].clip_slots[0].clip.is_midi_clip:
            raise ValueError("Selected Clip must be MIDI")
    except AttributeError:
        raise ValueError("Selected Clip must not be empty")

    def callback(live):
        clip = live.get_document().tracks[0].clip_slots[0].clip
        print clip.get_notes(0.0, 0, 135.0, 127)

    with RegisterListener(song.tracks[0].clip_slots[0].clip,
                          'notes', callback, live):
        while 1:
            time.sleep(0.001)
            conn.poll_all(0)
