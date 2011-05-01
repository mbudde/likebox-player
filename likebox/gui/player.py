
from PyQt4 import QtCore, QtGui
from nmevent import Event

from .model import SongListModel

class Player(QtGui.QMainWindow):

    play = Event()
    stop = Event()
    pause = Event()

    def __init__(self, model):
        super(Player, self).__init__()

        self._model = model

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Likebox')

        self._controls = PlayerControls(model)
        self._sourcelist = PlayerSourceList()
        self._songview = PlayerSongView()
        self._menubar = PlayerMenuBar()
        self._playlistpicker = PlayerListPicker()

        mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(mainWidget)

        vbox = QtGui.QVBoxLayout(mainWidget)
        vbox.addWidget(self._controls, 0)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self._sourcelist)
        splitter.addWidget(self._songview)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        vbox.addWidget(splitter, 1)

        self.setMenuBar(self._menubar)
        vbox.addWidget(self._playlistpicker)

        self._controls.play.connect(self._on_play)

        self._loadData()

    def _loadData(self):
        for playlist in self._model.playlists:
            print playlist
            self._sourcelist.addPlaylist(playlist['playlist'])
        self._songview.setSongs(self._model.songs)
            # self._playlistpicker.add_playlist(playlist['playlist'])

    def _on_play(self, *args):
        print 'hasf'
        print self._model
        self._model.play()


class PlayerControls(QtGui.QWidget):

    play = QtCore.pyqtSignal()
    stop = QtCore.pyqtSignal()

    def __init__(self, model):
        super(PlayerControls, self).__init__()

        self._model = model

        hbox = QtGui.QHBoxLayout(self)
        play = QtGui.QPushButton('Play')
        stop = QtGui.QPushButton('Stop')
        hbox.addWidget(play)
        hbox.addWidget(stop)
        hbox.addStretch(1)

        # play.clicked.connect(self._on_play)
        play.clicked.connect(self.play)
        # stop.clicked.connect(model.stop)


class PlayerSourceList(QtGui.QListWidget):
    def __init__(self):
        super(PlayerSourceList, self).__init__()

    def addPlaylist(self, name):
        QtGui.QListWidgetItem(name, self)


class PlayerSongView(QtGui.QTreeView):
    def __init__(self):
        super(PlayerSongView, self).__init__()
        self._song_model = SongListModel()
        self.setModel(self._song_model)

    def setSongs(self, songs):
        self._song_model.setSongs(songs)


class PlayerMenuBar(QtGui.QMenuBar):
    def __init__(self):
        super(PlayerMenuBar, self).__init__()

        menu_file = self.addMenu('File')
        quit = QtGui.QAction("Quit", menu_file)
        quit.triggered.connect(self._on_quit)
        quit.setShortcut(QtGui.QKeySequence("Ctrl+q"))
        menu_file.addAction(quit)

        menu_options = self.addMenu('Options')
        remove_song = QtGui.QAction("Remove Song", menu_options)
        remove_song.triggered.connect(self._on_remove_song)
        menu_options.addAction(remove_song)

    def _on_quit(self, *args):
        QtGui.qApp.quit()

    def _on_remove_song(self, *args):
        pass


class PlayerListPicker(QtGui.QComboBox):
    def __init__(self):
        super(PlayerListPicker, self).__init__()
        self.addItem("Party in the Montana")
        self.addItem("Some unknow band")

