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

import urllib
import urllib2
import xml.etree.ElementTree as ET

import RezzMe.uri

fakeGridInfo = {
    'rezzmes://lindenlab.com/': {
        'login': 'https://login.agni.lindenlab.com/cgi-bin/login.cgi',
        'gridname': 'LindenLab SecondLife(tm) main grid',
        'gridnick': 'secondlife'
        },
    'rezzmes://aditi.lindenlab.com/': {
        'login': 'https://login.aditi.lindenlab.com/cgi-bin/login.cgi',
        'gridname': 'LindenLab SecondLife(tm) BETA grid',
        'gridnick': 'secondlife-beta'
        }
    }


def GetGridInfo(uri):
    '''Invoke /get_grid_info on target grid and obtain additional parameters
       '''

    # short circuit for "fake" uris
    if uri.PlainUri in fakeGridInfo: return fakeGridInfo[uri.PlainUri]

    # construct GridInfo URL
    infoUri = '%s/get_grid_info' % (uri.BaseHttpUri)

    # try to retrieve GridInfo 
    gridInfo = {}
    try:
        gridInfoXml = ET.parse(urllib2.urlopen(infoUri))
        for e in gridInfoXml.findall('/*'):
            if e.text: gridInfo[e.tag] = e.text

    except urllib2.URLError:
        print 'oops, failed to retrieve grid info, proceeding with guestimates...'

    gridKeys = gridInfo.keys()
    if not 'login' in gridKeys: gridInfo['login'] = '%s/' % uri.BaseHttpUri
    if not 'gridname' in gridKeys: gridInfo['gridname'] = '-'
    if not 'gridnick' in gridKeys: gridInfo['gridnick'] = 'grid'

    # construct the grid key: login server plus region only
    gridKey = gridInfo['login'].rstrip('/')
    if uri.Region:
        region = urllib.quote(uri.Region)
        gridKey = '%s/%s' % (gridKey, region)
    gridInfo['gridkey'] = urllib.quote(gridKey, '')

    return gridInfo
