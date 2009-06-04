#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright (c) Contributors, http://opensimulator.org/
# See CONTRIBUTORS.TXT for a full list of copyright holders.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the OpenSim Project nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE DEVELOPERS ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
rezzme.py is a little launcher tool that knows about the GridInfo
protocol. it expects the grid coordinates to be passed as a
command line argument either as a "rezzme:" or as an "opensim:" style
URI:

        rezzme://osgrid.org:8002/

you can also provide region/X/Y/Z coordinates:

        rezzme://osgrid.org:8002/Wright%20Plaza/128/50/75

and, it also understands avatar names and passwords:

        rezzme://mr%20smart:secretpassword@osgrid.org:8002/Wright%20Plaza/128/50/75

'''

# early initialization: load config, setup logging
import os
import sys

logHandler = None
protologHandler = None

try:
    import logging
    import logging.handlers
    import RezzMe.config.config

    cfg = RezzMe.config.config.config()
    # set up logging support
    if 'level' in cfg['debug']:
        level = eval('logging.%s' % cfg['debug']['level'])
    else:
        level = logging.CRITICAL

    logfile = cfg['debug']['logfile'] if 'logfile' in cfg['debug'] else '~/.rezzme.log'
    protologfile = cfg['debug']['protologfile'] if 'protologfile' in cfg['debug'] else '~/.rezzme-proto.log'
    logsize = cfg['debug']['logsize'] if 'logsize' in cfg['debug'] else 1000 * 100

    if logfile:
        logfile = os.path.expanduser(logfile)
        protologfile = os.path.expanduser(logfile)
        if logfile.startswith('~/') and sys.platform == 'win32' and 'USERPROFILE' in os.environ:
            logfile = '%s/%s' % (os.environ['USERPROFILE'], logfile[2:])
        if protologfile.startswith('~/') and sys.platform == 'win32' and 'USERPROFILE' in os.environ:
            protologfile = '%s/%s' % (os.environ['USERPROFILE'], protologfile[2:])

        logHandler = logging.handlers.RotatingFileHandler(logfile, 'a', logsize)
        logHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',
                                                  '%a, %d %b %Y %H:%M:%S'))
        protologHandler = logging.handlers.RotatingFileHandler(protologfile, 'a', logsize)
        protologHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',
                                                       '%a, %d %b %Y %H:%M:%S'))
   
        logging.getLogger().addHandler(logHandler)
        logging.getLogger().setLevel(level)

    else:
        logging.basicConfig(level    = level,
                            format   = '%(asctime)s %(levelname)-8s %(message)s',
                            datefmt  = '%a, %d %b %Y %H:%M:%S')
except BaseException, e:
    print >>sys.stderr, 'failed to do early-initialization: %s', str(e)
    sys.exit(1)

# late initialization: the rest
try:
    import urllib
    import os
    import socket
    import sys
    
    import PyQt4.QtCore
    import PyQt4.QtGui
    from PyQt4.QtCore import SIGNAL
    
    import RezzMe.config.desktop
    import RezzMe.bookmarks
    import RezzMe.exceptions
    import RezzMe.gridinfo
    import RezzMe.launcher
    import RezzMe.parse
    import RezzMe.ui.launcher
    import RezzMe.ui.tray
    import RezzMe.uri
    import RezzMe.utils
except ImportError, e:
    logging.critical('rezzme: import error: %s', str(e), exc_info = True)
    sys.exit(1)
except BaseException, e:
    logging.critical('rezzme: the unexpected happened: %s', str(e), exc_info = True)
    sys.exit(1)

timeout = 30

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'


if onMacOSX: 
    import aemreceive.sfba as AE


def ConnectToGrid(app, uri):
    logging.debug('rezzme.ConnectToGrid: uri %s', uri)
    uri = RezzMe.uri.Uri(uri = uri)
    # logging.debug('rezzme.ConnectToGrid: uri resolved to %s', uri.SafeUri)

    # sanity check: rezzme: or opensim: scheme?
    if uri.Scheme != 'rezzme' and uri.Scheme != 'rezzmes':
        raise RezzMe.exceptions.RezzMeException('Oops: URI "%s" contains unknown scheme "%s"' % (uri, uri.Scheme))

    # get grid info from OpenSim server (todo: move into launcher.py)
    logging.debug('rezzme.ConnectToGrid: try to get grid info from %s', uri)
    gridInfo = RezzMe.gridinfo.GetGridInfo(uri)

    # unless we already have avatar and password from the URI, check
    # whether we can get credentials for uri via our extensive
    # collection of bookmarks...
    updateBookmarks = False
    bookmarks = RezzMe.bookmarks.Bookmarks(RezzMe.utils.ExpandUser('~/.rezzme.bookmarks'))
    bookmark = bookmarks.FindBestMatch(uri = uri)
    if bookmark:
        logging.debug('rezzme.ConnectToGrid: found bookmark %s for uri %s', bookmark.SafeUri, uri.SafeUri)
        # logging.debug('rezzme.ConnectToGrid: found bookmark %s for uri %s', bookmark, uri)
        if any(bookmark.Credentials): 
            logging.debug('rezzme.ConnectToGrid: obtained credentials')
            uri.Credentials = bookmark.Credentials
            # updateBookmarks = True
        if bookmark.UserId:
            logging.debug('rezzme.ConnectToGrid: using user ID "%s" from bookmarks', bookmark.UserId)
            uri.UserId = bookmark.UserId
            # updateBookmarks = True
        uri.Client = bookmark.Client
        uri.Extensions = bookmark.Extensions
        # update display value if bookmark was pointing to the same place
        if uri.PlainUri == bookmark.PlainUri:
            uri.Display = bookmark.Display
            updateBookmarks = True
        

    logging.debug('rezzme.ConnectToGrid: starting launcher GUI')
    launcher = RezzMe.launcher.ClientLauncher()
    if not launcher.ClientTags:
        launcher.GetClient('Hmm, cannot find a virtual world client. Please select a virtual world client and give it a tag:')
        if not launcher.ClientTags:
            raise RezzMe.exceptions.RezzMeException('RezzMe.launcher: no virtual world client found')


    oldUri = RezzMe.uri.Uri(uri)
    logging.debug('rezzme.ConnectToGrid: calling launcher UI with %s', uri.SafeUri)
    ui = RezzMe.ui.launcher.RezzMeLauncher(app = app, uri = uri, gridInfo = gridInfo, cfg = cfg, launcher = launcher)
    ui.exec_()

    logging.debug('rezzme.ConnectToGrid: launcher returned %s', ui.OK)
    if ui.OK:
        uri = ui.Uri
            
        logging.debug('rezzme.ConnectToGrid: uri returned: %s', uri.SafeUri)
        # logging.debug('rezzme.ConnectToGrid: uri returned: %s', uri)
        # user mode: update the bookmark if the user wants us to or if the bookmark was an exact match
        if not ui.IsAvatar and (ui.BookmarkIt or updateBookmarks):

            logging.debug('rezzme.ConnectToGrid: saving userId')
            # don't save the password in 'bound' mode, it's temporary
            # in all likelihood anyhow
            password = uri.Password
            avatar = uri.Avatar

            uri.Password = None
            uri.Avatar = None

            # delete the old bookmark, add the new one, then drop the
            # bookmarks object to avoid it picking up the password and
            # avatar
            bookmarks.Delete(oldUri)
            bookmarks.Add(uri, save = True)
            bookmarks = None

            uri.Avatar = avatar
            uri.Password = password
            
        elif ui.IsAvatar and (ui.BookmarkIt or updateBookmarks):

            logging.debug('rezzme.ConnectToGrid: saving/updating avatar name/password')
            bookmarks.Delete(oldUri)
            bookmarks.Add(uri, save = True)

    else:
        return

    if not uri.Avatar or not uri.Password:
        raise RezzMe.exceptions.RezzMeException('Oops: could not obtain avatar name and password from grid "%s"' % 
                                                gridInfo['gridname'])

    # ok, got everything, now construct the command line
    logging.debug('rezzme.ConnectToGrid: starting client for %s', uri.SafeUri)
    launcher.Launch(uri.Avatar, uri.Password, gridInfo, uri.Client, uri.Location)


def RezzMeUri(app, args):
    if not args:
        raise RezzMe.exceptions.RezzMeException('Oops: no rezzme:// URI found. Is your protocol handler set up correctly?')

    uri = None
    for uri in args:
        uriLower = uri.lower()
        logging.debug('rezzme.RezzMeUri: looking at %s', uriLower)
        if uriLower.startswith('rezzme://') or uriLower.startswith('rezzmes://'): 
            logging.debug('rezzme.RezzMeUri: %s is proper rezzme:// URI', uriLower)
            ConnectToGrid(app, uri)
            return

    raise RezzMe.exceptions.RezzMeException("hmm...couldn't find a rezzme(s):// URI in %s" % ' '.join(sys.argv))

class MacOSXAppleEventHandler(PyQt4.QtCore.QObject):
    def __init__(self, parent = None):
        super(MacOSXAppleEventHandler, self).__init__(parent)

        def _urlHandler(uri):
            self.emit(SIGNAL('rezzme'), uri)

        logging.debug('rezzme.MacOSXAppleEventHandler: installed event handler for "GURLGURL"')
        AE.installeventhandler(_urlHandler, 'GURLGURL', ('----', 'uri', AE.kAE.typeUnicodeText))
        


if __name__ == '__main__':
    # slightly generous banner makes it easier to find start of trace in log file :-)
    logging.info('                                        ')
    logging.info('========================================')
    logging.info('rezzme.py version %s on %s' %( cfg['package']['version'], sys.platform))
    logging.info('========================================')
    logging.info('                                        ')

    # set the socket timeout
    socket.setdefaulttimeout(timeout)

    # need an QApplication context to signal errors
    app = PyQt4.QtGui.QApplication(sys.argv)

    RezzMe.config.desktop.InstallProtocolHandlers()

    args = sys.argv[1:]
    tray = None
    try:
        
        if onMacOSX:
            # change log format
            logHandler.setFormatter(logging.Formatter('%(asctime)s [mac] %(levelname)-8s %(message)s',
                                                      '%a, %d %b %Y %H:%M:%S'))


            logging.debug('rezzme.main: onMacOSX: installing MacOS AppleEvent handler')
            aeHandler = MacOSXAppleEventHandler()
            logging.debug('rezzme.main: onMacOSX: instantiating rezzme system tray')
            tray = RezzMe.ui.tray.RezzMeTrayWindow(parent = None, app = app, cfg = cfg)

            def rezzMe(uri, app = app):
                RezzMeUri(app = app, args = [uri])

            tray.connect(aeHandler, SIGNAL('rezzme'), rezzMe)
            logging.debug('rezzme.main: onMacOSX: starting rezzme system tray')
            app.exec_()

        else:

            if not args:
                logHandler.setFormatter(logging.Formatter('%(asctime)s [systray] %(levelname)-8s %(message)s',
                                                          '%a, %d %b %Y %H:%M:%S'))
                logging.debug('rezzme.main: invoked without command line arguments, starting rezzme system tray')
                tray = RezzMe.ui.tray.RezzMeTrayWindow(parent = None, app = app, cfg = cfg)
                while not tray.Done: app.exec_()
            else:
                logging.getLogger().removeHandler(logHandler)
                logging.getLogger().addHandler(protologHandler)
                protologHandler.setFormatter(logging.Formatter('%(asctime)s [proto] %(levelname)-8s %(message)s',
                                                               '%a, %d %b %Y %H:%M:%S'))
                logging.debug('rezzme.main: invoked with command line arguments: %s', ' '.join(args))
                logging.debug('rezzme.main: starting launcher GUI')
                RezzMeUri(app = app, args = args)

    except RezzMe.exceptions.RezzMeException, e:
        logging.critical('rezzme.main: caught rezzme exception: %s', e.Message, exc_info = True)
        oops = PyQt4.QtGui.QMessageBox.critical(None, 'Virtual World Launcher Wizard', e.Message)
        logging.critical('rezzme.main: exiting with retval 1')
        sys.exit(1)

    except BaseException, e:
        logging.critical('rezzme.main: caught base exception: %s', str(e), exc_info = True)
        sys.exit(2)
        

    logging.debug('rezzme.main: exiting normally with retval 0')
    sys.exit(0)

