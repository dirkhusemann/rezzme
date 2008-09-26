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

clients = ['hippo_opensim_viewer', 'secondlife']

def FindClient(clients):
    for bin in os.environ['PATH'].split(':'):
        for c in clients:
            c = '%s/%s' % (bin, c)
            if os.path.exists(c):
                return c
    return None


def Launch(avatar, password, gridInfo, location):
    clientArgs = [ ]
    clientArgs += ['-loginuri', gridInfo['login']]
    clientArgs += ['-multiple']

    keys = gridInfo.keys()
    if 'welcome' in keys: clientArgs += ['-loginpage', gridInfo['welcome']]
    if 'economy' in keys: clientArgs += ['-helperuri', gridInfo['economy']]

    if avatar and password:
        clientArgs += ['-login']
        clientArgs += map(lambda x: "'%s'" % x, urllib.unquote(avatar).split())
        clientArgs += [password]

    if location:
        clientArgs += [location]

    # locate client:
    client = FindClient(clients)
    if not client: 
        logging.critical('RezzMe.launchers.linux2: did not find %s on path %s', ' or '.join(clients), sys.environ['PATH'])
        raise RezzMe.exceptions.RezzMeException('cannot find suitable client! install hippo viewer or secondlife client and try again')

    logging.debug('RezzMe.launchers.linux2: found client %s', client)

    if 'hippo' in client:
        hippoGridInfo = None
        hippoUserSettings = os.path.expanduser('~/.hippo_opensim_viewer/user_settings')
        hippoGridInfoXml = os.path.expanduser('~/.hippo_opensim_viewer/user_settings/grid_info.xml') 

        # hippo 0.21 doesn't honor -loginuri :-( so, we need to write the gridinfo.xml file
        if not os.path.exists(hippoUserSettings):
            logging.info('RezzMe.launchers.linux2: hippo: creating hippo setting directory %s', hippoUserSettings)
            os.makedirs(hippoUserSettings)

        if os.path.exists(hippoGridInfoXml):
            logging.debug('RezzMe.launchers.linux2: hippo: found %s', hippoGridInfoXml)
            with open(hippoGridInfoXml, 'r') as xml:
                hippoGridInfo = ET.parse(xml)
        else:
            logging.debug('RezzMe.launchers.linux2: hippo: hippo grid info not found at %s, creating it', hippoGridInfoXml)
            hippoGridInfo = ET.fromstring('<llsd><array></array></llsd>')
            
        # check whether we are already in hippo's grid info
        gridnick = None

        grid = hippoGridInfo.xpath('/llsd/array/map/string[string() = "%s"]' % gridInfo['login'])
        if grid and grid[0].text == gridInfo['login']:
            # LLSD "XML" sucks big time: it depends on the ordering of elements to work...
            gridnick = grid[0].getparent().xpath('./key[string() = "gridnick"]')[0].getnext().text
            logging.debug('RezzMe.launchers.linux2: hippo:  found gridnick %s for loginuri %s', 
                          gridnick, gridInfo['login'])
        else:
            logging.debug('RezzMe.launchers.linux2: hippo:  no existing gridnick for loginuri %s', gridInfo['login'])
            gridXml = '<map>'
            for (key, value) in {'gridname' : 'gridname', 
                                 'gridnick' : 'gridnick', 
                                 'economy'  : 'helperuri', 
                                 'welcome'  : 'loginpage', 
                                 'login'    : 'loginuri', 
                                 'platform' : 'platform', 
                                 'about'    : 'website'}.iteritems():
                if key in gridInfo: 
                    gridXml += '<key>%s</key><string>%s</string>' % (value, gridInfo[key])
                else:
                    gridXml += '<key>%s</key><string/>' % value
            gridXml += '</map>'
            grid = ET.fromstring(gridXml)
            logging.debug('RezzMe.launchers.linux2: hippo: : adding XML sniplet %s to grid_info.xml', 
                          ET.tostring(grid, pretty_print = True))

            # write out grid_info.xml again
            hippoGridInfo.xpath('/llsd/array')[0].append(grid)
            logging.debug('RezzMe.launchers.linux2: hippo: grid_info.xml: %s', 
                          ET.tostring(hippoGridInfo))

            if os.path.exists(hippoGridInfoXml):
                bak = '%s.bak' % hippoGridInfoXml
                logging.debug('RezzMe.launchers.linux2: hippo: "%s" exists, baking up to "%s"', 
                              hippoGridInfoXml, bak)
                if os.path.exists(bak): os.unlink(bak)
                os.rename(hippoGridInfoXml, bak)
            hippoGridInfo.write(hippoGridInfoXml)
            logging.info('RezzMe.launchers.linux2: hippo: updated grid_info.xml')

            gridnick = gridInfo['gridnick']
        
        clientArgs += ['-grid', gridnick]

    # all systems go: start client
    clientArgs = [ client ] + clientArgs
    logging.debug('RezzMe.launchers.linux2: client %s args %s', client, ' '.join(clientArgs))
    os.execvp(client, clientArgs)


