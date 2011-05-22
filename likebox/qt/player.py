
from PyQt4 import QtCore, QtGui
from nmevent import Event
from collections import OrderedDict

from .model import SongListModel

import logging
logger = logging.getLogger(__name__)


class Player(QtGui.QMainWindow):
    """Player main GUI."""

    def __init__(self, client):
        super(Player, self).__init__()

        self._client = client

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

        self._controls.play.connect(self._on_playpause)
        self._controls.pause.connect(self._on_playpause)
        self._controls.stop.connect(self._on_stop)
        self._controls.next.connect(self._on_next)
        self._controls.add.connect(self._on_add)
        self._sourcelist.playlist_selected.connect(self._on_playlist_selected)
        self._menubar.rescan.connect(self._on_perform_rescan)

        self._client.queue.updated += self._on_queue_updated
        self._client.current_song_changed += self._controls.updateSongInfo
        self._client.state_changed += self._on_state_change

        self._controls.updateState(client.state)

    def _on_playpause(self):
        self._client.playpause()

    def _on_stop(self):
        self._client.stop()

    def _on_next(self):
        self._client.next()

    def _on_add(self):
        songs = self._songview.getSelected()
        self._client.queue.add(songs[0])

    def _on_playlist_selected(self):
        self._songview.loadPlaylist(self._sourcelist.getSelectedPlaylist())

    def _on_update(self, sender, change):
        logger.debug(change)

    def _on_queue_updated(self, sender):
        logger.debug('queue changed')

    def _on_state_change(self, sender, state):
        self._controls.updateState(state)

    def _on_perform_rescan(self):
        self._client.rescan()


class PlayerControls(QtGui.QWidget):

    play = QtCore.pyqtSignal()
    pause = QtCore.pyqtSignal()
    stop = QtCore.pyqtSignal()
    next = QtCore.pyqtSignal()
    add = QtCore.pyqtSignal()

    def __init__(self):
        super(PlayerControls, self).__init__()

        self._playing = False

        hbox = QtGui.QHBoxLayout(self)
        self._playpause = QtGui.QPushButton('Play')
        stop = QtGui.QPushButton('Stop')
        next = QtGui.QPushButton('Next')
        add = QtGui.QPushButton('Add to Queue')
        hbox.addWidget(self._playpause)
        hbox.addWidget(stop)
        hbox.addWidget(next)
        hbox.addWidget(add)

        self._current_song = QtGui.QLabel('')
        hbox.addWidget(self._current_song)

        hbox.addStretch(1)

        self._playpause.clicked.connect(self._on_playpause)
        stop.clicked.connect(self.stop)
        next.clicked.connect(self.next)
        add.clicked.connect(self.add)

    def updateSongInfo(self, song):
        self._current_song.setText('{0[title]} by {0[artist]} from {0[album]}'.format(song))

    def updateState(self, state):
        self._playing = (state == 'play')
        self._playpause.setText('Pause' if self._playing else 'Play')

    def _on_playpause(self):
        if self._playing:
            self.pause.emit()
        else:
            self.play.emit()


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
        self.header().resizeSections(QtGui.QHeaderView.Stretch)

    def getSelected(self):
        indexes = self.selectedIndexes()
        return [self._song_model.getSong(i) for i in indexes]

    def _on_playlist_updated(self, sender):
        self._song_model.setSongs(self._playlist.songs)


class PlayerMenuBar(QtGui.QMenuBar):

    rescan = QtCore.pyqtSignal()

    def __init__(self):
        super(PlayerMenuBar, self).__init__()

        menu_file = self.addMenu('Likebox')
        item = QtGui.QAction("Rescan Music Library", menu_file)
        item.triggered.connect(self.rescan)
        menu_file.addAction(item)
        item = QtGui.QAction("Quit", menu_file)
        item.triggered.connect(self._on_quit)
        item.setShortcut(QtGui.QKeySequence("Ctrl+q"))
        menu_file.addAction(item)

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
        self._sources[client.library.name] = client.library
        for playlist in client.library.playlists:
            self._sources[playlist.name] = playlist
        for name in self._sources.iterkeys():
            self.addItem(name)
