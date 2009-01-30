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
import optparse
import re
import sys
import urllib

def ParseOptions():
    '''Parse the command line options and setup options.
       '''

    parser = optparse.OptionParser()
    parser.add_option('-l', '--longhelp', action='store_true', dest = 'longhelp', help = 'longhelp')
    (options, args) = parser.parse_args()

    if options.longhelp:
        parser.print_help()
        sys.exit(0)

    return options


#
# regex: parse a URI
#
reURI = re.compile(r'''^(?P<scheme>[a-zA-Z0-9]+)://                         # scheme
                        ((?P<avatar>[^:@]+)(:(?P<password>[^@]+))?@)?       # avatar name and password (optional)
                        (?P<host>[^:/]+)(:(?P<port>\d+))?                   # host, port (optional)
                        (?P<path>/.*)                                       # path
                       $''', re.IGNORECASE | re.VERBOSE)

def ParseUri(uri):
    '''Parse a URI and return its constituent parts.
       '''

    uri = uri.lstrip().rstrip()
    match = reURI.match(uri)
    if not match or not match.group('scheme') or not match.group('host'):
        logging.warning('RezzMe.parser.ParseUri: wonky URI: %s --- skipping it', uri)
        return (None, None, None, None, None, None)

    scheme = match.group('scheme')
    host = match.group('host')
    port = match.group('port')
    avatar = match.group('avatar')
    password = match.group('password')
    path = match.group('path')

    if avatar: avatar = urllib.unquote(avatar)

    return (scheme, host, port, avatar, password, path)


# 
# regex: parse path as location 
#
reLOCXYZ = re.compile(r'''^/(?P<region>[^/]+)/          # region name
                            (?P<x>\d+)/                 # X position
                            (?P<y>\d+)/                 # Y position
                            (?P<z>\d+)                  # Z position
                    ''', re.IGNORECASE | re.VERBOSE)
reLOC = re.compile(r'''^/(?P<region>.+)/?$  # region name
                    ''', re.IGNORECASE | re.VERBOSE)

def ParsePath(path):
    '''Try and parse path as /region/X/Y/Z.
       '''

    loc = None
    region = None
    x = 0
    y = 0
    z = 0

    try:
        matchXYZ = reLOCXYZ.match(path)
        match = reLOC.match(path)
    except:
        logging.error('RezzMe.parser.ParsePath: stumbled badly over %s', path)
        raise
    
    if matchXYZ:
        region = matchXYZ.group('region')
        x = int(matchXYZ.group('x'))
        y = int(matchXYZ.group('y'))
        z = int(matchXYZ.group('z'))

        loc = 'secondlife:///%s/%d/%d/%d' % (region, x, y, z)

    elif match:
        region = match.group('region')
        loc = 'secondlife:///%s' % region

    return (loc, region, x, y, z)

def ParseUriAndPath(uri):
    (scheme, host, port, avatar, password, path) = ParseUri(uri)

    if not scheme:
        return {}

    (slurl,region, x, y, z) = (None, None, None, None, None)
    if path:
        (slurl,region, x, y, z) = ParsePath(path)

    p = {}
    for key in ['scheme', 'host', 'port', 'avatar', 'password', 
                'path', 'slurl', 'region', 'x', 'y', 'z']:
        if eval(key): p[key] = eval(key)

    if port:
        p['plain'] = '%s://%s:%s' % (scheme, host, port)
    else:
        p['plain'] = '%s://%s' % (scheme, host)

    return p
