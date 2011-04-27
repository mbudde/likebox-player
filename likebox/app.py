
import sys
from PyQt4 import QtCore, QtGui

from .gui.player import Player

class Main(object):

    def __init__(self):
        self._app = QtGui.QApplication(sys.argv)
        self._player = Player()

    def run(self):
        self._player.show()
        return self._app.exec_()
