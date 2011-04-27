

class PlaybackController(object):

    def __init__(self):
        self._playqueue = None
        self._source = None
        self._shuffle_mode = None
        self._repeat_mode = None
        self._stop_when_finished = False

    def first(self):
        pass

    def next(self, restart=None, change_immediately=True):
        pass

    def previous(self, restart=None):
        pass

    def previous_or_restart(self):
        pass

    @property
    def playqueue(self):
        return self._playqueue
    @playqueue.setter
    def playqueue(self, value):
        self._playqueue = value

    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, value):
        self._source = value

    @property
    def shuffle_mode(self):
        return self._shuffle_mode
    @shuffle_mode.setter
    def shuffle_mode(self, value):
        self._shuffle_mode = value

    @propety
    def repeat_mode(self):
        return self._repeat_mode
    @repeat_mode.setter
    def repeat_mode(self, value):
        self._repeat_mode = value

    @propety
    def stop_when_finished(self):
        return self._stop_when_finished
    @repeat_mode.setter
    def repeat_mode(self, value):
        self._stop_when_finished = value
