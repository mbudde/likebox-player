
from PyQt4 import QtCore, QtGui
from nmevent import Event

class Player(QtGui.QMainWindow):

    playing = Event()
    stopped = Event()
    paused = Event()
    quit = Event()

    def __init__(self):
        super(Player, self).__init__()

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')

        self._controls = PlayerControls()
        self._sourcelist = PlayerSourceList()
        self._songtable = PlayerSongTable()

        mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(mainWidget)

        vbox = QtGui.QVBoxLayout(mainWidget)
        vbox.addWidget(self._controls, 0)

        lowerWidget = QtGui.QWidget()
        hbox = QtGui.QHBoxLayout(lowerWidget)
        hbox.addWidget(self._sourcelist)
        hbox.addWidget(self._songtable)
        vbox.addWidget(lowerWidget, 1)


class PlayerControls(QtGui.QWidget):
    def __init__(self):
        super(PlayerControls, self).__init__()

        hbox = QtGui.QHBoxLayout(self)
        play = QtGui.QPushButton('Play')
        stop = QtGui.QPushButton('Stop')
        hbox.addWidget(play)
        hbox.addWidget(stop)
        hbox.addStretch(1)

        # self.connect(quit, QtCore.SIGNAL('clicked()'),
                     # QtGui.qApp, QtCore.SLOT('quit()'))

class PlayerSourceList(QtGui.QWidget):
    def __init__(self):
        super(PlayerSourceList, self).__init__()

class PlayerSongTable(QtGui.QWidget):
    def __init__(self):
        super(PlayerSongTable, self).__init__()
