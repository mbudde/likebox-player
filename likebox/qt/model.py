from PyQt4 import QtCore, QtGui

from ..utils import format_time

"""
class SourceListModel(QtCore.QAbstractItemModel):

    def __init__(self, model):
        super(SourceListModel, self).__init__()

        self._columns = (
            ('Title', 'title'),
        )
        self._sources = {
            model.queue,
            model.library,
            }

    def addSource(self, source):
        self.beginResetModel()
        self._songs = songs
        self.endResetModel()

    def index(self, row, col, parent=None):
        if not parent.isValid():
            return self.createIndex(row, col)
        return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if not index.isValid():
            return len(self._songs)
        return 0

    def columnCount(self, parent=None):
        return len(self._columns)

    def data(self, index, role=None):
        if not (index.isValid() and role == QtCore.Qt.DisplayRole):
            return None
        song = self._songs[index.row()]
        key = self._columns[index.column()][1]
        return song[key]

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemFlags(0)
        return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def headerData(self, section, orientation, role=None):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._columns[section][0]
        return None
"""


class SongListModel(QtCore.QAbstractItemModel):
    """ItemModel for song table view. See Qt docs on
    QAbstractItemModel."""

    def __init__(self, parent=None):
        super(SongListModel, self).__init__(parent)

        self._columns = (
            ('Title', 'title'),
            ('Artist', 'artist'),
            ('Album', 'album'),
            ('Genre', 'genre'),
            ('Time', 'time', format_time)
        )
        self._songs = []

    @property
    def songs(self):
        return self._songs

    def getSong(self, index):
        if not index.isValid():
            return None
        return self._songs[index.row()]

    def setSongs(self, songs):
        self.beginResetModel()
        self._songs = songs
        self.endResetModel()

    def index(self, row, col, parent=None):
        if not parent.isValid():
            return self.createIndex(row, col)
        return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if not index.isValid():
            return len(self._songs)
        return 0

    def columnCount(self, parent=None):
        return len(self._columns)

    def data(self, index, role=None):
        if not (index.isValid() and role == QtCore.Qt.DisplayRole):
            return None
        song = self._songs[index.row()]
        key = self._columns[index.column()][1:]
        if len(key) == 2:
            key, formatter = key[0], key[1]
            return formatter(song[key])
        else:
            return song[key[0]]

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemFlags(0)
        return QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def headerData(self, section, orientation, role=None):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._columns[section][0]
        return None
