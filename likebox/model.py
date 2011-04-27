from mpd import MPDClient
from nmevent import Event

from .song import Song

class PlayerModel(object):

    def __init__(self, host, port, password=None):
        self._host = host
        self._port = port
        self._password = password

    def connect(self):
        self._client = MPDClient()
        self._client.connect(self._host, self._port)
        if self._password is not None:
            self._client.password(self._password)

    @property
    def songs(self):
        return [Song(i) for i in self._client.listallinfo() if 'title' in i]

    @property
    def playlists(self):
        return self._client.listplaylists()

    def create_playlist(self, name, songs):
        for song in songs:
            self._client.playlistadd(name, song.file)
        self._client.save(name)
