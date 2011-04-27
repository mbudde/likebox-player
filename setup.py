#!/usr/bin/python

from distutils.core import setup

setup(
    name = 'Likebox',
    version = '0.1',
    description = 'Musicplayer with voting',
    author = 'Likebox developers',
    packages = [
        'likebox'
    ],
    scripts = [
        'bin/likebox',
    ],
    requires = [
        'PyQT',
        'python_mpd',
    ],
)
