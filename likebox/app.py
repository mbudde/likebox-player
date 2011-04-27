
import sys
from PyQt4 import QtCore, QtGui

from .gui.player import Player
from .model import PlayerModel

class Main(object):

    def __init__(self):
        self._app = QtGui.QApplication(sys.argv)
        self._model = PlayerModel('localhost', 6600)
        self._model.connect()
        self._player = Player(self._model)

    def run(self):
        self._player.show()
        return self._app.exec_()
