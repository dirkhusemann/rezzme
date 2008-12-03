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
import sys
import types
import types
import urllib

import RezzMe.parse
import RezzMe.exceptions

class Uri(object):
    
    def __init__(self, uri = None, tag = None, display = None):
        
        if uri is None: 
            raise RezzMe.exceptions.RezzMeException('empty uri parameter')

        self._plain = None
        self._http = None
        self._safe = None
        self._display = None
        self._tag = None

        if isinstance(uri, str) or isinstance(uri, unicode):
            self._dict = {}
            self._orig = uri
            self._parse(uri)
        elif type(uri) is types.DictType:
            self._dict = dict
            self._sync()
            self._orig = self.FullUri
        elif isinstance(uri, RezzMe.uri.Uri):
            self._dict = uri._dict
            self._sync()
            self._orig = uri.FullUri
        else:
            raise RezzMe.exceptions.RezzMeException('unexpected uri type %s' % type(uri))


        self._tag = tag
        self._display = display

        for k in self._dict:
            logging.debug('RezzMe.uri.Uri: %s -> %s', k, self._dict[k])

    def _sync(self):
        self._plain = '%s://' % self.Scheme
        self._full  = self._plain
        self._safe  = self._plain

        if self.Scheme == 'rezzme':
            self._http = 'http://'
        else:
            self._http = 'https://'
        
        if 'avatar' in self._dict: 
            avatar = urllib.quote(self._dict['avatar'])
            self._full += avatar
            self._safe += avatar
            if 'password' in self._dict: 
                self._full += ':%s' % self._dict['password']
            self._full += '@'
            self._safe += '@'
        
        self._plain += self._dict['host']
        self._http  += self._dict['host']
        self._safe  += self._dict['host']
        self._full  += self._dict['host']

        if 'port' in self._dict:
            port = ':%s' % self._dict['port']
            self._plain += port
            self._http  += port
            self._safe  += port
            self._full  += port

        self._plain += '/'
        self._safe  += '/'
        self._full  += '/'

        self._base  = self._plain

        if 'region' in self._dict:
            self._plain += self._dict['region']
            self._safe  += self._dict['region']
            self._full  += self._dict['region']

            if 'x' in self._dict and 'y' in self._dict and 'z' in self._dict:
                xyz = '/%s' % '/'.join(map(lambda x: str(x), self.XYZ))
                self._safe  += xyz
                self._full  += xyz

    def _parse(self, uri):
        self._dict = RezzMe.parse.ParseUriAndPath(uri)

        if not self.Scheme: return None
        self._sync()

    def _plain(self):
        return self._plain
    PlainUri = property(fget = _plain, doc = 'plain URI without avatar name, avatar password and region X/Y/Z')

    def _base(self):
        return self._base
    BaseUri = property(fget = _base, doc = 'base URI without avatar name, avatar password and region')

    def _safe(self):
        return self._safe
    SafeUri = property(fget = _safe, doc = 'URI without password')
    
    def _full(self):
        return self._full
    FullUri = property(fget = _full, doc = 'full URI including avatar name and password if available')

    def _http(self):
        return self._http
    BaseHttpUri = property(fget = _http, doc = 'base HTTP URI of the server (without trailing "/")')

    def _keyValue(self, key):
        if type(key) is types.StringType:
            if key in self._dict: return self._dict[key]
        elif type(key) is types.ListType:
            if not all(map(lambda x: x in self._dict, key)): 
                return map(lambda k: None, key)
            return map(lambda x: self._dict[x], key)
        return None

    def _credentials(self):
        return self._keyValue(['avatar', 'password'])
    def _scredentials(self, value):
        if value[0] is None:
            del self._dict['avatar']
        else:
            self._dict['avatar'] = value[0]

        if value[1] is None:
            del self._dict['password']
        else:
            self._dict['password'] = value[1]

        self._sync()
    Credentials = property(fget = _credentials, fset = _scredentials, doc = 'tuple containing (avatar name, password)')

    def _avatar(self):
        return self._keyValue('avatar')
    def _savatar(self, value):
        if value is None:
            del self._dict['avatar'] 
        else:
            self._dict['avatar'] = value

        self._sync()
    Avatar = property(fget = _avatar, fset = _savatar, doc = 'avatar name')

    def _password(self):
        return self._keyValue('password')
    def _spassword(self, value):
        if value is None:
            del self._dict['password']
        else:
            self._dict['password'] = value

        self._sync()
    Password = property(fget = _password, fset = _spassword, doc = 'password')

    def _tag(self):
        return self._tag
    def _stag(self, value):
        self._tag = value
    Tag = property(fget = _tag, fset = _stag, doc ='short descriptive label of the target grid')

    def _display(self):
        if not self._display: 

            self._display = ''
            if self.Avatar: 
                self._display += '%s@' % self.Avatar
            if self.Tag: 
                self._display += '%s, ' % self.Tag
            if self.Port:
                self._display += 'rezzme://%s:%s' % (self.Host, self.Port)
            else:
                self._display += 'rezzme://%s' % self.Host
            if self.Path:
                self._display += '%s' % self.Path

        return self._display
    def _sdisplay(self, value):
        self._display = value
        self._sync()
    Display = property(fget = _display, fset = _sdisplay, doc = 'string that can be used in menus and so forth')

    def _scheme(self):
        return self._keyValue('scheme')
    Scheme = property(fget = _scheme, doc = 'URI scheme')

    def _port(self):
        return self._keyValue('port')
    Port = property(fget = _port, doc = 'URI port (if specified)')

    def _host(self):
        return self._keyValue('host')
    Host = property(fget = _host, doc = 'URI host')

    def _region(self):
        return self._keyValue('region')
    Region = property(fget = _region, doc = 'URI region (if specified)')

    def _xyz(self):
        return self._keyValue(['x', 'y', 'z'])
    XYZ = property(fget = _xyz, doc = 'tuple containing (X, Y, Z) coordinates (if specified)')

    def _location(self):
        if self.Region and all(self.XYZ):
            return 'secondlife://%s/%s' % (self.Region, '/'.join(map(lambda x: str(x), self.XYZ)))
        elif self.Region:
            return 'secondlife://%s/' % self.Region
    Location = property(fget = _location, doc = 'location with in the target grid as a secondlife:// slurl')

    def _path(self):
        return self._keyValue('path')
    Path = property(fget = _path, doc = 'URI path component (if available)')
    
    def _bookmarkAndTag(self):
        if self._tag is not None:
            return '%s %s' % (self.FullUri, self.Tag)
        else:
            return self.FullUri
    BookmarkAndTag = property(fget = _bookmarkAndTag)

    def _dict(self):
        return self._dict
    Dict = property(fget = _dict)


    def __cmp__(self, other):
        return cmp(self.FullUri, other.FullUri)

    def __hash__(self):
        return self.FullUri.__hash__()

    def __str__(self): 
        return self.FullUri
