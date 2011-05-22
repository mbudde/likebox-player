from __future__ import division


def format_time(seconds):
    if isinstance(seconds, basestring):
        seconds = int(seconds)
    hours, rest = seconds // (60*60), seconds % (60*60)
    minutes, seconds = rest // 60, rest % 60
    if hours > 0:
        return '{0}:{1:02}:{2:02}'.format(hours, minutes, seconds)
    else:
        return '{0}:{1:02}'.format(minutes, seconds)
