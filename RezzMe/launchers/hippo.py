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

import codecs
import logging
import os
import xml.etree.ElementTree

def LLSD2Dict(element):
    d = {}
    key = None
    for e in element:
        if e.tag == 'key':
            key = e.text
            continue
        elif e.tag == 'string' and key is not None:
            d[key] = e.text
            key = None
        else:
            logging.warning('launchers.hippo.LLSD2Dict: unexpected tag/value %s/%s' % (e.tag, e.text))
    return d

def HippoGridInfoFix(gridInfo, userGridXml, defaultGridXml):
    hippoGridInfo = None

    # check whether userGridXml exists, if not create the containing
    # directory if necessary and copy in defaultGridXml
    if not os.path.exists(userGridXml):
        logging.info('launchers.hippo: user grid_info.xml does not exist at "%s"', userGridXml)
        # does the containing directory exist?
        if not os.path.exists(os.path.dirname(userGridXml)):
            logging.info('launchers.hippo: creating hippo setting directory %s', os.path.dirname(userGridXml))
            os.makedirs(os.path.dirname(userGridXml))

        # do we even have defaultGridXml
        if not os.path.exists(defaultGridXml):
            logging.warning('launchers.hippo: incomplete hippo installation: missing %s', defaultGridXml)
        else:
            # yes, copy it over to userGridXml
            with codecs.open(defaultGridXml, 'r', 'utf8') as defaultXml:
                with codecs.open(userGridXml, 'w', 'utf8') as userXml:
                    userXml.write(defaultXml.read())
            logging.info('launchers.hippo: copied %s to %s', defaultGridXml, userGridXml)

    if os.path.exists(userGridXml):
        logging.debug('launchers.hippo: found %s', userGridXml)
        with codecs.open(userGridXml, 'r', 'utf8') as xmlGridInfo:
            hippoGridInfo = xml.etree.ElementTree.parse(xmlGridInfo).getroot()
    else:
        logging.debug('launchers.hippo: hippo grid info not found at %s, creating it', userGridXml)
        hippoGridInfo = xml.etree.ElementTree.fromstring('<llsd><array></array></llsd>')
            
    # check whether we are already in hippo's grid info
    # note: LLSD "XML" sucks big time: it depends on the ordering of elements to work...
    for gmap in hippoGridInfo.findall('./array/map'):
        grid = LLSD2Dict(gmap)
        if 'loginuri' in grid and grid['loginuri'] == gridInfo['login']:
            logging.debug('launchers.hippo:  found gridnick %s for loginuri %s', 
                          grid['gridnick'], gridInfo['login'])
            return grid['gridnick']

    # no, we are not in hippo's grid info: need add ourselves then
    logging.debug('launchers.hippo:  no existing gridnick for loginuri %s', gridInfo['login'])
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
    grid = xml.etree.ElementTree.fromstring(gridXml)
    logging.debug('launchers.hippo: : adding XML sniplet %s to grid_info.xml', xml.etree.ElementTree.tostring(grid))

    # write out grid_info.xml again
    hippoGridInfo.find('./array').append(grid)
    logging.debug('launchers.hippo: grid_info.xml: %s', xml.etree.ElementTree.tostring(hippoGridInfo))

    if os.path.exists(userGridXml):
        bak = '%s.bak' % userGridXml
        logging.debug('launchers.hippo: "%s" exists, baking up to "%s"', userGridXml, bak)
        if os.path.exists(bak): os.unlink(bak)
        os.rename(userGridXml, bak)
    with codecs.open(userGridXml, 'w', 'utf8') as xml:
        xml.write(xml.etree.ElementTree.tostring(hippoGridInfo))
    logging.info('launchers.hippo: updated grid_info.xml')

    return gridInfo['gridnick']

