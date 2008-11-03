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
import urllib
import _winreg

import RezzMe.exceptions
import RezzMe.launchers.hippo

class PlatformLauncher(object):
    
    def __init__(self):

        # try for hippo opensim viewer first
        try:
            hovk = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\OpenSim\\Hippo OpenSim Viewer')

            if hovk:
                hovp = _winreg.QueryValueEx(hovk, None)[0]
                hove = _winreg.QueryValueEx(hovk, 'Exe')[0]
                hippoExe = '%s\\%s' % (hovp, hove)

                self._clients['hippo'] = hippoExe
        except:
            pass

        try:
            slk = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '\\secondlife\\shell\\open\\command')
            if slk:
                slp = _winreg.QueryValueEx(slk, None)[0].split('"')[1]

                self._clients['secondlife'] = slp
        except:
            pass


    def _gClients(self):
        return self._clients
    Clients = property(fget = _gClients)

    def _gClientPattern(self):
        return 'client executable (*.exe *.bat)'
    ClientPattern = property(fget = _gClientPattern)

    
    def Launch(self, avatar, password, gridInfo, clientName, client, location):

        clientArgs = [ ]
        clientArgs += ['-loginuri', gridInfo['login']]
        clientArgs += ['-multiple']

        keys = gridInfo.keys()
        if 'welcome' in keys: clientArgs += ['-loginpage', gridInfo['welcome']]
        if 'economy' in keys: clientArgs += ['-helperuri', gridInfo['economy']]

        # need to mirror clientArgs into logArgs to avoid capturing
        # password into log file
        logArgs = clientArgs[:]
        if avatar and password:
            clientArgs += ['-login']
            # on windows we use os.exec*(), thus, no quote
            clientArgs += urllib.unquote(avatar).split()
            logArgs = clientArgs[:]

            clientArgs += [password]
            logArgs += ['**********']


        if clientName == 'hippo':
            userGridXml = os.path.expanduser('~/Application Data/Hippo_OpenSim_Viewer/user_settings/grid_info.xml')
            userGridXml = os.path.normcase(userGridXml)

            defaultGridXml = os.path.join(os.path.dirname(clientPaths[clientName]), 'app_settings', 'default_grids.xml')

            gridnick = RezzMe.launchers.hippo.HippoGridInfoFix(gridInfo, userGridXml, defaultGridXml)
            clientArgs += ['-grid', gridnick]
            logArgs += ['-grid', gridnick]

        if location:
            clientArgs += [location]
            logArgs += [location]
        
        # all systems go: start client
        clientArgs = [ client ] + clientArgs
        logArgs = [ client ] + logArgs

        logging.debug('RezzMe.launchers.win32: client args %s', ' '.join(logArgs))
        os.execv(client, clientArgs)
