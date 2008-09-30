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

import logging
import os
import urllib
import lxml.etree as ET

import RezzMe.exceptions
import RezzMe.launchers.hippo

clients = ['hippo', 'secondlife']
clientPaths = {'hippo'     : 'hippo_opensim_viewer',
               'secondlife': 'secondlife'}

for c in clients:
    found = False
    for bin in os.environ['PATH'].split(':'):
        t = '%s/%s' % (bin, clientPaths[c])
        if os.path.exists(t):
            clientPaths[c] = t
            found = True
            break
    if not found: 
        del clients[c]
        del clientPaths[c]


def Clients():
    return (clients, clientPaths)

def Launch(avatar, password, gridInfo, clientName, location):
    clientArgs = [ ]
    clientArgs += ['-loginuri', gridInfo['login']]
    clientArgs += ['-multiple']

    keys = gridInfo.keys()
    if 'welcome' in keys: clientArgs += ['-loginpage', gridInfo['welcome']]
    if 'economy' in keys: clientArgs += ['-helperuri', gridInfo['economy']]

    # mirror clientArgs into logArgs to avoid capturing passwords into
    # log files
    logArgs = clientArgs[:]
    if avatar and password:
        clientArgs += ['-login']
        clientArgs += map(lambda x: "'%s'" % x, urllib.unquote(avatar).split())
        logArgs = clientArgs[:]

        clientArgs += [password]
        logArgs += ["'**********'"]

    # locate client:
    client = clientPaths[clientName]
    if not client: 
        logging.critical('RezzMe.launchers.linux2: did not find %s on path %s', ' or '.join(clients), sys.environ['PATH'])
        raise RezzMe.exceptions.RezzMeException('cannot find suitable client! install hippo viewer or secondlife client and try again')

    logging.debug('RezzMe.launchers.linux2: found client %s', client)

    if 'hippo' == clientName:
        gridnick = RezzMe.launchers.hippo.HippoGridInfoFix(gridInfo)
        clientArgs += ['-grid', gridnick]
        logArgs += ['-grid', gridnick]

    # has to come last
    if location:
        clientArgs += [location]
        logArgs += [location]

    # all systems go: start client
    clientArgs = [ client ] + clientArgs
    logArgs = [ client ] + logArgs

    logging.debug('RezzMe.launchers.linux2: client %s args %s', client, ' '.join(logArgs))
    os.execvp(client, clientArgs)


