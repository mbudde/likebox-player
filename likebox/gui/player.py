
from PyQt4 import QtCore, QtGui
from nmevent import Event

class Player(QtGui.QMainWindow):

    playing = Event()
    stopped = Event()
    paused = Event()
    quit = Event()

    def __init__(self):
        super(Player, self).__init__()

        self._controls = PlayerControls()
        self._sourcelist = PlayerSourceList()
        self._songtable = PlayerSongTable()
        self._menubar = PlayerMenuBar()

        mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(mainWidget)

        vbox = QtGui.QVBoxLayout(mainWidget)
        vbox.addWidget(self._controls, 0)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self._sourcelist)
        splitter.addWidget(self._songtable)
        vbox.addWidget(splitter, 1)

        self.setMenuBar(self._menubar)

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

class PlayerSourceList(QtGui.QListWidget):
    def __init__(self):
        super(PlayerSourceList, self).__init__()
        QtGui.QListWidgetItem("Oak", self)


class PlayerSongTable(QtGui.QWidget):
    def __init__(self):
        super(PlayerSongTable, self).__init__()

class PlayerMenuBar(QtGui.QMenuBar):
    def __init__(self):
        super(PlayerMenuBar, self).__init__()
        
        menuFile = self.addMenu('File')

        Quit = QtGui.QAction("Quit", menuFile)
        menuFile.addAction(Quit)
        Quit.triggered.connect(self._on_quit)
        

        menuOptions = self.addMenu('Options')

        RemoveSong = QtGui.QAction("Remove Song", menuOptions)       
        menuOptions.addAction(RemoveSong)
        RemoveSong.triggered.connect(self._on_remove_song)
    
    def _on_quit(self, *args):    
        QtGui.qApp.quit()

    def _on_remove_song(self, *args):
        pass
        
        

