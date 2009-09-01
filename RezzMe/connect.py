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

import logging
import sys
import urllib2
import xml.etree.ElementTree

import PyQt4.QtCore
import PyQt4.QtGui

import RezzMe.exceptions
import RezzMe.uri
import RezzMe.bookmarks
import RezzMe.launcher

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

def Connect(app, uri, cfg):

    try:
        class setup(PyQt4.QtCore.QThread):
            def __init__(self, uri, lastStep = 'launching rezzme dialog'):
                self.uri = uri
                self.lastStep = lastStep

                # information to make available to GUI code
                self.gridInfo = None
                self.updateBookmarks = False
                self.bookmarks = None

                # status information
                self.exception = None
                self.canceled = False
                self.done = False
                
                super(setup, self).__init__()

            def progress(self, msg, step):
                self.emit(PyQt4.QtCore.SIGNAL('progress'), msg, step)

            def cancel(self):
                self.emit(PyQt4.QtCore.SIGNAL('cancel'))
                self.canceled = self.done = True

            def run(self):
                try:
                    self.progress('checking URI', 1)
                    logging.debug('connect.Connect: uri %s', uri)
                    self.uri = RezzMe.uri.Uri(uri = uri)
                
                    # sanity check: rezzme: or opensim: scheme?
                    if self.uri.Scheme != 'rezzme' and self.uri.Scheme != 'rezzmes':
                        raise RezzMe.exceptions.RezzMeException('Oops: URI "%s" contains unknown scheme "%s"' %
                                                                (self.uri, self.uri.Scheme))
                
                
                    # get grid info from OpenSim server 
                    self.progress('fetching connection details for virtual world', 2)
                    logging.debug('connect.Connect: try to get grid info from %s', self.uri)
                    self.gridInfo = RezzMe.gridinfo.GetGridInfo(self.uri)

                    if self.gridInfo['error'] == 'non-existent':
                        logging.info('Connect: target region on virtual world does not exist')
                        raise RezzMe.exceptions.RezzMeException('Oops: target region "%s" on virtual world "%s" does not exist' %
                                                                (self.uri.DecodedRegion, self.uri.SafeUri))
                    elif self.gridInfo['error']:
                        logging.info('Connect: cannot fetch gridinfo')
                        raise RezzMe.exceptions.RezzMeException('Oops: cannot fetch connection details from virtual world "%s": %s' %
                                                                (self.uri.SafeUri, self.gridInfo['error']))

                    if self.canceled: return

                    # check whether target server is reachable
                    if self.gridInfo['platform'].lower() == 'opensim' and self.gridInfo['regioninfoavailable']:
                        regionInfoUri = ''
                        try:
                            regionInfoUri = '%sadmin/regioninfo/' % (self.gridInfo['login'])
                            logging.info('Connect: opensim platform: checking connectivity to virtual world: %s via %s',
                                         self.uri, regionInfoUri)
                            if self.gridInfo['error'] == 'timeout':
                                self.progress('failed getting connection details, checking reachability', 3)
                            else:
                                self.progress('checking reachability', 3)
                            regioninfoXml = xml.etree.ElementTree.parse(urllib2.urlopen(regionInfoUri)).getroot()
                        except Exception, e:
                            logging.info('Connect: cannot connect to target virtual world: %s via %s: %s', self.uri, regionInfoUri, str(e))
                            # self.progress("connectivity test failed, keep fingers crossed!", 3)
                            raise RezzMe.exceptions.RezzMeException('Oops: cannot connect to virtual world %s' % uri)
                    else:
                        logging.info('Connect: secondlife platform: skipping connectivity test')
                        self.progress('skipping reachability check (non-opensim grid)', 3)
    
                    if self.canceled: return
            
                    # unless we already have avatar and password from the URI, check
                    # whether we can get credentials for uri via our extensive
                    # collection of bookmarks...
                    self.progress('loading and searching bookmarks', 4)

                    self.bookmarks = RezzMe.bookmarks.Bookmarks(RezzMe.utils.ExpandUser('~/.rezzme.bookmarks'))
                    bookmark = self.bookmarks.FindBestMatch(uri = self.uri)
                    if bookmark:
                        logging.debug('connect.Connect: found bookmark %s for uri %s', bookmark.SafeUri, self.uri)
            
                        if any(bookmark.Credentials): 
                            logging.debug('connect.Connect: obtained credentials')
                            self.uri.Credentials = bookmark.Credentials
            
                        if bookmark.UserId:
                            logging.debug('connect.Connect: using user ID "%s" from bookmarks', bookmark.UserId)
                            self.uri.UserId = bookmark.UserId
            
                        self.uri.Client = bookmark.Client
                        self.uri.Extensions = bookmark.Extensions
            
                        # update display value if bookmark was pointing to the same place
                        if self.uri.PlainUri == bookmark.PlainUri:
                            self.uri.Display = bookmark.Display
                            self.updateBookmarks = True

                    self.progress(self.lastStep, 5)

                except RezzMe.exceptions.RezzMeException, rme:
                    self.exception = rme
                    self.cancel()
                self.done = True
    
        uri = RezzMe.uri.Uri(uri = uri)
        if uri.AutoLogin:
            setup = setup(uri, lastStep = 'logging in to virtual world')
        else:
            setup = setup(uri)

        progress = PyQt4.QtGui.QProgressDialog('', 'abort', 0, 5)
        progress.setWindowTitle('RezzMe setup')
        progress.setWindowModality(PyQt4.QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)

        def advance(msg, step):
            progress.setLabelText(msg)
            progress.setValue(step)

        PyQt4.QtCore.QObject.connect(setup, PyQt4.QtCore.SIGNAL('progress'), advance, PyQt4.QtCore.Qt.QueuedConnection)
        PyQt4.QtCore.QObject.connect(setup, PyQt4.QtCore.SIGNAL('cancel'), progress.cancel, PyQt4.QtCore.Qt.QueuedConnection)
        PyQt4.QtCore.QObject.connect(progress, PyQt4.QtCore.SIGNAL('canceled()'), setup.cancel, PyQt4.QtCore.Qt.QueuedConnection)

        setup.start()
        progress.show()

        # while not setup.done:
        progress.exec_()

        if setup.exception:
            raise setup.exception

        if setup.canceled:
            if not onMacOSX:
                app.Done = True
            return

        gridInfo = setup.gridInfo

        launcher = RezzMe.launcher.ClientLauncher()
        if not launcher.ClientTags:
            launcher.GetClient('Hmm, cannot find a virtual world client. Please select a virtual world client and give it a tag:')
            if not launcher.ClientTags:
                raise RezzMe.exceptions.RezzMeException('no virtual world client found')

        # bow out early if we already have all the information we need
        if uri.AutoLogin:
            if not uri.Client or not launcher.ClientForTag(uri.Client):
                logging.debug('ui.launcher: setting client to %s', launcher.ClientTags[0])
                uri.Client = launcher.ClientTags[0]

            try:
                launcher.Launch(uri.Avatar, uri.Password, gridInfo, uri.Client, uri.Location)
            except Exception, le:
                # attemptedClient = '%s - %s' % (uri.Client, launcher.ClientForTag(uri.Client))
                raise RezzMe.exceptions.RezzMeException('could not launch virtual world client: %s' % uri.Client)
            if not onMacOSX:
                app.Done = True
            return
        
            
        uri = setup.uri
        updateBookmarks = setup.updateBookmarks
        bookmarks = setup.bookmarks

        logging.debug('connect.Connect: starting launcher GUI')
    
        oldUri = RezzMe.uri.Uri(uri)
        logging.debug('connect.Connect: calling launcher UI with %s', uri.SafeUri)
        ui = RezzMe.ui.launcher.RezzMeLauncher(app = app, uri = uri, gridInfo = gridInfo, cfg = cfg, launcher = launcher)
        ui.exec_()
    
        logging.debug('connect.Connect: launcher UI returned %s', ui.OK)

        if not ui.OK:
            if not onMacOSX:
                app.Done = True
            return
        
        uri = ui.Uri
            
        logging.debug('connect.Connect: uri returned: %s', uri.SafeUri)
        # logging.debug('connect.Connect: uri returned: %s', uri)
        # user mode: update the bookmark if the user wants us to or if the bookmark was an exact match
        if not ui.IsAvatar and (ui.BookmarkIt or updateBookmarks):

            logging.debug('connect.Connect: saving userId')
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

            logging.debug('connect.Connect: saving/updating avatar name/password')
            bookmarks.Delete(oldUri)
            bookmarks.Add(uri, save = True)
    
        if not uri.Avatar or not uri.Password:
            raise RezzMe.exceptions.RezzMeException('Oops: could not obtain avatar name and password from grid "%s"' % 
                                                    gridInfo['gridname'])


        logging.debug('connect.Connect: IsNewbie %s, ChangeOutfitRequested %s', ui.IsNewbie, ui.ChangeOutfitRequested)

        if (ui.IsNewbie and ui.AppearanceUri) or (ui.ChangeOutfitRequested and ui.AppearanceUri):
            if ui.IsNewbie:
                # newbie alert: send them to AppearanceUri to select an outfit
                PyQt4.QtGui.QMessageBox.information(None, 'RezzMe',
                                                    'It seems like this is the first time you are visiting the virtual world. '
                                                    'Your browser should open with a web page in just a moment. '
                                                    'You can select an outfit for your avatar on that web page '
                                                    'and then continue on your way in-world.',
                                                    PyQt4.QtGui.QMessageBox.Ok, PyQt4.QtGui.QMessageBox.Ok)
            else:
                # newbie alert: send them to AppearanceUri to select an outfit
                PyQt4.QtGui.QMessageBox.information(None, 'RezzMe',
                                                    'You indicated that you want to obtain a new outfit for your avatar. '
                                                    'Your browser should open with a web page in just a moment. '
                                                    'You can select an outfit for your avatar on that web page '
                                                    'and then continue on your way in-world.',
                                                    PyQt4.QtGui.QMessageBox.Ok, PyQt4.QtGui.QMessageBox.Ok)

            
            PyQt4.QtGui.QDesktopServices().openUrl(PyQt4.QtCore.QUrl(str(ui.AppearanceUri)))
            
            if not onMacOSX:
                app.Done = True
            return
            

        # ok, got everything, now construct the command line
        logging.debug('connect.Connect: starting client for %s', uri.SafeUri)
        try:
            launcher.Launch(uri.Avatar, uri.Password, gridInfo, uri.Client, uri.Location, ui.PurgeCacheRequested)
        except Exception, le:
            # attemptedClient = '%s - %s' % (uri.Client, launcher.ClientForTag(uri.Client))
            raise RezzMe.exceptions.RezzMeException('could not launch virtual world client: %s' % le.message)
    

    except RezzMe.exceptions.RezzMeException, rme:
        logging.critical('connect.Connect: caught rezzme exception: %s', rme.Message, exc_info = True)
        PyQt4.QtGui.QMessageBox.critical(None, 'RezzMe', rme.Message)

    if not onMacOSX:
        app.Done = True
