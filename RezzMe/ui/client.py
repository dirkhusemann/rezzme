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

import PyQt4.QtCore
import PyQt4.QtGui
from PyQt4.QtCore import SIGNAL

import RezzMe.ui.clientselector

class RezzMeClientSelector(PyQt4.QtGui.QDialog, RezzMe.ui.clientselector.Ui_ClientSelector):

    def __init__(self, parent = None, msg = 'Select a new virtual world client:', clientLauncher = None):

        # init: base and app
        super(RezzMeClientSelector, self).__init__(parent)
        self.setupUi(self)

        if msg: self.labelMessage.setText(msg)

        self._launcher = clientLauncher

        self._clientPath = None
        self._clientTag = None

        self._ok = False
        
        self.show()

    def _gClient(self):
        return (self._clientPath, self._clientTag)
    Client = property(fget = _gClient)

    def _gOK(self):
        return self._ok
    OK = property(fget = _gOK)

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonOK_clicked(self):
        if not self._clientPath or not self._clientTag:
            return None

        self.close()
        self._ok = True

    @PyQt4.QtCore.pyqtSignature('')
    def on_pushButtonSelectClient_clicked(self):
        self._clientPath = unicode(PyQt4.QtGui.QFileDialog.getOpenFileName(self, 'Select virtual world client', '.', 
                                                                           self._launcher.ClientPattern));
        if self._clientPath:
            self.labelClientPath.setText(self._clientPath)

    @PyQt4.QtCore.pyqtSignature('')
    def on_lineEditClientTag_editingFinished(self):
        self._clientTag = unicode(self.lineEditClientTag.text())

