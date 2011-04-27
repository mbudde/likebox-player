
class Song(object):

    def __init__(self, info=None):
        self.title = ""
        self.artist = ""
        self.album = ""
        self.year = None
        self.genre = None
        self.uri = None
        self.file = ""

        if info is not None:
            for k, v in info.iteritems():
                setattr(self, k, v)

    def __repr__(self):
        return '<Song [{0} by {1} from {2}]>'.format(self.title, self.artist, self.album)

