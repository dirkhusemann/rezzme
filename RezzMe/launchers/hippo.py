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

def HippoGridInfoFix(gridInfo):
    parser = ET.XMLParser(remove_blank_text = True)

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
            hippoGridInfo = ET.parse(xml, parser)
    else:
        logging.debug('RezzMe.launchers.linux2: hippo: hippo grid info not found at %s, creating it', hippoGridInfoXml)
        hippoGridInfo = ET.fromstring('<llsd><array></array></llsd>', parser)
            
    # check whether we are already in hippo's grid info
    gridnick = None

    grid = hippoGridInfo.xpath('/llsd/array/map/string[string() = "%s"]' % gridInfo['login'])
    if grid and grid[0].text == gridInfo['login']:
        # LLSD "XML" sucks big time: it depends on the ordering of elements to work...
        gridnick = grid[0].getparent().xpath('./key[string() = "gridnick"]')[0].getnext().text
        logging.debug('RezzMe.launchers.linux2: hippo:  found gridnick %s for loginuri %s', 
                      gridnick, gridInfo['login'])
        return gridnick

    # no, we are not in hippo's grid info: need add ourselves then
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
    grid = ET.fromstring(gridXml, parser)
    logging.debug('RezzMe.launchers.linux2: hippo: : adding XML sniplet %s to grid_info.xml', 
                  ET.tostring(grid, pretty_print = True))

    # write out grid_info.xml again
    hippoGridInfo.xpath('/llsd/array')[0].append(grid)
    logging.debug('RezzMe.launchers.linux2: hippo: grid_info.xml: %s', 
                  ET.tostring(hippoGridInfo, pretty_print = True))

    if os.path.exists(hippoGridInfoXml):
        bak = '%s.bak' % hippoGridInfoXml
        logging.debug('RezzMe.launchers.linux2: hippo: "%s" exists, baking up to "%s"', 
                      hippoGridInfoXml, bak)
        if os.path.exists(bak): os.unlink(bak)
        os.rename(hippoGridInfoXml, bak)
    with open(hippoGridInfoXml, 'w') as xml:
        xml.write(ET.tostring(hippoGridInfo, pretty_print = True))
    logging.info('RezzMe.launchers.linux2: hippo: updated grid_info.xml')

    return gridInfo['gridnick']

