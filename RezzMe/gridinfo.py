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
import urllib
import urllib2
import xml.etree.ElementTree

fakeGridInfo = {
    'rezzme://lindenlab.com/': {
        'login': 'https://login.agni.lindenlab.com/cgi-bin/login.cgi',
        'gridname': 'LindenLab SecondLife(tm) main grid',
        'gridnick': 'secondlife',
        'platform': 'secondlife'},
    'rezzme://aditi.lindenlab.com/': {
        'login': 'https://login.aditi.lindenlab.com/cgi-bin/login.cgi',
        'gridname': 'LindenLab SecondLife(tm) BETA grid',
        'gridnick': 'secondlife-beta',
        'platform': 'secondlife'},
    }


def GetGridInfo(uri):
    '''Invoke /get_grid_info on target grid and obtain additional parameters
       '''

    logging.debug('gridinfo.GetGridInfo: retrieving grid info from uri %s', uri)
    logging.debug('gridinfo.GetGridInfo: base URI %s', uri.BaseUri)

    # short circuit for "fake" uris
    if uri.BaseUri in fakeGridInfo: 
        logging.debug('gridinfo.GetGridInfo: returning fake grid info for uri %s', uri)
        gridInfo = fakeGridInfo[uri.BaseUri]
        gridInfo['faked'] = True
        gridInfo['error'] = None
        return fakeGridInfo[uri.BaseUri]

    # construct GridInfo URL
    infoUri = '%s/get_grid_info' % (uri.BaseHttpUri)

    # try to retrieve GridInfo 
    gridInfo = {}
    # default platform: opensim
    gridInfo['platform'] = 'opensim'
    gridInfo['error'] = None

    try:
        req = urllib2.Request(url = infoUri)
        req.add_header('X-OpenSim-Host', uri.Host)
        if uri.Region: req.add_header('X-OpenSim-Region', uri.DecodedRegion)
        logging.debug('gridinfo.GetGridInfo: req %s headers[%s]', req.get_full_url(),
                      ' '.join(['%s: %s' % (x, req.headers[x]) for x in req.headers]))

        gridInfoXml = xml.etree.ElementTree.parse(urllib2.urlopen(req))
        for e in gridInfoXml.findall('/*'):
            if e.text: gridInfo[e.tag] = e.text
            logging.debug('gridinfo.GetGridInfo: %s = %s', e.tag, e.text)

    except urllib2.URLError, ue:
        logging.error('gridinfo.GetGridInfo: oops, failed to retrieve grid info: %s', ue)
        # we can get any number of URLErrors here, unfortunately they
        # are not uniform, hence i need to test for attribs
        if getattr(ue, 'reason', None):
            gridInfo['error'] = str(ue.reason)
        elif getattr(ue, 'code', None):
            # the server/proxy can send back a 404 if the region does not exist
            if ue.code == 404:
                gridInfo['error'] = 'region not found (%s)' % ue.msg
            else:
                gridInfo['error'] = 'server returned a "%s"' % str(ue.code)
        else:
            gridInfo['error'] = 'connection failed (network problem)'
    except Exception, ex:
            gridInfo['error'] = 'connection failed (general problem: %s)' % str(ex)

    gridKeys = gridInfo.keys()
    if not 'login' in gridKeys: 
        gridInfo['login'] = '%s/' % uri.BaseHttpUri
        logging.info('gridinfo.GetGridInfo: curing missing "login" key with %s', gridInfo['login'])
    if not 'gridname' in gridKeys: 
        gridInfo['gridname'] = '-'
        logging.info('gridinfo.GetGridInfo: curing missing "gridname" key with %s', gridInfo['gridname'])
    if not 'gridnick' in gridKeys: 
        gridInfo['gridnick'] = 'grid'
        logging.info('gridinfo.GetGridInfo: curing missing "gridnick" key with %s', gridInfo['gridnick'])

    if not 'regioninfoavailable' in gridKeys:
        gridInfo['regioninfoavailable'] = False
    else:
        gridInfo['regioninfoavailable'] = (gridInfo['regioninfoavailable'].lower() == 'true')

    # construct the grid key: login server plus region only
    gridKey = gridInfo['login'].rstrip('/')
    if uri.Region:
        region = urllib.quote(uri.Region)
        gridKey = '%s/%s' % (gridKey, region)
    gridInfo['gridkey'] = urllib.quote(gridKey, '')

    return gridInfo
