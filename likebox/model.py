from mpd import MPDClient
from nmevent import Event

from .song import Song
from .playlist import Queue, Library

class PlayerModel(object):

    playing = Event()
    stopped = Event()
    paused = Event()

    current_song_changed = Event()

    songs_changed = Event()
    playlist_deleted = Event()

    def __init__(self, host, port, password=None):
        self._host = host
        self._port = port
        self._password = password
        self._client = MPDClient()
        self._queue = Queue(self._client)
        self._library = Library(self._client)
        self._state = 'stop'

    def connect(self):
        self._client.connect(self._host, self._port)
        if self._password is not None:
            self._client.password(self._password)

    @property
    def queue(self):
        return self._queue

    @property
    def library(self):
        return self._library

    def play(self, song=None):
        id = self._client.addid(song['file'])
        self._client.playid(id)
        self._state = 'play'
        self.playing(self)
        print self._client.status()

    def stop(self):
        self._client.stop()
        self._state = 'stop'

    def pause(self):
        status = self._client.status()
        if status['state'] == 'play':
            self._client.pause(1)
            self._state = 'pause'
            self.paused(self)

    def next(self):
        self._client.next()

    @property
    def current_song(self):
        return self._client.currentsong()
