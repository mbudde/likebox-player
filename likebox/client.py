from mpd import MPDClient
from nmevent import Event
from select import select
from threading import Thread

from .playlist import Queue, Library

import logging
logger = logging.getLogger(__name__)


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
        self._current_song = None
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
        self._client.consume(1)
        self._update_status()

    def play(self):
        if self._state == 'pause':
            self._client.pause(0)
        elif self._state == 'stop':
            self._client.play(0)

    def stop(self):
        self._client.stop()

    def pause(self):
        if self._state == 'play':
            self._client.pause(1)

    def playpause(self):
        if self._state == 'play':
            self.pause()
        else:
            self.play()

    def next(self):
        self._client.next()
        self.queue.update()

    def rescan(self):
        self._client.update()

    def _on_update(self, sender, changes):
        for change in changes:
            logger.debug('idle update: {0}'.format(change))
            if change == 'playlist':
                self.queue.update()
            elif change == 'player':
                self._update_status()

    def _update_status(self):
        status = self._client.status()
        if self._state != status['state']:
            self._state = status['state']
            self.state_changed(self._state)
        if self._current_song != status.get('songid', None):
            self._current_song = status['songid']
            self.current_song_changed(self.current_song)


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
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self._client.send_idle()
            select([self._client], [], [])
            changes = self._client.fetch_idle()
            self.updates(changes)
