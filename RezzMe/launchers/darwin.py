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
import subprocess
import sys
import urllib
import xml.etree.ElementTree

import RezzMe.exceptions
import RezzMe.launchers.hippo

import PyQt4.QtCore

class PlatformLauncher(object):


    def __init__(self):
        self._clientsDefault = {'secondlife': '/Applications/Second Life.app/Contents/MacOS/Second Life'}
        self._clients = {}

        for c in self._clientsDefault:
            logging.debug('darwin: checking client %s with path %s', c, self._clientsDefault[c])
            if os.path.exists(self._clientsDefault[c]):
                self._clients[c] = self._clientsDefault[c]
                logging.debug('darwin: found client %s at path %s', c, self._clientsDefault[c])
            else:
                logging.debug('darwin: no client %s at path %s', c, self._clientsDefault[c])
                
            
    def _gClients(self):
        return self._clients
    Clients = property(fget = _gClients)

    def _gClientPattern(self):
        return 'client executable (*)'
    ClientPattern = property(fget = _gClientPattern)


    def VerifyClient(self, path):
        if not os.path.exists(path): return None

        infoPlistPath = '%s/Contents/Info.plist' % path
        if not os.path.exists(infoPlistPath): return None

        executable = None
        try:
            infoPlist = xml.etree.ElementTree.parse(open(infoPlistPath, 'r'))
            kv = infoPlist.findall('/dict/*')
            kv = ['%s:%s' % (k.tag, k.text) for k in kv]
            executable = kv[kv.index('key:CFBundleExecutable') + 1].split(':')[1]
        except:
            return None

        execPath = '%s/Contents/MacOS/%s' % (path, executable)
        if os.path.exists(execPath): 
            return execPath

        return None

    def Launch(self, avatar, password, gridInfo, clientName, client, location, purge):
        
        avatar = urllib.unquote(avatar)

        clientArgs = [ ]
        clientArgs += ['-loginuri', gridInfo['login']]
        clientArgs += ['-multiple']

        keys = gridInfo.keys()
        if 'welcome' in keys: clientArgs += ['-loginpage', gridInfo['welcome']]
        if 'economy' in keys: clientArgs += ['-helperuri', gridInfo['economy']]

        if purge:
            clientArgs += ['--purge']

        logArgs = clientArgs[:]
        if avatar and password:
            clientArgs += ['-login']
            clientArgs += map(lambda x: "%s" % x, avatar.split())
            logArgs = clientArgs[:]

            clientArgs += [password]
            logArgs += ['**********']

        if location:
            clientArgs += [location]
            logArgs += [location]

        # all systems go: start client
        # need to invoke via shell as SecondLife client on MacOS does
        # funny things when invoked via os.exec*
        logging.debug('launchers.darwin: client %s %s', client, ' '.join(logArgs))
        try:
            # subprocess.call(clientArgs)
            PyQt4.QtCore.QProcess.startDetached(client, clientArgs)
        except Exception, e:
            logging.error('launchers.darwin: failed to start client: %s', str(e))


