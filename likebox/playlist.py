from nmevent import Event
from functools import wraps


def memoized(f):
    @wraps(f)
    def wrapper(self):
        val = getattr(self, '_'+f.__name__, None)
        if val is None:
            val = f(self)
            setattr(self, '_'+f.__name__, val)
        return val
    return wrapper


class Playlist(object):

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

    def __init__(self, client):
        super(Queue, self).__init__(client, 'Play Queue')

    @property
    @memoized
    def songs(self):
        print 'updating queue'
        return self._client.playlistinfo()

    def add(self, song):
        self._client.add(song['file'])
        self.update()

    def remove(self, song):
        self._client.deleteid(song['file'])
