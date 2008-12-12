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

from __future__ import with_statement

import ConfigParser
import logging
import os
import re
import sys
import RezzMe.exceptions
import RezzMe.ui.client

try:
    exec 'import RezzMe.launchers.%s as PlatformLauncher' % sys.platform
except ImportError, e:
    print 'no launcher available for this platform (%s) [%s]' % (sys.platform, str(e))
    raise e

class ClientLauncher(object):

    def __init__(self):
        self._clients = None
        self._configFile = os.path.expanduser('~/.rezzme.clients')

        logging.debug('RezzMe.launcher.Clients: determining available clients on %s', sys.platform)
        self._platformLauncher = PlatformLauncher.PlatformLauncher()
        self._clients = self._platformLauncher.Clients
        for c in self._clients:
            logging.info('RezzMe.launcher.Clients: found %s client at %s', c,self._clients[c])

        # add in user specified clients
        self._loadUserClients()
        for c in self._clients:
            logging.info('RezzMe.launcher.Clients: %s client at %s', c, self._clients[c])

    def _gClients(self):
        return self._clients.keys()
    ClientTags = property(fget = _gClients)

    def Launch(self, avatar, password, gridInfo, clientTag, location = None):
        '''launch platform specific virtual world client.
           '''

        if not clientTag in self._clients:
            raise RezzMeException('RezzMe.launcher: no client for for %s' % clientTag)

        self._platformLauncher.Launch(avatar, password, gridInfo, clientTag, self._clients[clientTag], location)
        

    def _loadUserClients(self):
        if not self._configFile or not os.path.exists(self._configFile): return

        config = ConfigParser.RawConfigParser()
        with open(self._configFile, 'r') as clientConfig:
            config.readfp(clientConfig)

        for tag in config.sections():
            if config.has_option(tag, 'path'):
                self._clients[tag] = config.get(tag, 'path')
                logging.debug('RezzMe.launcher._loadUserClients: adding %s - %s', tag, self._clients[tag])


    def GetClient(self, msg = None):
        clientSelector = RezzMe.ui.client.RezzMeClientSelector(msg = msg, clientLauncher = self)
        clientSelector.exec_()
        if not clientSelector.OK: return

        (client, tag) = clientSelector.Client
        if not tag in self._clients:
            self._clients[tag] = client
        self.SaveClients()
        logging.debug('RezzMe.launcher.GetClient: %s - %s', tag, client)
        return (tag, client)

    def AddClient(self, tag, path):
        self._clients[tag] = path


    def SaveClients(self):
        # save to ~/.rezzme.clients
        config = ConfigParser.RawConfigParser()
        for c in self._clients:
            if c not in config.sections():
                config.add_section(c)
            config.set(c, 'path', self._clients[c])

        with open(self._configFile, 'w') as clientConfig:
            config.write(clientConfig)


    def _gClientPattern(self):
        return self._platformLauncher.ClientPattern
    ClientPattern = property(fget = _gClientPattern)
