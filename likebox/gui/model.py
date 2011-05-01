from PyQt4 import QtCore, QtGui

class SongListModel(QtCore.QAbstractItemModel):

    def __init__(self, parent=None):
        super(SongListModel, self).__init__(parent)

        self._columns = (
            ('Title', 'title'),
            ('Artist', 'artist'),
            ('Album', 'album'),
            ('Genre', 'genre'),
            ('Time', 'time')
        )
        self._songs = []

    @property
    def songs(self):
        return self._songs

    def setSongs(self, songs):
        self.beginResetModel()
        self._songs = songs
        self.endResetModel()

    def index(self, row, col, parent=None):
        if not parent.isValid():
            return self.createIndex(row, col)
        print parent.row(), parent.column()
        return QtCore.QModelIndex()
        # return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if not index.isValid():
            return len(self._songs)
        return 0

    def columnCount(self, parent=None):
        return len(self._columns)

    def data(self, index, role=None):
        print index.row(), index.column(), index.isValid()
        if not (index.isValid() and
                role == QtCore.Qt.DisplayRole and
                index.row() < len(self._songs)):
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
