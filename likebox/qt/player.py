
from PyQt4 import QtCore, QtGui
from nmevent import Event
from collections import OrderedDict

from .model import SongListModel

class Player(QtGui.QMainWindow):

    play = Event()
    stop = Event()
    pause = Event()

    def __init__(self, client):
        super(Player, self).__init__()

        self._client = client
        # self._client.updates += self._on_update
        # idle.change.connect(self._on_change)

        self.setGeometry(100, 100, 700, 500)
        self.setWindowTitle('Likebox')

        self._controls = PlayerControls()
        self._sourcelist = PlayerSourceList(client)
        self._songview = PlayerSongView()
        self._menubar = PlayerMenuBar()
        self._playlistpicker = PlayerListPicker(client)

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

        self._client.queue.updated += self._on_queue_updated
        self._client.current_song_changed += self._controls.updateSongInfo

    def _on_play(self, *args):
        songs = self._songview.getSelected()
        self._client.play(songs[0])

    def _on_stop(self, *args):
        self._client.stop()

    def _on_next(self, *args):
        self._client.next()

    def _on_playlist_selected(self):
        self._songview.loadPlaylist(self._sourcelist.getSelectedPlaylist())

    def _on_update(self, sender, change):
        print change

    def _on_queue_updated(self, sender):
        print 'queue changed'

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

        self._current_song = QtGui.QLabel('')
        hbox.addWidget(self._current_song)

        hbox.addStretch(1)

        play.clicked.connect(self.play)
        stop.clicked.connect(self.stop)
        next.clicked.connect(self.next)

    def updateSongInfo(self, song):
        self._current_song.setText('{0[title]} by {0[artist]} from {0[album]}'.format(song))

class PlayerSourceList(QtGui.QListWidget):

    playlist_selected = QtCore.pyqtSignal()

    def __init__(self, client):
        super(PlayerSourceList, self).__init__()
        self._client = client
        self._sources = OrderedDict()
        self._sources[client.queue.name] = client.queue
        self._sources[client.library.name] = client.library
        for playlist in client.library.playlists:
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
        self._playlist = None

    def loadPlaylist(self, playlist):
        if self._playlist:
            self._playlist.updated -= self._on_playlist_updated
        self._playlist = playlist
        self._playlist.updated += self._on_playlist_updated
        self._song_model.setSongs(playlist.songs)

    def getSelected(self):
        indexes = self.selectedIndexes()
        return [self._song_model.getSong(i) for i in indexes]

    def _on_playlist_updated(self, sender):
        self._song_model.setSongs(self._playlist.songs)

class PlayerMenuBar(QtGui.QMenuBar):

    def __init__(self):
        super(PlayerMenuBar, self).__init__()

        menu_file = self.addMenu('Likebox')
        quit = QtGui.QAction("Quit", menu_file)
        quit.triggered.connect(self._on_quit)
        quit.setShortcut(QtGui.QKeySequence("Ctrl+q"))
        menu_file.addAction(quit)

        menu_options = self.addMenu('Edit')
        remove_song = QtGui.QAction("Remove Song", menu_options)
        remove_song.triggered.connect(self._on_remove_song)
        menu_options.addAction(remove_song)

    def _on_quit(self, *args):
        QtGui.qApp.quit()

    def _on_remove_song(self, *args):
        pass


class PlayerListPicker(QtGui.QComboBox):

    def __init__(self, client):
        super(PlayerListPicker, self).__init__()
        self._sources = OrderedDict()
        self._sources[client.queue.name] = client.queue
        self._sources[client.library.name] = client.library
        for playlist in client.library.playlists:
            self._sources[playlist.name] = playlist
        for name in self._sources.iterkeys():
            self.addItem(name)
