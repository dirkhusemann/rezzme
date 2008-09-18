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

import urllib
import os
import socket
import sys

import PyQt4.QtCore
import PyQt4.QtGui
from PyQt4.QtCore import SIGNAL

import RezzMe.bookmarks
import RezzMe.config.config
import RezzMe.exceptions
import RezzMe.gridinfo
import RezzMe.launcher
import RezzMe.parse
import RezzMe.ui.launcher
import RezzMe.ui.tray
import RezzMe.uri

timeout = 30
cfg = RezzMe.config.config.config()

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

if onMacOSX: import aemreceive.sfba as AE

class RezzMeQApplication(PyQt4.QtGui.QApplication):
    '''Wrapper class around QApplication adding exec state information.
       '''

    def __init__(self, *args):
        PyQt4.QtGui.QApplication.__init__(self, *args)
        self._started = False

    def exec_(self):
        self._started = True
        PyQt4.QtGui.QApplication.exec_()

    def _started(self):
        return self._started
    Started = property(fget = _started)



def ConnectToGrid(app, uri):
    uri = RezzMe.uri.Uri(uri = uri)

    # sanity check: rezzme: or opensim: scheme?
    if uri.Scheme != 'rezzme' and uri.Scheme != 'rezzmes':
        raise RezzMe.exceptions.RezzMeException('Oops: URI "%s" contains unknown scheme "%s"' % (uri, uri.Scheme))

    # get grid info from OpenSim server (todo: move into launcher.py)
    gridInfo = RezzMe.gridinfo.GetGridInfo(uri)

    # unless we already have avatar and password from the URI check
    # whether we can get credentials for uri via our extensive
    # collection of bookmarks...
    bookmarks = RezzMe.bookmarks.Bookmarks(os.path.expanduser('~/.rezzme.bookmarks'))
    bookmark = bookmarks.Bookmark(uri = uri)
    if all(bookmark.Credentials): 
        uri.Credentials = bookmark.Credentials

    launcher = RezzMe.ui.launcher.RezzMeLauncher(app = app, uri = uri, gridInfo = gridInfo, cfg = cfg)
    launcher.exec_()
                
    if launcher.OK:
        uri = launcher.Uri
        if launcher.Mode == 'bound':
            # don't save the password in 'bound' mode, it's temporary
            # in all likelihood anyhow
            password = uri.Password
            avatar = uri.Avatar

            uri.Password = None
            uri.Avatar = None

            bookmarks.Add(uri)
            bookmarks.Save()

            uri.Avatar = avatar
            uri.Password = password
            
        elif launcher.Mode == 'free':
            bookmarks.Add(uri)
            bookmarks.Save()

    else:
        return

    launcher = None
    
    if not uri.Avatar or not uri.Password:
        raise RezzMe.exceptions.RezzMeException('Oops: could not obtain avatar name and password from grid "%s"' % 
                                                gridInfo['gridname'])

    # ok, got everything, now construct the command line
    RezzMe.launcher.Launch(uri.Avatar, uri.Password, gridInfo, uri.Location)


# def RezzMeSystemTray(app):
#     tray = RezzMe.ui.tray.RezzMeTray(parent = None, app = app, cfg = cfg)
#     while not tray.Done:
#         app.exec_()

def RezzMeUri(app, args):
    if not args:
        raise RezzMe.exceptions.RezzMeException('Oops: no rezzme:// URI found. Is your protocol handler set up correctly?')

    uri = None
    for uri in args:
        uriLower = uri.lower()
        if uriLower.startswith('rezzme://') or uriLower.startswith('rezzmes://'): 
            ConnectToGrid(app, uri)
            if onMacOSX: 
                return
            else:
                sys.exit(0)

    raise RezzMe.exceptions.RezzMeException("hmm...couldn't find a rezzme(s):// URI in %s" % ' '.join(sys.argv))

class MacOSXAppleEventHandler(PyQt4.QtCore.QObject):
    def __init__(self, parent = None):
        super(MacOSXAppleEventHandler, self).__init__(parent)

        def _urlHandler(uri):
            self.emit(SIGNAL('rezzme'), uri)

        AE.installeventhandler(_urlHandler, 'GURLGURL', ('----', 'uri', AE.kAE.typeUnicodeText))
        


if __name__ == '__main__':
    # set the socket timeout
    socket.setdefaulttimeout(timeout)

    # need an QApplication context to signal errors
    app = RezzMeQApplication(sys.argv)

    args = sys.argv[1:]
    tray = None
    try:
        
        if onMacOSX:
            aeHandler = MacOSXAppleEventHandler()
            tray = RezzMe.ui.tray.RezzMeTray(parent = None, app = app, cfg = cfg)

            def rezzMe(uri, app = app):
                RezzMeUri(app = app, args = [uri])

            tray.connect(aeHandler, SIGNAL('rezzme'), rezzMe)
            app.exec_()

        else:
            if not args:
                tray = RezzMe.ui.tray.RezzMeTray(parent = None, app = app, cfg = cfg)
                while not tray.Done: app.exec_()
            else:
                RezzMeUri(app = app, args = args)
                app.exec_()

    except RezzMe.exceptions.RezzMeException, e:
        oops = PyQt4.QtGui.QMessageBox.critical(None, 'Virtual World Launcher Wizard', e.Message)
        sys.exit(1)

    sys.exit(0)

