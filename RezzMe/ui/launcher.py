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

import ConfigParser
import os
import urllib
import urllib2
import xml.etree.ElementTree as ET

import PyQt4.QtCore
import PyQt4.QtGui
import RezzMe.bookmarks
import RezzMe.credentials
import RezzMe.parse
import RezzMe.ui.rezzme

from PyQt4.QtCore import SIGNAL

onMacOS = hasattr(PyQt4.QtGui, "qt_mac_set_native_menubar")

black = 'rgb(0, 0, 0)'
red   = 'rgb(255, 0, 0)'
green = 'rgb(0, 170, 0)'
blue  = 'rgb(0, 0, 255)'

class RezzMeLauncher(PyQt4.QtGui.QDialog, RezzMe.ui.rezzme.Ui_RezzMe):

    def __init__(self, parent = None, app = None, cfg = None, uri = None, gridInfo = None):

        # sanity check
        if not uri: 
            raise RezzMe.exceptions.RezzMeException('uri not provided')

        # init: base and app
        super(RezzMeLauncher, self).__init__(parent)
        self._app = app
        self.setupUi(self)
        
        # init: attributes
        self._uri = uri
        self._gridInfo = gridInfo
        self._bookmark = False
        self._ok = False

        self._credentials = RezzMe.credentials.Credentials(os.path.expanduser('~/.rezzme.credentials'))
        self._userID = self._credentials.Credential(uri)
        self._userPassword = None


        # load GUI
        if 'authenticator' in gridInfo:
            self.pushButtonOverride.setEnabled(True)
            self._authenticator = gridInfo['authenticator']
        else:
            self.pushButtonOverride.setEnabled(False)
            self._authenticator = None

        self.labelUri.setText(uri.SafeUri)
        self.labelGridName.setText(gridInfo['gridname'])
        
        if uri.Region:
            self.labelRegion.setText(urllib.unquote(uri.Region))
        else:
            self.labelRegion.clear()

        if self._authenticator:
            # set title
            if 'authgridname' in gridInfo:
                self.labelAuthenticationName.setText('<b>%s</b>' % gridInfo['authgridname'])
            else:
                self.labelAuthenticationName.setText('<b>%s credentials</b>' % gridInfo['gridname'])
            # fill in user ID if known
            if self._userID:
                self.lineEditUserID.setText(self._userID)


        if uri.Avatar: 
            self.lineEditAvatarName.setText(uri.Avatar)
        else:
            self.lineEditAvatarName.clear()

        if uri.Password:
            self.lineEditAvatarPassword.setText(uri.Password)
            self.pushButtonOK.setEnabled(True)
        else:
            self.lineEditAvatarPassword.clear()
            self.pushButtonOK.setEnabled(False)

        self.labelVersion.setText('%s/%s' % (cfg['package']['name'], 
                                             cfg['package']['version']))


        if self._authenticator: 
            self._boundMode()
        else:
            self._freeMode()

        self.setAttribute(PyQt4.QtCore.Qt.WA_DeleteOnClose)

        self.show()
        self.raise_()


    def _status(self, msg, color = None):
        self.labelStatus.setText(msg)
        if color: 
            self.labelStatus.setStyleSheet('QWidget { color: %s }' % color)
        else:
            self.labelStatus.setStyleSheet('QWidget { color: %s }' % black)
        self._app.sendPostedEvents()
        self._app.processEvents()


    def _boundMode(self):
        self._mode = 'bound'
        self.stackedWidget.setCurrentWidget(self.bound)
        self._status('enter your user ID and password', color = green)

    def _freeMode(self):
        self._mode = 'free'
        self.stackedWidget.setCurrentWidget(self.free)
        self._status('enter your avatar name and password', color = green)


    def _authenticate(self):
        keys = {}
        keys['rezzme'] = urllib.quote(self._uri.PlainUri, '')
        keys['rezzme_base'] = urllib.quote(self._uri.BaseUri, '')
        keys['avatar'] = self._uri.Avatar
        keys['userid'] = self._userID
        keys['grid'] = urllib.quote(self._uri.BaseHttpUri, '')

        authUri = self._authenticator % keys

        # we need an auth handler
        httpPasswordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        httpPasswordManager.add_password(realm = None, uri = authUri, 
                                         user = self._userID, passwd = self._userPassword)
        httpBasicAuthHandler = urllib2.HTTPBasicAuthHandler(httpPasswordManager)
        httpBasicAuthOpenener = urllib2.build_opener(httpBasicAuthHandler)
        urllib2.install_opener(httpBasicAuthOpenener)

        avatar = None
        password = None
        try:
            self._status('trying to authenticate with %s' % self._uri.BaseHttpUri)
            req = urllib2.Request(authUri)
            req.add_header('Accept', 'text/xml')
            authXml = ET.parse(urllib2.urlopen(req)).getroot()
            avatar = authXml.attrib['avatar']
            password = authXml.attrib['token']
        except:
            self._status('failed to authenticate with %s' % self._uri.BaseHttpUri)
            print 'failed to authenticate via %s' % authUri
            return False
        
        self._uri.Avatar = avatar
        self._uri.Password = password
        self._status('authenticated successfully with %s' % self._uri.BaseHttpUri)

        return True

    # properties
    def _mode(self):
        return self._mode
    Mode = property(fget = _mode)


    def _uri(self):
        return self._uri
    Uri = property(fget = _uri)


    def _ok(self):
        return self._ok
    OK = property(fget = _ok)

    # auto bindings
    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonOverride_clicked(self):
        self._boundMode()

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonOverrideProvided_clicked(self):
        self._freeMode()
    
    @PyQt4.QtCore.pyqtSignature('bool')
    def on_checkBoxBookmark_toggled(self, checked):
        self._bookmark = checked


    # UserID and password
    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditUserID_editingFinished(self):
        self._userID = unicode(self.lineEditUserID.text())
        if self._userID:
            self._credentials.Add(self._uri, self._userID)
            self._credentials.Save()

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditUserPassword_editingFinished(self):
        self._userPassword = unicode(self.lineEditUserPassword.text())
        if self._userPassword:
            self.pushButtonOK.setEnabled(True)
        else:
            self.pushButtonOK.setEnabled(False)

    @PyQt4.QtCore.pyqtSignature('QString')
    def on_lineEditUserPassword_textEdited(self, text):
        if text:
            self.pushButtonOK.setEnabled(True)
        else:
            self.pushButtonOK.setEnabled(False)

    # Avatar name and password
    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditAvatarName_editingFinished(self):
        self._uri.Avatar = unicode(self.lineEditAvatarName.text())

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditAvatarPassword_editingFinished(self):
        self._uri.Password = unicode(self.lineEditAvatarPassword.text())

    @PyQt4.QtCore.pyqtSignature('QString')
    def on_lineEditAvatarPassword_textEdited(self, text):
        if text:
            self.pushButtonOK.setEnabled(True)
        else:
            self.pushButtonOK.setEnabled(False)


    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonOK_clicked(self):
        if self.Mode == 'bound':
            if not self._authenticate():
                return None

        self.close()

        self._ok = True
        return self._uri