from mpd import MPDClient
from nmevent import Event
from select import select
from threading import Thread

from .playlist import Queue, Library

class BaseClient(object):

    def __init__(self, host, port, password=None):
        self._host = host
        self._port = port
        self._password = password
        self._client = MPDClient()

    def connect(self):
        self._client.connect(self._host, self._port)
        if self._password is not None:
            self._client.password(self._password)

    def disconnect(self):
        self._client.disconnect()

class Client(BaseClient):
    """MPD client. Acts as a middleman between MPD and the GUI."""

    state_changed = Event()
    current_song_changed = Event()

    def __init__(self, *args):
        super(Client, self).__init__(*args)
        self._queue = Queue(self._client)
        self._library = Library(self._client)
        self._state = 'stop'
        self._idle = IdleClient(*args)
        self._idle.updates += self._on_update

    @property
    def queue(self):
        return self._queue

    @property
    def library(self):
        return self._library

    @property
    def current_song(self):
        return self._client.currentsong()

    @property
    def state(self):
        return self._state

    def connect(self):
        super(Client, self).connect()
        self._idle.connect()
        self._state = self._client.status()['state']
        self._client.consume(1)

    def play(self):
        if self._state == 'pause':
            self._client.pause(0)
        elif self._state == 'stop':
            self._client.play(0)
        self._set_state('play')

    def stop(self):
        self._client.stop()
        self._set_state('stop')

    def pause(self):
        if self._state == 'play':
            self._client.pause(1)
            self._set_state('pause')

    def playpause(self):
        if self._state == 'play':
            self.pause()
        else:
            self.play()

    def next(self):
        self._client.next()
        self.queue.update()

    def _set_state(self, state):
        if self._state == state:
            return
        self._state = state
        self.state_changed(state)

    def _on_update(self, sender, changes):
        for change in changes:
            if change == 'playlist':
                self.queue.update()


class IdleClient(BaseClient, Thread):
    """MPD idle client. Receives notification of events in MPD.

    Runs in a seperate thread.
    """

    updates = Event()

    def __init__(self, *args):
        BaseClient.__init__(self, *args)
        Thread.__init__(self)

    def connect(self):
        super(IdleClient, self).connect()
        self._client.send_idle()
        self.daemon = True
        self.start()

    def run(self):
        while True:
            select([self._client], [], [])
            changes = self._client.fetch_idle()
            self.updates(changes)
