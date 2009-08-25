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
import logging
import os
import sys
import urllib
import urllib2
import xml.etree.ElementTree as ET

import PyQt4.QtCore
import PyQt4.QtGui
import RezzMe.launcher
import RezzMe.parse
import RezzMe.ui.rezzme
import RezzMe.ui.client

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

black = 'rgb(0, 0, 0)'
red   = 'rgb(255, 0, 0)'
green = 'rgb(0, 170, 0)'
blue  = 'rgb(0, 0, 255)'

addNewClient = '>add new client<'

class RezzMeLauncher(PyQt4.QtGui.QDialog, RezzMe.ui.rezzme.Ui_RezzMe):

    def __init__(self, parent = None, app = None, cfg = None, uri = None, gridInfo = None, launcher = None):

        # sanity check
        if not uri: 
            logging.error('ui.RezzMeLauncher: uri not provided')
            raise RezzMe.exceptions.RezzMeException('uri not provided')

        # init: base and app
        super(RezzMeLauncher, self).__init__(parent)
        self._app = app
        self.setupUi(self)
        self._launcher = launcher
        
        # init: attributes
        # logging.debug('ui.RezzMeLauncher:__init__: uri %s', uri.SafeUri)
        logging.debug('ui.RezzMeLauncher:__init__: uri %s', uri)
        self._uri = uri
        self._gridInfo = gridInfo
        self._cfg = cfg
        self._bookmark = False
        self._ok = False
        self._isAvatar = True

        self._isNewbie = False
        self._appearanceUri = None
        self._canChangeOutfit = False
        self._changeOutfitRequested = False
        self._purgeCache = False

        self._userID = self._uri.UserId
        self._userPassword = None
        self._override = self._uri.Avatar is not None

        self._clients = self._launcher.ClientTags
        if not self._uri.Client or not launcher.ClientForTag(self._uri.Client):
            logging.debug('ui.launcher: setting client to %s', self._clients[0])
            self._uri.Client = self._clients[0]
        self._updateClients()
        
        logging.debug('ui.launcher: client selection: %s', ' '.join(self._clients))
        logging.debug('ui.launcher: instantiating object, uri %s', uri.SafeUri)


        # init: invariant GUI elements
        versionToolTip = unicode(self.labelVersion.toolTip()) % cfg['package']
        self.labelVersion.setToolTip(versionToolTip)

        self._tooltips = {}
        
        if 'authenticator' in gridInfo:
            if 'authgridname' in gridInfo:
                self._tooltips['userid'] = 'enter your %s user ID here' % gridInfo['authgridname']
                self._tooltips['password'] = 'enter your %s password here' % gridInfo['authgridname']
                logging.debug('ui.launcher: authgridname = %s', gridInfo['authgridname'])
            else:
                self._tooltips['userid'] = 'enter your %s user ID here' % gridInfo['gridname']
                self._tooltips['password'] = 'enter your %s password here' % gridInfo['gridname']

            if 'authuseridtooltip' in gridInfo:
                self._tooltips['userid'] = gridInfo['authuseridtooltip']
            if 'authpasswordtooltip' in gridInfo:
                self._tooltips['password'] = gridInfo['authpasswordtooltip']

        if 'appearanceuri' in gridInfo and (gridInfo['appearanceuri'].lower() == 'true' or gridInfo['appearanceuri'].lower() == 'yes'):
            self.checkBoxOutfit.setVisible(True)
            self._canChangeOutfit = True
        else:
            self.checkBoxOutfit.setVisible(False)
        
        if 'authenticator' in gridInfo:
            self._authenticator = gridInfo['authenticator']
        else:
            self._authenticator = None

        
        if self._authenticator:
            # set title
            if 'authgridname' in gridInfo:
                self.labelAuthenticationName.setText('<b>%s</b>' % gridInfo['authgridname'])
                self.labelAuthenticationName2.setText('<b>%s</b>' % gridInfo['authgridname'])
            else:
                self.labelAuthenticationName.setText('<b>%s credentials</b>' % gridInfo['gridname'])
                self.labelAuthenticationName2.setText('<b>%s credentials</b>' % gridInfo['gridname'])

        self._updateLabels()

        if self._isAvatar:
            self._status("please enter your avatar's name and password", green)
        else:
            self._status("please enter your user name and password", green)

        self.labelVersion.setText('%s/%s' % (cfg['package']['name'], 
                                             cfg['package']['version']))

        if self._override:
            self.tabWidget.setCurrentIndex(1)
        else:
            self.tabWidget.setCurrentIndex(0)
        self.show()
        self.raise_()

    # dialog core: UI logic contained in here
    def _updateLabels(self):
        if not self._authenticator or (self._authenticator and self._override):
            logging.debug('ui.launcher: avatar mode')

            self.labelAuthenticationName.setText('<b>Grid authentication</b>')
            self.labelAuthenticationName2.setText('<b>Grid authentication</b>')

            self.labelUser.setText('avatar &name:')
            self.lineEditUser.setToolTip('enter your avatar name here')
            self.labelUser2.setText('avatar &name:')
            self.lineEditUser2.setToolTip('enter your avatar name here')

            self.labelPassword.setText('&password:')
            self.lineEditPassword.setToolTip('enter your avatar password here')
            self.labelPassword2.setText('&password:')
            self.lineEditPassword2.setToolTip('enter your avatar password here')

            if self._authenticator:
                self.checkBoxOverride.setEnabled(True)
                if self._override:
                    self.checkBoxOverride.setChecked(True)
            else:
                self.checkBoxOverride.setEnabled(False)

            if self.tabWidget.currentIndex() == 0:
                self.lineEditUser.setFocus()
            else:
                self.lineEditUser2.setFocus()
                
            if self._uri.Avatar:
                self.lineEditUser.setText(self._uri.Avatar)
                self.lineEditUser2.setText(self._uri.Avatar)
                logging.debug('ui.launcher: avatar %s', self._uri.Avatar)

                if self.tabWidget.currentIndex() == 0:
                    self.lineEditPassword.setFocus()
                else:
                    self.lineEditPassword2.setFocus()

            else:
                self.lineEditUser.clear()
                self.lineEditUser2.clear()

                if self.tabWidget.currentIndex() == 0:
                    self.lineEditUser.setFocus()
                else:
                    self.lineEditUser2.setFocus()
                

            if self._uri.Password:
                self.lineEditPassword.setText(self._uri.Password)
                self.lineEditPassword2.setText(self._uri.Password)
                self.pushButtonOK.setEnabled(True)
                self.pushButtonOK2.setEnabled(True)
            else:
                self.lineEditPassword.clear()
                self.lineEditPassword.clear()
                self.pushButtonOK.setEnabled(False)
                self.pushButtonOK2.setEnabled(False)

            self._isAvatar = True

        else:

            logging.debug('ui.launcher: user mode')
            # set title
            if 'authgridname' in self._gridInfo:
                self.labelAuthenticationName.setText('<b>%s</b>' % self._gridInfo['authgridname'])
                self.labelAuthenticationName2.setText('<b>%s</b>' % self._gridInfo['authgridname'])
            else:
                self.labelAuthenticationName.setText('<b>%s credentials</b>' % self._gridInfo['gridname'])
                self.labelAuthenticationName2.setText('<b>%s credentials</b>' % self._gridInfo['gridname'])

            self.labelUser.setText('&user name:')
            self.lineEditUser.setToolTip(self._tooltips['userid'])
            self.labelUser2.setText('&user name:')
            self.lineEditUser2.setToolTip(self._tooltips['userid'])

            self.labelPassword.setText('&password:')
            self.lineEditPassword.setToolTip(self._tooltips['password'])
            self.labelPassword2.setText('&password:')
            self.lineEditPassword2.setToolTip(self._tooltips['password'])

            self.checkBoxOverride.setEnabled(True)


            # fill in user ID if known
            if self._userID:
                self.lineEditUser.setText(self._userID)
                self.lineEditUser2.setText(self._userID)
                self.lineEditPassword.setFocus()

                if self.tabWidget.currentIndex() == 0:
                    self.lineEditPassword.setFocus()
                else:
                    self.lineEditPassword2.setFocus()

            else:
                self.lineEditUser.clear()
                self.lineEditUser2.clear()

                if self.tabWidget.currentIndex() == 0:
                    self.lineEditUser.setFocus()
                else:
                    self.lineEditUser2.setFocus()

            self._isAvatar = False


        self.labelUri.setText(self._uri.SafeUri)
        self.labelUri.setToolTip(unicode(self.labelUri.toolTip()) % self._gridInfo)

    def _updateClients(self):
        self.comboBoxClients.clear()
        self.comboBoxClients.addItems(self._clients)
        self.comboBoxClients.addItem(addNewClient)
        self.comboBoxClients.setCurrentIndex(self._clients.index(self._uri.Client))


    def _status(self, msg, color = None):
        self.labelStatus.setText(msg)
        self.labelStatus2.setText(msg)
        if color: 
            self.labelStatus.setStyleSheet('QWidget { color: %s; font-size:10pt; }' % color)
            self.labelStatus2.setStyleSheet('QWidget { color: %s; font-size:10pt; }' % color)
        else:
            self.labelStatus.setStyleSheet('QWidget { color: %s; font-size:10pt; }' % black)
            self.labelStatus2.setStyleSheet('QWidget { color: %s; font-size:10pt; }' % black)
        self._app.sendPostedEvents()
        self._app.processEvents()

    def _authenticate(self):
        logging.debug('ui.launcher: starting authentication')
        keys = {}
        keys['rezzme'] = urllib.quote(self._uri.PlainUri, '')
        keys['rezzme_base'] = urllib.quote(self._uri.BaseUri, '')
        keys['avatar'] = urllib.quote(self._uri.Avatar, '') if self._uri.Avatar else 'None'
        keys['userid'] = self._userID
        keys['grid'] = urllib.quote(self._uri.BaseHttpUri, '')
        if self._uri.Region:
            keys['region'] = urllib.quote(self._uri.Region)
        else:
            keys['region'] = ''
        keys['host'] = urllib.quote(self._uri.Host)
        keys['port'] = urllib.quote(self._uri.Port)

        try:
            authUri = self._authenticator % keys
        except ValueError:
            logging.info('ui.launcher: authentication failed: ValueError on %s', self._authenticator);
            self._status('Ouch: authentication failed, authentication server seems to be mis-configured', red)
            return False
            
        logging.debug('ui.launcher: authUri %s', authUri)

        # we need an auth handler
        httpPasswordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        httpPasswordManager.add_password(realm = None, uri = authUri, 
                                         user = self._userID, passwd = self._userPassword)
        httpBasicAuthHandler = urllib2.HTTPBasicAuthHandler(httpPasswordManager)
        httpBasicAuthOpenener = urllib2.build_opener(httpBasicAuthHandler)
        urllib2.install_opener(httpBasicAuthOpenener)

        avatar = None
        password = None
        newbie = False
        appearanceUri = None
        try:
            self._status('trying to authenticate with %s' % self._uri.BaseHttpUri)
            req = urllib2.Request(authUri)
            req.add_header('Accept', 'text/xml')
            req.add_header('X-OpenSim-Region', keys['region'])
            authXml = ET.parse(urllib2.urlopen(req)).getroot()
            avatar = authXml.attrib['avatar']
            password = authXml.attrib['token']
            if 'newbie' in authXml.attrib:
                n = authXml.attrib['newbie'].lower()
                newbie = n == 'yes' or n == 'true'
            if 'appearance' in authXml.attrib:
                appearanceUri = authXml.attrib['appearance']
            if 'appearanceuri' in authXml.attrib:
                appearanceUri = authXml.attrib['appearanceuri']
            
        except urllib2.URLError, ue:
            logging.info('ui.launcher: authentication failed: %s', str(ue));
            status  = "hmm, you've encountered an unknown bug"
            if getattr(ue, 'code', None):
                # error codes on which the user can retry
                if ue.code == 500:
                    self._status('cannot authenticate you: authentication server has an internal problem')
                    return False
                if ue.code == 401:
                    self._status('user name or password are wrong or not known')
                    return False

                # error codes on which the user cannot retry
                if ue.code == 403:
                    status = 'you are not allowed in the target region'
                elif ue.code == 404:
                    status = 'target region does not exist'
                elif ue.code == 400:
                    status = 'missing region'

            if getattr(ue, 'reason', None):
                status = 'cannot authenticate you: %s ' % str(ue.reason)

            self.close()
            self._status(status)
            bye = PyQt4.QtGui.QMessageBox.critical(None, 'RezzMe', 'Sorry, cannot take you in-world: %s' % status)
            return False
        
        self._uri.Avatar = avatar
        self._uri.Password = password
        self._isNewbie = newbie
        self._appearanceUri = appearanceUri
        self._status('authenticated successfully with %s' % self._uri.BaseHttpUri)

        return True

    def _addClient(self):
        (tag, client) = self._launcher.GetClient()
        if not client:
            return
        self._clients = self._launcher.ClientTags
        # self._uri.Client = self._clients[0]
        self._uri.Client = tag
        self._updateClients()

    # properties
    @property
    def Override(self):
        return self._override

    @property
    def Uri(self):
        return self._uri

    @property
    def OK(self):
        return self._ok

    @property
    def BookmarkIt(self):
        return self._bookmark

    @property
    def IsAvatar(self):
        return self._isAvatar

    @property
    def IsNewbie(self):
        return self._isNewbie

    @property
    def AppearanceUri(self):
        return self._appearanceUri

    @property
    def CanChangeOutfit(self):
        return self._canChangeOutfit

    @property
    def ChangeOutfitRequested(self):
        return self._changeOutfitRequested

    @property
    def PurgeCacheRequested(self):
        return self._purgeCache


    # auto bindings
    @PyQt4.QtCore.pyqtSignature('bool')
    def on_checkBoxOverride_toggled(self, checked):
        self._override = checked
        self._updateLabels()

    @PyQt4.QtCore.pyqtSignature('bool')
    def on_checkBoxBookmark_toggled(self, checked):
        self._bookmark = checked

    @PyQt4.QtCore.pyqtSignature('bool')
    def on_checkBoxOutfit_toggled(self, checked):
        self._changeOutfitRequested = checked

    @PyQt4.QtCore.pyqtSignature('bool')
    def on_checkBoxPurgeCache_toggled(self, checked):
        self._purgeCache = checked


    @PyQt4.QtCore.pyqtSignature('QString')
    def on_comboBoxClients_activated(self, client):
        if not client:
            return
        client = unicode(client)
        if client == addNewClient:
            self._addClient()
        else:
            self._uri.Client = client


    # UserID and password
    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditUser_editingFinished(self):
        name = unicode(self.lineEditUser.text())
        if not name: return
        if self._isAvatar:
            self._uri.Avatar = name
        else:
            self._userID = name
            self._uri.UserId = name
        self.lineEditUser2.setText(name)

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditUser2_editingFinished(self):
        name = unicode(self.lineEditUser2.text())
        if not name: return
        if self._isAvatar:
            self._uri.Avatar = name
        else:
            self._userID = name
            self._uri.UserId = name
        self.lineEditUser.setText(name)


    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditPassword_editingFinished(self):
        password = unicode(self.lineEditPassword.text())
        if self._isAvatar:
            self._uri.Password = password
        else:
            self._userPassword = password

        if password:
            self.pushButtonOK.setEnabled(True)
            self.pushButtonOK2.setEnabled(True)
            self.lineEditPassword2.setText(password)
        else:
            self.pushButtonOK.setEnabled(False)
            self.pushButtonOK2.setEnabled(False)


    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditPassword2_editingFinished(self):
        password = unicode(self.lineEditPassword2.text())
        if self._isAvatar:
            self._uri.Password = password
        else:
            self._userPassword = password

        if password:
            self.pushButtonOK.setEnabled(True)
            self.pushButtonOK2.setEnabled(True)
            self.lineEditPassword.setText(password)
        else:
            self.pushButtonOK.setEnabled(False)
            self.pushButtonOK2.setEnabled(False)

    @PyQt4.QtCore.pyqtSignature('QString')
    def on_lineEditPassword_textEdited(self, text):
        # cannot use parameter text, as that is according to the docs
        # the text delta which could be empty, so take a look at the
        # QLineEdit widget
        if unicode(self.lineEditPassword.text()):
            self.pushButtonOK.setEnabled(True)
            self.pushButtonOK2.setEnabled(True)
            self.lineEditPassword2.setText(self.lineEditPassword.text())
        else:
            self.pushButtonOK.setEnabled(False)
            self.pushButtonOK2.setEnabled(False)

    @PyQt4.QtCore.pyqtSignature('QString')
    def on_lineEditPassword2_textEdited(self, text):
        # cannot use parameter text, as that is according to the docs
        # the text delta which could be empty, so take a look at the
        # QLineEdit widget
        if unicode(self.lineEditPassword2.text()):
            self.pushButtonOK.setEnabled(True)
            self.pushButtonOK2.setEnabled(True)
            self.lineEditPassword.setText(self.lineEditPassword2.text())
        else:
            self.pushButtonOK.setEnabled(False)
            self.pushButtonOK2.setEnabled(False)

    def captureAllInput(self):
        self.on_lineEditUser_editingFinished()
        self.on_lineEditPassword_editingFinished()

    def captureAllInput2(self):
        self.on_lineEditUser2_editingFinished()
        self.on_lineEditPassword2_editingFinished()

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonOK_clicked(self):
        self.captureAllInput()
        if not self._isAvatar and not self._authenticate():
                return None

        self.close()

        self._ok = True
        return self._uri

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonOK2_clicked(self):
        self.captureAllInput2()
        self.on_pushButtonOK_clicked()


