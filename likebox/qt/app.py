
import sys
from PyQt4 import QtCore, QtGui

from .player import Player
from ..client import Client, IdleClient

class IdleThread(QtCore.QThread):

    change = QtCore.pyqtSignal(list)

    def __init__(self, *args):
        super(IdleThread, self).__init__()
        self._client = IdleClient(*args)

    def connect_and_run(self):
        self._client.connect()
        self.start()

    def run(self):
        while True:
            change = self._client.wait_for_change()
            self.change.emit(change)


class Main(object):

    def __init__(self):
        self._app = QtGui.QApplication(sys.argv)
        credentials = ('localhost', 6600)
        self._client = Client(*credentials)
        self._client.connect()
        self._idle = IdleThread(*credentials)
        self._idle.connect_and_run()
        self._player = Player(self._client, self._idle)

    def run(self):
        self._player.show()
        return self._app.exec_()
