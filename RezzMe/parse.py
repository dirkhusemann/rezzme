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
import re
import urllib

import RezzMe.exceptions

#
# regex: parse a URI
#
reURI = re.compile(r'''^(?P<scheme>[a-zA-Z0-9]+)://                        # scheme
                        ((?P<avatar>[^:@]+)(:(?P<password>[^ @]+))?@)?     # avatar name and password (optional)
                        (?P<host>[^@:/]+)(:(?P<port>\d+))?                 # host, port (optional)
                        (?:/(?P<path>[^\?$]*))?                            # path
                        (?:\?(?P<query>.*))?                               # query
                       $''', re.IGNORECASE | re.VERBOSE)

def ParseUri(uri):
    '''Parse a URI string and return its constituent parts.

       To use RezzMe.parse.ParseUri() you need to import RezzMe.parse:

           >>> import RezzMe.parse
    
       ParseUri() takes a URI string in various formats:

       - a simple rezzme URI:

           >>> # Uri with trailing '/'...
           >>> RezzMe.parse.ParseUri('rezzme://opensim.foobar.com/')
           ('rezzme', 'opensim.foobar.com', None, None, None, '', None)
           >>>
           >>> # ...and without:
           >>> RezzMe.parse.ParseUri('rezzme://opensim.foobar.com')
           ('rezzme', 'opensim.foobar.com', None, None, None, None, None)
    

       - a rezzme URI including port:

           >>> # Uri with trailing '/'...
           >>> RezzMe.parse.ParseUri('rezzme://opensim.foobar.com:9000/')
           ('rezzme', 'opensim.foobar.com', '9000', None, None, '', None)
           >>>
           >>> # ...and without:
           >>> RezzMe.parse.ParseUri('rezzme://opensim.foobar.com:9000')
           ('rezzme', 'opensim.foobar.com', '9000', None, None, None, None)
    

       - a rezzme URI including an avatar name and optionally a password:

           >>> # Uri with just avatar name:
           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield@opensim.foobar.com:9000/')
           ('rezzme', 'opensim.foobar.com', '9000', 'dr scofield', None, '', None)
           >>>
           >>> # Uri with avatar name and password
           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/')
           ('rezzme', 'opensim.foobar.com', '9000', 'dr scofield', 'secret', '', None)
    

       - a rezzme URI with a path component:

           >>> RezzMe.parse.ParseUri('rezzme://opensim.foobar.com:9000/island')
           ('rezzme', 'opensim.foobar.com', '9000', None, None, 'island', None)

       - a rezzme URI with a path component and an query string:

           >>> RezzMe.parse.ParseUri('rezzme://opensim.foobar.com:9000/island?query=blub&a=wuff')
           ('rezzme', 'opensim.foobar.com', '9000', None, None, 'island', 'query=blub&a=wuff')
    

       - rezzme URIs containing all of the above:

           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield@opensim.foobar.com:9000/island')
           ('rezzme', 'opensim.foobar.com', '9000', 'dr scofield', None, 'island', None)
           >>>
           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island')
           ('rezzme', 'opensim.foobar.com', '9000', 'dr scofield', 'secret', 'island', None)
           >>>
           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island/1/2/3')
           ('rezzme', 'opensim.foobar.com', '9000', 'dr scofield', 'secret', 'island/1/2/3', None)
           >>>
           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island/1/2/3?query=a&wuff=b')
           ('rezzme', 'opensim.foobar.com', '9000', 'dr scofield', 'secret', 'island/1/2/3', 'query=a&wuff=b')
    

       in each case the extracted results are returned as a list:
       
           >>> res = RezzMe.parse.ParseUri('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island/1/2/3?query=a&wuff=b')
           >>> # print contents of list:
           >>> print "scheme: %s" % res[0]
           scheme: rezzme
           >>> print "host: %s" % res[1]
           host: opensim.foobar.com
           >>> print "port: %s" % res[2]
           port: 9000
           >>> print "avatar: %s" % res[3]
           avatar: dr scofield
           >>> print "password: %s" % res[4]
           password: secret
           >>> print "path: %s" % res[5]
           path: island/1/2/3
           >>> print "query: %s" % res[6]
           query: query=a&wuff=b

       Note also, that the avatar name must not contain a space (' ')
       but has to contain an encoded space ('%20'):

       - this will fail (' ' instead of '%20'):

           >>> RezzMe.parse.ParseUri('rezzme://dr scofield@opensim.zurich.ibm.com/')
           Traceback (most recent call last):
           ...
           RezzMeException: avatar name format violation, must be "First%20Last" or "First+Last", found "dr scofield"

       - this will fail as well (no '%20'):

           >>> RezzMe.parse.ParseUri('rezzme://drscofield@opensim.zurich.ibm.com/')
           Traceback (most recent call last):
           ...
           RezzMeException: avatar name format violation, must be "First%20Last" or "First+Last", found "drscofield"

        - this, however, will work:

           >>> RezzMe.parse.ParseUri('rezzme://dr%20scofield@opensim.zurich.ibm.com/')
           ('rezzme', 'opensim.zurich.ibm.com', None, 'dr scofield', None, '', None)


        - this, will work as well:

           >>> RezzMe.parse.ParseUri('rezzme://dr+scofield@opensim.zurich.ibm.com/')
           ('rezzme', 'opensim.zurich.ibm.com', None, 'dr scofield', None, '', None)

       '''

    uri = uri.lstrip().rstrip()
    match = reURI.match(uri)
    if not match or not match.group('scheme') or not match.group('host'):
        logging.warning('parser.ParseUri: wonky URI: %s --- skipping it', uri)
        return (None, None, None, None, None, None, None)

    scheme = match.group('scheme')
    host = match.group('host')
    port = match.group('port')
    avatar = match.group('avatar')
    password = match.group('password')
    path = match.group('path')
    query = match.group('query')

    if avatar:
        if avatar.find('%20') > 0:
            avatar = urllib.unquote(avatar)
        elif avatar.find('+') > 0:
            avatar = avatar.replace('+', ' ')
        else:
            raise RezzMe.exceptions.RezzMeException('avatar name format violation, must be "First%%20Last" or "First+Last", found "%s"' % avatar)

    return (scheme, host, port, avatar, password, path, query)


