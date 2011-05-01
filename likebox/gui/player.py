
from PyQt4 import QtCore, QtGui
from nmevent import Event
from collections import OrderedDict

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

        self._controls = PlayerControls()
        self._sourcelist = PlayerSourceList(model)
        self._songview = PlayerSongView()
        self._menubar = PlayerMenuBar()
        self._playlistpicker = PlayerListPicker(model)

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

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel('Take songs from:'))
        hbox.addWidget(self._playlistpicker)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setMenuBar(self._menubar)

        self._controls.play.connect(self._on_play)
        self._controls.stop.connect(self._on_stop)
        self._controls.next.connect(self._on_next)
        self._sourcelist.playlist_selected.connect(self._on_playlist_selected)

    #     self._load_data()

    # def _load_data(self):
    #      for playlist in self._model.library.playlists:
    #          self._sourcelist.addPlaylist(playlist.name)

    def _on_play(self, *args):
        songs = self._songview.getSelected()
        self._model.play(songs[0])

    def _on_stop(self, *args):
        self._model.stop()

    def _on_next(self, *args):
        self._model.next()

    def _on_playlist_selected(self):
        self._songview.loadPlaylist(self._sourcelist.getSelectedPlaylist())

class PlayerControls(QtGui.QWidget):

    play = QtCore.pyqtSignal()
    stop = QtCore.pyqtSignal()
    next = QtCore.pyqtSignal()

    def __init__(self):
        super(PlayerControls, self).__init__()

        hbox = QtGui.QHBoxLayout(self)
        play = QtGui.QPushButton('Play')
        stop = QtGui.QPushButton('Stop')
        next = QtGui.QPushButton('Next')
        hbox.addWidget(play)
        hbox.addWidget(stop)
        hbox.addWidget(next)
        hbox.addStretch(1)

        play.clicked.connect(self.play)
        stop.clicked.connect(self.stop)
        next.clicked.connect(self.next)


class PlayerSourceList(QtGui.QListWidget):

    playlist_selected = QtCore.pyqtSignal()

    def __init__(self, model):
        super(PlayerSourceList, self).__init__()
        self._model = model
        self._sources = OrderedDict()
        self._sources[model.queue.name] = model.queue
        self._sources[model.library.name] = model.library
        for playlist in model.library.playlists:
            self._sources[playlist.name] = playlist
        for name in self._sources.iterkeys():
            QtGui.QListWidgetItem(name, self)

        self.itemSelectionChanged.connect(self.playlist_selected)

    def getSelectedPlaylist(self):
        items = self.selectedItems()
        if len(items) == 0:
            return None
        return self._sources[str(items[0].text())]

class PlayerSongView(QtGui.QTreeView):
    def __init__(self):
        super(PlayerSongView, self).__init__()
        self._song_model = SongListModel()
        self.setModel(self._song_model)

    def loadPlaylist(self, playlist):
        self._song_model.setSongs(playlist.songs)

    def getSelected(self):
        indexes = self.selectedIndexes()
        return [self._song_model.getSong(i) for i in indexes]

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

    def __init__(self, model):
        super(PlayerListPicker, self).__init__()
        self._sources = OrderedDict()
        self._sources[model.queue.name] = model.queue
        self._sources[model.library.name] = model.library
        for playlist in model.library.playlists:
            self._sources[playlist.name] = playlist
        for name in self._sources.iterkeys():
            self.addItem(name)

