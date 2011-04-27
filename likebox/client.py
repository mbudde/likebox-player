
from PyQt4.QtCore import QObject, pyqtSignal
from mpd import MPDClient


class Client(QObject):

    # Signals
    connected = pyqtSignal()
    disconnected = pyqtSignal()


    def __init__(self, host, port, password=None):
        pass

    def connect_client(self):
        self._client = MPDClient()
        self._client.connect(host, port)
        if password is not None:
            self._client.password(password)

    def get_songs(self):
        return self._client.listall()