# 
# regex: parse path as location 
#
reLOCXYZ = re.compile(r'''^/?(?P<region>[^/]+)/          # region name
                            (?P<x>\d+)/                 # X position
                            (?P<y>\d+)/                 # Y position
                            (?P<z>\d+)                  # Z position
                            $''', re.IGNORECASE | re.VERBOSE)
reLOC = re.compile(r'''^/?(?P<region>[^/]+)/?$  # region name
                       $''', re.IGNORECASE | re.VERBOSE)

def ParsePath(path):
    '''Try and parse path as /region/X/Y/Z.

       To use RezzMe.parse.ParsePath() you need to import RezzMe.parse:

           >>> import RezzMe.parse
     
       ParsePath() takes a string that either contains just a region
       name or consists of region name and X/Y/Z coordinates:

           >>> RezzMe.parse.ParsePath('island')
           ('secondlife:///island', 'island', 0, 0, 0)
           
       Note, that for historical reasons ParsePath() also accepts a
       leading'/' but strips it out:

           >>> RezzMe.parse.ParsePath('/island')
           ('secondlife:///island', 'island', 0, 0, 0)
           
       Here is an example of a path with X/Y/Z coordinates:

           >>> RezzMe.parse.ParsePath('island/127/127/24')
           ('secondlife:///island/127/127/24', 'island', 127, 127, 24)
    
       ParsePath() returns a "None" list when it cannot parse the path
       value; for example, when the region name contains'/' or
       if you supply more than 3 coordinate values (or less than 3):

           >>> RezzMe.parse.ParsePath('island/127/127/24/2')
           (None, None, 0, 0, 0)
           >>> RezzMe.parse.ParsePath('island/wuff')
           (None, None, 0, 0, 0)
    
       If ParsePath() can parse the path argument it will return a
       list containing the secondlife:/// URI, the region name, and
       the X, Y, and Z coordinates:

           >>> RezzMe.parse.ParsePath('treasure%20island/127/127/24')
           ('secondlife:///treasure%20island/127/127/24', 'treasure%20island', 127, 127, 24)
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
        logging.error('parser.ParsePath: stumbled badly over %s', path)
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
    '''Try and parse the URI string as a rezzme URI and return region
       and query values.

       To use RezzMe.parse.ParsePath() you need to import RezzMe.parse:

           >>> import RezzMe.parse
    
       ParseUriAndPath() combines ParseUri() and ParsePath() into one
       function. In contrast to both it does not return a list but
       instead returns a dictionary object:

           >>> RezzMe.parse.ParseUriAndPath('rezzme://opensim.zurich.ibm')
           {'plain': 'rezzme://opensim.zurich.ibm', 'host': 'opensim.zurich.ibm', 'scheme': 'rezzme'}
           >>> RezzMe.parse.ParseUriAndPath('rezzme://opensim.foobar.com:9000/test%20island')
           {'plain': 'rezzme://opensim.foobar.com:9000', 'region': 'test%20island', 'slurl': 'secondlife:///test%20island', 'host': 'opensim.foobar.com', 'path': 'test%20island', 'scheme': 'rezzme', 'port': '9000'}
    

       Note, that the dictionary will contain only those keys for which
       ParseUriAndPath() could find components in the URI string:

           >>> RezzMe.parse.ParseUriAndPath('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island/1/2/3?query=a&wuff=b')
           {'scheme': 'rezzme', 'plain': 'rezzme://opensim.foobar.com:9000', 'region': 'island', 'z': 3, 'slurl': 'secondlife:///island/1/2/3', 'host': 'opensim.foobar.com', 'query': 'query=a&wuff=b', 'avatar': 'dr scofield', 'x': 1, 'y': 2, 'path': 'island/1/2/3', 'password': 'secret', 'port': '9000'}
           
           >>> res = RezzMe.parse.ParseUriAndPath('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island/1/2/3?query=a&wuff=b')
           >>> res['x']
           1

       but

           >>> res = RezzMe.parse.ParseUriAndPath('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/island?query=a&wuff=b')
           >>> res['x']
           Traceback (most recent call last):
               ...
           KeyError: 'x'
    
       If you look at the results of ParseUriAndPath(), you will notice that
       it also returns 'slurl' and 'plain' key--value pairs:
       
           >>> res = RezzMe.parse.ParseUriAndPath('rezzme://dr%20scofield:secret@opensim.foobar.com:9000/test%20island')
           >>> print res['slurl']
           secondlife:///test%20island
           >>> print res['plain']
           rezzme://opensim.foobar.com:9000
    
       the 'slurl' key--value pair contains the 'secondlife:///' URI
       ready to use with the SecondLife client, the 'plain' key--value
       pair contains the original rezzme URI without the authentication information.

       Also, the 'avatar' key--value pair will have a ' ' substituted for the original '%20':

           >>> print res['avatar']
           dr scofield
       
       '''
    (scheme, host, port, avatar, password, path, query) = ParseUri(uri)

    if not scheme:
        return {}

    (slurl,region, x, y, z) = (None, None, None, None, None)
    if path:
        (slurl,region, x, y, z) = ParsePath(path)

    p = {}
    for key in ['scheme', 'host', 'port', 'avatar', 'password', 
                'path', 'slurl', 'region', 'x', 'y', 'z', 'query']:
        if eval(key): p[key] = eval(key)

    if port:
        p['plain'] = '%s://%s:%s' % (scheme, host, port)
    else:
        p['plain'] = '%s://%s' % (scheme, host)

    return p
