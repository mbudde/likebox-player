from mpd import MPDClient
from nmevent import Event

from .song import Song

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

        self._state = 'stop'

    def connect(self):
        self._client = MPDClient()
        self._client.connect(self._host, self._port)
        if self._password is not None:
            self._client.password(self._password)

    @property
    def songs(self):
        return [i for i in self._client.listallinfo() if 'title' in i]

    @property
    def playlists(self):
        return self._client.listplaylists()

    def create_playlist(self, name, songs):
        for song in songs:
            self._client.playlistadd(name, song.file)
        self._client.save(name)

    def play(self, song=None):
        print 'asdf'
        self._client.play()
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

    @property
    def current_song(self):
        return self._client.currentsong
