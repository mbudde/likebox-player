from nmevent import Event

class Playlist(object):

    def __init__(self, client, name):
        self._client = client
        self._name = name
        self._songs = None

    @property
    def name(self):
        return self._name

    @property
    def songs(self):
        if self._songs is None:
            self._songs = self._client.listplaylistinfo(self.name)
        return self._songs


class Library(Playlist):

    def __init__(self, client):
        super(Library, self).__init__(client, 'Music')
        self._playlists = None

    @property
    def songs(self):
        if self._songs is None:
            self._songs = [s for s in self._client.listallinfo()
                           if 'title' in s]
        return self._songs

    @property
    def playlists(self):
        if self._playlists is None:
            self._playlists = [Playlist(self._client, p['playlist'])
                               for p in self._client.listplaylists()]
        return self._playlists


class Queue(Playlist):

    def __init__(self, client):
        super(Queue, self).__init__(client, 'Play Queue')

    @property
    def songs(self):
        if self._songs is None:
            self._songs = self._client.playlistinfo()
        return self._songs
