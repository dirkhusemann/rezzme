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
import os
import sys
import urllib

import PyQt4.QtCore
import PyQt4.QtGui

import RezzMe.bookmarks
import RezzMe.parse
import RezzMe.ui.edit
import RezzMe.ui.about
import RezzMe.resources

from PyQt4.QtCore import SIGNAL

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

class RezzMeTrayAbout(PyQt4.QtGui.QDialog, RezzMe.ui.about.Ui_About):

    def __init__(self, parent = None):
        super(RezzMeTrayAbout, self).__init__(parent)
        self.setupUi(self)
        logging.debug('RezzMe.ui.RezzMeTrayAbout: init')

        self.textBrowser.setSource(PyQt4.QtCore.QUrl('qrc:/about.html'))
        self.textBrowser.setOpenExternalLinks(True)

        self.show()


class RezzMeTrayWindow(PyQt4.QtGui.QDialog, RezzMe.ui.edit.Ui_RezzMeTrayEdit):

    def __init__(self, app = None, bookmarks = None, defaults = None, cfg = None,
                 parent = None):
        super(RezzMeTrayWindow, self).__init__(parent)

        self._bookmarks = bookmarks
        self._defaultBookmarks = defaults
        self._uri = {}
        self._tag = None

        self._app = app
        self._cfg = cfg

        # setup generated UI 
        self.setupUi(self)

        self._setupTrayIcon()
        self._desktopServices = PyQt4.QtGui.QDesktopServices()
        
        logging.debug('RezzMe.ui.RezzMeTrayEdit: init')
        if onMacOSX:
            logging.debug('RezzMe.ui.RezzMeTrayEdit: onMacOSX: disabling focus for buttons')
            self.pushButtonAdd.setFocusPolicy(PyQt4.QtCore.Qt.NoFocus)
            self.pushButtonChange.setFocusPolicy(PyQt4.QtCore.Qt.NoFocus)
            self.pushButtonDelete.setFocusPolicy(PyQt4.QtCore.Qt.NoFocus)
            self.pushButtonCancel.setFocusPolicy(PyQt4.QtCore.Qt.NoFocus)

        self.comboBoxBookmarks.clear()
        self.comboBoxBookmarks.addItems(sorted(self._bookmarks.Displays))

        if self._defaultBookmarks: 
            logging.debug('RezzMe.ui.RezzMeTrayEdit: adding menu entries')
            self.comboBoxBookmarks.addItems(sorted(self._defaultBookmarks.Displays))

        self._trayIcon.show()

        #        self.show()
        #        self.raise_()

    def __delete__(self):
        self._bookmarks = None
        self._uri = None

    def _setupTrayIcon(self):
        logging.debug('RezzMe.ui.tray: setting up system tray icon')
        self._trayIcon = PyQt4.QtGui.QSystemTrayIcon(self)
        self._trayIcon.setIcon(PyQt4.QtGui.QIcon(':/rezzme-16x16.png'))

        self._menu = None
        self._bookmarks = RezzMe.bookmarks.Bookmarks('~/.rezzme.bookmarks')
        logging.debug('RezzMe.ui.tray: loaded bookmarks')
        self._defaultBookmarks = RezzMe.bookmarks.Bookmarks()

        if self._cfg and 'default rezzmes' in self._cfg:
            for tag in self._cfg['default rezzmes']:
                self._defaultBookmarks.Add(RezzMe.uri.Uri(uri = self._cfg['default rezzmes'][tag], tag = tag))
                logging.debug('RezzMe.ui.tray: adding default bookmark: %s', self._cfg['default rezzmes'][tag])

        self._reloadMenu()
        self._done = False

        PyQt4.QtCore.QObject.connect(self._trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self._iconActivated)
        logging.debug('RezzMe.ui.tray: connected slot')

    def _iconActivated(self, reason):
        logging.debug('RezzMe.ui.tray: activated')
        self._reloadMenu()

    def _reloadMenu(self):
        self._menu = PyQt4.QtGui.QMenu(self)
        self._bookmarks.Reload()
        logging.debug('RezzMe.ui.tray._reloadMenu: reloading menu')

        menu = {}
        for bookmark in self._bookmarks.Bookmarks:
            menu[bookmark.Display] = lambda bookmark = bookmark: self._action(bookmark)
            logging.debug('RezzMe.ui.tray._reloadMenu: adding bookmark %s', bookmark)

        for entry in sorted(menu.keys()):
            self._menu.addAction(entry, menu[entry])

        if menu: self._menu.addSeparator()

        if self._defaultBookmarks:
            menu = {}
            for bookmark in self._defaultBookmarks.Bookmarks:
                menu[bookmark.Display] = lambda bookmark = bookmark: self._action(bookmark)
                logging.debug('RezzMe.ui.tray._reloadMenu: adding default bookmark %s', bookmark)

            for entry in sorted(menu.keys()): 
                self._menu.addAction(entry, menu[entry])
            if menu:
                self._menu.addSeparator()

        self._menu.addAction('edit or add rezzme:// bookmarks', self.showNormal)
        self._menu.addAction('about...', self._about)
        self._menu.addAction('quit', self._quit)

        self._trayIcon.setContextMenu(self._menu)
        logging.debug('RezzMe.ui.tray._reloadMenu: menu (re)set')

    def _activate(self):
        self.showNormal()

    def _action(self, bookmark):
        logging.debug('RezzMe.ui.tray._action: selected %s', bookmark)
        self._desktopServices.openUrl(PyQt4.QtCore.QUrl(bookmark.FullUri))
        

    def _about(self):
        rezzMeAbout = RezzMeTrayAbout()
        rezzMeAbout.exec_()

    def _quit(self):
        self._done = True
        self._app.quit()

    def _updateRezzMeUri(self, gridHost = None, 
                         region = None, x = None, y = None, z = None,
                         avatar = None, Description = None, updateGui = True):
        host = None
        port = None

        if gridHost:
            if ':' in gridHost: 
                (host, port) = gridHost.split(':')
            else:
                host = gridHost
            if host: self._uri['host'] = host
            if port: self._uri['port'] = port

        if avatar is not None:
            if not avatar:
                del self._uri['avatar']
            else:
                self._uri['avatar'] = avatar
        if region: self._uri['region'] = urllib.quote(region)
        if x: self._uri['x'] = x
        if y: self._uri['y'] = y
        if z: self._uri['z'] = z

        # sanity check: can happen when no input
        if not 'host' in self._uri: return

        rezzme = 'rezzme://'
        if 'avatar' in self._uri: rezzme += '%s@' % self._uri['avatar']
        rezzme += self._uri['host']
        if 'port' in self._uri: rezzme += ':%s' % self._uri['port']
        rezzme += '/'
        if 'region' in self._uri: rezzme += self._uri['region']
        if 'x' in self._uri: rezzme += '/%s' % self._uri['x']
        if 'y' in self._uri: rezzme += '/%s' % self._uri['y']
        if 'z' in self._uri: rezzme += '/%s' % self._uri['z']

        if not updateGui: return rezzme

        # reset line edit fields
        self.lineEditGridHost.setText('')
        self.lineEditRegion.setText('')
        self.lineEditX.setText('')
        self.lineEditY.setText('')
        self.lineEditZ.setText('')
        self.lineEditAvatarName.setText('')

        if 'port' in self._uri: 
            self.lineEditGridHost.setText('%(host)s:%(port)s' % self._uri)
        else:
            self.lineEditGridHost.setText('%(host)s' % self._uri)
        if 'region' in self._uri: self.lineEditRegion.setText(urllib.unquote(self._uri['region'])) 
        if 'x' in self._uri: self.lineEditX.setText(str(self._uri['x'])) 
        if 'y' in self._uri: self.lineEditY.setText(str(self._uri['y'])) 
        if 'z' in self._uri: self.lineEditZ.setText(str(self._uri['z'])) 
        if 'avatar' in self._uri: self.lineEditAvatarName.setText(self._uri['avatar']) 
        self.labelRezzMe.setText(rezzme)

    def _fillXYZ(self, x = None, y = None, z = None):
        if x is not None and 'x' not in self._uri: self._uri['x'] = x
        if y is not None and 'y' not in self._uri: self._uri['y'] = y
        if z is not None and 'z' not in self._uri: self._uri['z'] = z

    def _gDone(self):
        return self._done
    Done = property(fget = _gDone)

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditGridHost_editingFinished(self):
        self._updateRezzMeUri(gridHost = unicode(self.lineEditGridHost.text()))

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditRegion_editingFinished(self):
        self._updateRezzMeUri(region = unicode(self.lineEditRegion.text()))

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditX_editingFinished(self):
        x = unicode(self.lineEditX.text())
        if x.isdigit(): self._fillXYZ(y = 0, z = 0)
        self._updateRezzMeUri(x = x)

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditY_editingFinished(self):
        y = unicode(self.lineEditY.text())
        if y.isdigit(): self._fillXYZ(x = 0, z = 0)
        self._updateRezzMeUri(y = y)

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditZ_editingFinished(self):
        z = unicode(self.lineEditZ.text())
        if z.isdigit(): self._fillXYZ(x = 0, y = 0)
        self._updateRezzMeUri(z = z)

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditAvatarName_editingFinished(self):
        self._updateRezzMeUri(avatar = unicode(self.lineEditAvatarName.text()))

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditTag_editingFinished(self):
        tag = unicode(self.lineEditTag.text()).strip()
        if tag: self._tag = tag

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonAdd_clicked(self):
        bookmark = self._updateRezzMeUri(updateGui = False)
        logging.debug('RezzMe.ui.tray.edit.on_pushButtonAdd_clicked: bookmark %s', bookmark)
        self._bookmarks.Add(RezzMe.uri.Uri(uri = bookmark, tag = self._tag))
        self._bookmarks.Save()
        self._reloadMenu()

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonChange_clicked(self):
        old = unicode(self.comboBoxBookmarks.currentText())
        new = self._updateRezzMeUri(updateGui = False)

        oldBookmark = self._bookmarks.FindBestMatch(display = old)
        newBookmark = RezzMe.uri.Uri(uri = new, tag = self._tag)
        logging.debug('RezzMe.ui.tray.edit.on_pushButtonChange_clicked: old %s -> new %s', oldBookmark, newBookmark)

        if oldBookmark:
            self._bookmarks.Change(oldBookmark, newBookmark)
            self._bookmarks.Save()
        self._reloadMenu()

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonDelete_clicked(self):
        bookmark = unicode(self.comboBoxBookmarks.currentText())
        bookmark = self._bookmarks.FindBestMatch(display = bookmark)

        logging.debug('RezzMe.ui.tray.edit.on_pushButtonDelete_clicked: bookmark %s', bookmark)
        if bookmark:
            self._bookmarks.Delete(bookmark)
            self._bookmarks.Save()
        self._reloadMenu()

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonCancel_clicked(self):
        logging.debug('RezzMe.ui.tray.edit.on_pushButtonCancel_clicked')


    @PyQt4.QtCore.pyqtSignature('QString')
    def on_comboBoxBookmarks_activated(self, display):
        self.pushButtonChange.setEnabled(True)

        display = unicode(display)
        bookmark = self._bookmarks.FindBestMatch(display = display)
        logging.debug('RezzMe.ui.tray.edit.on_comboBoxBookmarks_activated: %s', bookmark)

        if not bookmark:
            bookmark = self._defaultBookmarks.FindBestMatch(display = display)
            self.pushButtonChange.setEnabled(False)

        self._uri = bookmark.Dict
        self._updateRezzMeUri()

        tag = bookmark.Tag
        if tag: self.lineEditTag.setText(tag)
        else: self.lineEditTag.clear()
        self._tag = tag


    @PyQt4.QtCore.pyqtSignature('bool')
    def on_checkBoxEditBookmark_toggled(self, checked):
        if checked:
            self.on_comboBoxBookmarks_activated(self.comboBoxBookmarks.currentText())
        else:
            self.labelRezzMe.clear()
            self.lineEditGridHost.clear()
            self.lineEditRegion.clear()
            self.lineEditX.clear()
            self.lineEditY.clear()
            self.lineEditZ.clear()
            self.lineEditAvatarName.clear()


