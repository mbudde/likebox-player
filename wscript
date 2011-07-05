#!/usr/bin/python

out = 'build'

VERSION = '0.0.1'
APPNAME = 'likebox'

def options(opt):
    opt.load('compiler_c vala')

def configure(conf):
    # conf.env.CC = 'clang'
    # conf.env.append_value('CFLAGS', ['-Wno-unused-value'])
    conf.load('compiler_c')
    conf.check_cfg(
        package         = 'glib-2.0',
        uselib_store    = 'GLIB',
        atleast_version = '2.26.0',
        mandatory       = True,
        args            = '--cflags --libs')
    conf.check_cfg(
        package         = 'gtk+-2.0',
        uselib_store    = 'GTK',
        atleast_version = '2.10.0',
        mandatory       = True,
        args            = '--cflags --libs')
    conf.check_cfg(
        package         = 'gstreamer-0.10',
        uselib_store    = 'GST',
        mandatory       = True,
        args            = '--cflags --libs')
    conf.check_cfg(
        package         = 'gee-1.0',
        uselib_store    = 'GEE',
        mandatory       = True,
        args            = '--cflags --libs')
    conf.check_cfg(
        package         = 'sqlite3',
        uselib_store    = 'SQLITE',
        mandatory       = True,
        args            = '--cflags --libs')
    conf.check_cfg(
        package         = 'taglib_c',
        uselib_store    = 'TAGLIB',
        mandatory       = True,
        args            = '--cflags --libs')

    conf.load('vala', funs='')
    conf.check_vala(min_version=(0, 13, 0), branch=(0, 14))

def build(bld):
    bld.program(
        packages      = 'gtk+-2.0 gstreamer-0.10 sqlite3 gee-1.0 taglib_c',
        target        = 'likebox',
        uselib        = 'GTK GLIB GST GEE SQLITE TAGLIB',
        source        = bld.path.ant_glob('src/**/*.vala'),
        vala_defines  = ['DEBUG']
        )
