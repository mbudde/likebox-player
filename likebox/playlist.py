from nmevent import Event
from functools import wraps

import logging
logger = logging.getLogger(__name__)


def memoized(f):
    """Memoization decorator. Saves the value for future calls"""
    @wraps(f)
    def wrapper(self):
        val = getattr(self, '_'+f.__name__, None)
        if val is None:
            val = f(self)
            setattr(self, '_'+f.__name__, val)
        return val
    return wrapper


class Playlist(object):
    """A list of songs with no order."""

    updated = Event()

    def __init__(self, client, name):
        self._client = client
        self._name = name
        self._songs = None

    @property
    def name(self):
        return self._name

    @property
    @memoized
    def songs(self):
        return self._client.listplaylistinfo(self.name)

    def update(self):
        self._songs = None
        self.updated()


class Library(Playlist):
    """A playlist with all songs in the library."""

    def __init__(self, client):
        super(Library, self).__init__(client, 'Music')
        self._playlists = None

    @property
    def playlists(self):
        if self._playlists is None:
            self._playlists = [Playlist(self._client, p['playlist'])
                               for p in self._client.listplaylists()]
        return self._playlists

    @property
    @memoized
    def songs(self):
        return [s for s in self._client.listallinfo()
                if 'title' in s]


class Queue(Playlist):
    """A play queue. Contains a list of songs in prioritized order."""

    def __init__(self, client):
        super(Queue, self).__init__(client, 'Play Queue')

    @property
    @memoized
    def songs(self):
        logger.debug('updating queue')
        return self._client.playlistinfo()

    def add(self, song):
        """Add a song to the end of the queue."""
        self._client.add(song['file'])

    def remove(self, song):
        """Remove song from the queue."""
        self._client.deleteid(song['file'])
