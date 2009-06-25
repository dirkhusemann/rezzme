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
        protologfile = os.path.expanduser(protologfile)
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
    import socket
    
    import PyQt4.QtCore
    import PyQt4.QtGui

    import RezzMe.connect
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

timeout = 15

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

class RezzMeQApplication(PyQt4.QtGui.QApplication):
    def __init__(self, argv):
        self.Done = False
        super(RezzMeQApplication, self).__init__(argv)


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
    app = RezzMeQApplication(sys.argv)

    RezzMe.config.desktop.InstallProtocolHandlers()

    args = sys.argv[1:]
    tray = None
    try:

        # on MacOSX rezzme always runs in system tray mode and gets
        # the rezzme:// URIs via the GURL GURL AppleEvent from the OS
        if onMacOSX:

            # on MacOSX we need to be able to recieve AppleEvents
            import aemreceive.sfba as AppleEvents

            # the MacOSXAppleEventHandler derives from QObject so that
            # we can issue SIGNAL('rezzme')
            class MacOSXAppleEventHandler(PyQt4.QtCore.QObject):
                def __init__(self, parent = None):
                    super(MacOSXAppleEventHandler, self).__init__(parent)

                    # _urlHandler is the actual handler and emits
                    # SIGNAL('rezzme') with the actual uri as payload
                    def _urlHandler(uri):
                        self.emit(PyQt4.QtCore.SIGNAL('rezzme'), uri)

                    def _quitHandler():
                        logging.debug('rezzme.main: onMacOSX: quitHandler called')
                        self.emit(PyQt4.QtCore.SIGNAL('quitme'))
                    
                    # tie the GURL GURL AppleEvent to _urlHandler
                    AppleEvents.installeventhandler(_urlHandler, 'GURLGURL', ('----', 'uri', AppleEvents.kAE.typeUnicodeText))
                    AppleEvents.installeventhandler(_quitHandler, 'aevtquit')
                    logging.debug('rezzme.MacOSXAppleEventHandler: installed event handler for "GURLGURL"')

            # change log format
            if logHandler:
                logHandler.setFormatter(logging.Formatter('%(asctime)s [mac] %(levelname)-8s %(message)s',
                                                          '%a, %d %b %Y %H:%M:%S'))

            # instantiate our AppleEvent handler object
            logging.debug('rezzme.main: onMacOSX: installing MacOS AppleEvent handler')
            aeHandler = MacOSXAppleEventHandler()

            # instantiate system tray
            logging.debug('rezzme.main: onMacOSX: instantiating rezzme system tray')
            tray = RezzMe.ui.tray.RezzMeTrayWindow(parent = None, app = app, cfg = cfg)

            # create a closure to capture app and cfg
            def rezzMe(uri, app = app):
                logging.debug('rezzme.main: rezzme AppleEvent: uri %s', uri)
                RezzMe.connect.Connect(app = app, uri = uri, cfg = cfg)

            def quitMe(app = app):
                app.Done = True

            # connect SIGNAL('rezzme') to rezzMe()
            app.connect(aeHandler, PyQt4.QtCore.SIGNAL('rezzme'), rezzMe, PyQt4.QtCore.Qt.QueuedConnection)
            app.connect(aeHandler, PyQt4.QtCore.SIGNAL('quitme'), quitMe, PyQt4.QtCore.Qt.QueuedConnection)
            logging.debug('rezzme.main: onMacOSX: starting')

        # on linux or windows
        else:

            # no command line arguments supplied: system tray mode
            if not args:

                if logHandler:
                    # change log format
                    logHandler.setFormatter(logging.Formatter('%(asctime)s [systray] %(levelname)-8s %(message)s',
                                                              '%a, %d %b %Y %H:%M:%S'))

                logging.debug('rezzme.main: invoked without command line arguments, starting rezzme system tray')

                # instantiate system tray
                tray = RezzMe.ui.tray.RezzMeTrayWindow(parent = None, app = app, cfg = cfg)

            # command line arguments supplied: protocol handler mode
            else:
                
                if protologHandler:
                    # change log format
                    logging.info('rezzme.main: switching to proto handler logfile')
                    logging.getLogger().removeHandler(logHandler)
                    logging.getLogger().addHandler(protologHandler)
                    protologHandler.setFormatter(logging.Formatter('%(asctime)s [proto] %(levelname)-8s %(message)s',
                                                                   '%a, %d %b %Y %H:%M:%S'))
                
                logging.debug('rezzme.main: invoked with command line arguments: %s', ' '.join(args))

                uris = [u for u in args if u.lower().startswith('rezzme://') or u.lower().startswith('rezzmes://')]

                if not uris:
                    raise RezzMe.exceptions.RezzMeException('missing rezzme:// URI')
                
                # interact with user and grid via launcher
                logging.debug('rezzme.main: starting launcher GUI')
                RezzMe.connect.Connect(app = app, uri = uris[0], cfg = cfg)


        # stay in the PyQt4 event loop until system tray is terminated
        while not app.Done: app.exec_()

    except RezzMe.exceptions.RezzMeException, e:
        logging.critical('rezzme.main: caught rezzme exception: %s', e.Message, exc_info = True)
        oops = PyQt4.QtGui.QMessageBox.critical(None, 'RezzMe', e.Message)
        logging.critical('rezzme.main: exiting with retval 1')
        sys.exit(1)


    except BaseException, e:
        logging.critical('rezzme.main: caught base exception: %s', str(e), exc_info = True)
        sys.exit(2)
        

    logging.debug('rezzme.main: exiting normally with retval 0')
    if onMacOSX:
        AppleEvents.stopeventloop()
    sys.exit(0)

