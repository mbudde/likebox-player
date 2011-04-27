from PyQt4.QtCore import QObject, pyqtSignal
from mpd import MPDClient
from pprint import pprint
from .song import Song

class Client(QObject):

    # Signals
    connected = pyqtSignal()
    disconnected = pyqtSignal()


    def __init__(self, host, port, password=None):
        self._host = host
        self._port = port
        self._password = password

    def connect_client(self):
        self._client = MPDClient()
        self._client.connect(self._host, self._port)
        if self._password is not None:
            self._client.password(self._password)

    def get_songs(self):
        return [Song(i) for i in self._client.listallinfo() if 'title' in i]

    def get_playlists(self):
        return self._client.listplaylists()

    def create_playlist(self, name, songs):
        for song in songs:
            self._client.playlistadd(name, song.file)

if __name__ == '__main__':
    c = Client('localhost', 6600)
    c.connect_client()
    # songs = c.get_songs()
    # c.create_playlist("Playlist 1", songs[5:10])
    pprint(c.get_playlists())
