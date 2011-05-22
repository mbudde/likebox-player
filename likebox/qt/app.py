
import sys
from PyQt4 import QtCore, QtGui

from .player import Player
from ..client import Client, IdleClient


class Main(object):
    """Main entry point for the Qt GUI application."""

    def __init__(self):
        self._app = QtGui.QApplication(sys.argv)
        credentials = ('localhost', 6600)
        self._client = Client(*credentials)
        self._client.connect()
        self._player = Player(self._client)

    def run(self):
        self._player.show()
        return self._app.exec_()
