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

# import logging
import types
import urllib

import RezzMe.parse
import RezzMe.exceptions

class Uri(object):
    '''The RezzMe.uri.Uri object encapsulates virtual world resource identifiers.

       A virtual world is identified by the hosting server, an
       optional user/avatar name and password, an optional region name
       with optional X/Y/Z coordinates. In addition RezzMe.uri.Uri
       objects can also contain a tag (short label of the target
       grid), a display tag (for use in menus), and the identifier of
       the virtual world client to use.
       '''
    
    def __init__(self, uri = None, display = None, client = None, userId = None):
        '''The Uri class encapsulates a RezzMe virtual world resource identifier.

           To use RezzMe.Uri you need to import it

               >>> import RezzMe.uri

           A Uri object can be instantiated in several ways:

           - from a string:

               >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/')
               >>> uri.PlainUri
               'rezzme://opensim.foobar.com/'

             note, that if the URI contains spaces, that they will be converted to '%20':

               >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/an island')
               >>> uri.PlainUri
               'rezzme://opensim.foobar.com/an%20island'
             

           - from a dictionary as generated by RezzMe.parse.ParseUriAndPath():

               >>> import RezzMe.parse
               >>> import RezzMe.uri
               >>> uriDict = RezzMe.parse.ParseUriAndPath('rezzme://opensim.foobar.com:9000/island')
               >>> uri = RezzMe.uri.Uri(uriDict)
               >>> uri.PlainUri
               'rezzme://opensim.foobar.com:9000/island'

           - from another Uri object (cloning it):

               >>> aUri = RezzMe.uri.Uri('rezzme://dr%20who@opensim.foobar.com/region/1/2/3')
               >>> anotherUri = RezzMe.uri.Uri(aUri)
               >>> anotherUri.Avatar
               'dr who'
               >>> anotherUri.Avatar = 'mr torchwood'
               >>> anotherUri.FullUri
               'rezzme://mr%20torchwood@opensim.foobar.com/region/1/2/3'
               >>> aUri.FullUri
               'rezzme://dr%20who@opensim.foobar.com/region/1/2/3'

              here we cloned anotherUri from aUri. aUri had as avatar 'dr who',
              which anotherUri inherits (we are cloning aUri). we then change
              the avatar value of anotherUri to 'mr torchwood' and retrieve the
              FullUri property from both objects: aUri still has 'dr who' as avatar,
              anotherUri has 'mr torchwood'.


           Additional instantiation parameters are the tag, display,
           client, and userId meta data parameters. The tag parameter
           is short label of the target grid. The display parameter is
           is used to display a Uri in GUI menus. The client parameter
           is used to associate a particular virtual world client with
           the URI object. The userId parameter finally can associate
           a default userId with the Uri object.

           Uri objects can also come as auto-login Uri: if avatar name
           and password are contained in the Uri *and* the query part
           of Uri contains 'auto' as parameter:

           >>> autoUri = RezzMe.uri.Uri('rezzme://dr%20who:SECRET@opensim.foobar.com/region/1/2/3?auto')
               >>> autoUri.AutoLogin
               True

           '''
        
        if uri is None: 
            raise RezzMe.exceptions.RezzMeException('empty uri parameter')

        self.__plain = None
        self.__http = None
        self.__safe = None
        self.__auto = False

        self.Extensions = {}

        if isinstance(uri, str) or isinstance(uri, unicode):
            uri = uri.replace(' ', '%20')
            self.__dict = {}
            self.__orig = uri
            self._parse(uri)

        elif type(uri) is types.DictType:
            self.__dict = uri
            self._sync()
            self.__orig = self.FullUri

        elif isinstance(uri, RezzMe.uri.Uri):
            self.__dict = uri.__dict
            self._sync()
            self.__orig = uri.FullUri
            self.Extensions = uri.Extensions
            return

        else:
            raise RezzMe.exceptions.RezzMeException('unexpected uri type %s' % type(uri))

        self.Display = display
        self.Client = client
        self.UserId = userId


#         for k in self.__dict:
#             logging.debug('uri.Uri: %s -> %s', k, self.__dict[k])

    def _sync(self):
        self.__plain = '%s://' % self.Scheme
        self.__full  = self.__plain
        self.__safe  = self.__plain

        if self.Scheme == 'rezzme':
            self.__http = 'http://'
        else:
            self.__http = 'https://'
        
        if 'avatar' in self.__dict: 
            avatar = urllib.quote(self.__dict['avatar'])
            self.__full += avatar
            self.__safe += avatar
            if 'password' in self.__dict: 
                self.__full += ':%s' % self.__dict['password']
            self.__full += '@'
            self.__safe += '@'
        
        self.__plain += self.__dict['host']
        self.__http  += self.__dict['host']
        self.__safe  += self.__dict['host']
        self.__full  += self.__dict['host']

        if 'port' in self.__dict:
            port = ':%s' % self.__dict['port']
            self.__plain += port
            self.__http  += port
            self.__safe  += port
            self.__full  += port

        self.__plain += '/'
        self.__safe  += '/'
        self.__full  += '/'

        self.__base  = self.__plain

        if 'region' in self.__dict:
            self.__plain += self.__dict['region']
            self.__safe  += self.__dict['region']
            self.__full  += self.__dict['region']

            if 'x' in self.__dict and 'y' in self.__dict and 'z' in self.__dict:
                xyz = '/%s' % '/'.join(map(lambda x: str(x), self.XYZ))
                self.__safe  += xyz
                self.__full  += xyz

        if 'query' in self.__dict:
            q = self.__dict['query'].split('&')
            self.__auto = 'auto' in q

    def _parse(self, uri):
        self.__dict = RezzMe.parse.ParseUriAndPath(uri)

        if not self.__dict:
            raise RezzMe.exceptions.RezzMeException('wonky URI >%s<' % uri)

        if not self.Scheme: return None
        self._sync()

    def _plain(self):
        return self.__plain
    PlainUri = property(fget = _plain,
                        doc = '''plain URI without avatar name, avatar password and region X/Y/Z (read-only)

                                     >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.zurich.ibm.com:9000/island/127/127/24')
                                     >>> uri.PlainUri
                                     'rezzme://opensim.zurich.ibm.com:9000/island'

                                 This is a read-only property, writing to it will result in an exception:

                                     >>> uri.PlainUri = 'rezzme://opensim.zurich.ibm.com:9000/island'
                                     Traceback (most recent call last):
                                     ...
                                     AttributeError: can't set attribute
                                 
                                 ''') #'

    def _base(self):
        return self.__base
    BaseUri = property(fget = _base,
                       doc = '''base URI without avatar name, avatar password and region (read-only)

                                    >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.zurich.ibm.com:9000/island/127/127/24?query')
                                    >>> uri.BaseUri
                                    'rezzme://opensim.zurich.ibm.com:9000/'

                                 This is a read-only property, writing to it will result in an exception:

                                     >>> uri.BaseUri = 'rezzme://opensim.zurich.ibm.com:9000/'
                                     Traceback (most recent call last):
                                     ...
                                     AttributeError: can't set attribute
                                 
                                ''') #'

    def _safe(self):
        return self.__safe
    SafeUri = property(fget = _safe,
                       doc = '''URI without password (read-only)

                                    >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24?query')
                                    >>> uri.FullUri
                                    'rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24'
                                    >>> uri.SafeUri
                                    'rezzme://dr%20scofield@opensim.zurich.ibm.com:9000/island/127/127/24'

                                 This is a read-only property, writing to it will result in an exception:

                                     >>> uri.SafeUri = 'rezzme://dr%20scofield@opensim.zurich.ibm.com:9000/island/127/127/24'
                                     Traceback (most recent call last):
                                     ...
                                     AttributeError: can't set attribute
                                 
                                ''') #'
    
    def _full(self):
        return self.__full
    FullUri = property(fget = _full,
                       doc = '''full URI including avatar name and password if available (read-only)

                                    >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24?query')
                                    >>> uri.FullUri
                                    'rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24'
                                
                                 This is a read-only property, writing to it will result in an exception:

                                     >>> uri.FullUri = 'rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24'
                                     Traceback (most recent call last):
                                     ...
                                     AttributeError: can't set attribute
                                 
                                ''') #'

    def _http(self):
        return self.__http
    BaseHttpUri = property(fget = _http,
                           doc = '''base HTTP URI of the server (without trailing "/") (read-only)

                                        >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24?query')
                                        >>> uri.BaseHttpUri
                                        'http://opensim.zurich.ibm.com:9000'

                                 This is a read-only property, writing to it will result in an exception:

                                     >>> uri.BaseHttpUri = 'http://opensim.zurich.ibm.com:9000'
                                     Traceback (most recent call last):
                                     ...
                                     AttributeError: can't set attribute
                                 
                                    ''') #'

    def _keyValue(self, key):
        if type(key) is types.StringType:
            if key in self.__dict: return self.__dict[key]
        elif type(key) is types.ListType:
            return [self.__dict[x] if x in self.__dict else None for x in key]
        return None

    def _credentials(self):
        return self._keyValue(['avatar', 'password'])
    def _scredentials(self, value):
        if value[0] is None and 'avatar' in self.__dict:
            del self.__dict['avatar']
        else:
            if len(value[0].split()) != 2:
                raise RezzMe.exceptions.RezzMeException('avatar name format violation, must be "First Last", found "%s"' % value[0])
            self.__dict['avatar'] = value[0]

        if value[1] is None and 'password' in self.__dict:
            del self.__dict['password']
        else:
            self.__dict['password'] = value[1]

        self._sync()
    Credentials = property(fget = _credentials, fset = _scredentials,
                           doc = '''tuple containing (avatar name, password) (read-write)
                                    
                                        >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield:secret@opensim.zurich.ibm.com:9000/island/127/127/24?query')
                                        >>> uri.Credentials
                                        ['dr scofield', 'secret']

                                    This is a read-write property:

                                        >>> uri.Credentials = ['dr who', 'anothersecret']
                                        >>> uri.Credentials
                                        ['dr who', 'anothersecret']


                                    Note, that, as with RezzMe.parse, the avatar name has to follow
                                    the format "First Last"; this will fail:

                                        >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/island')
                                        >>> uri.Credentials = ['drwho', 'secret']
                                        Traceback (most recent call last):
                                        ...
                                        RezzMeException: avatar name format violation, must be "First Last", found "drwho"

                                    ''')

    def _avatar(self):
        return self._keyValue('avatar')
    def _savatar(self, value):
        if value is None and 'avatar' in self.__dict:
            del self.__dict['avatar'] 
        else:
            if len(value.split()) != 2:
                raise RezzMe.exceptions.RezzMeException('avatar name format violation, must be "First Last", found "%s"' % value)
            self.__dict['avatar'] = value
        self._sync()
    Avatar = property(fget = _avatar, fset = _savatar,
                      doc = '''avatar name (read-write)

                                   >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island')
                                   >>> uri.Avatar
                                   'dr scofield'

                               As this is a read-write property you can set the avatar name as well:

                                   >>> uri.Avatar = 'dr who'
                                   >>> uri.Avatar
                                   'dr who'

                               Again, the avatar name has to follow the "First Last" pattern, this will fail:

                                   >>> uri.Avatar = 'drwho'
                                   Traceback (most recent call last):
                                   ...
                                   RezzMeException: avatar name format violation, must be "First Last", found "drwho"

                               ''')

    def _client(self):
        return self._keyValue('client')
    def _sclient(self, value):
        if value is None and 'client' in self.__dict:
            del self.__dict['client'] 
        else:
            self.__dict['client'] = value
    Client = property(fget = _client, fset = _sclient,
                      doc = '''client to use (read-write)

                               >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island')
                               >>> uri.Client
                               >>> uri.Client = '/opt/SL/secondlife/secondlife-1.22.11.113941/secondlife'
                               >>> uri.Client
                               '/opt/SL/secondlife/secondlife-1.22.11.113941/secondlife'

                               ''')

    def _password(self):
        return self._keyValue('password')
    def _spassword(self, value):
        if value is None and 'password' in self.__dict:
            del self.__dict['password']
        else:
            self.__dict['password'] = value

        self._sync()
    Password = property(fget = _password, fset = _spassword,
                        doc = '''avatar password (read-write)

                                     >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island')
                                     >>> uri.Credentials
                                     ['dr scofield', None]
                                     >>> uri.Password
                                     >>> uri.Password = 'secret'
                                     >>> uri.Password
                                     'secret'

                                 Setting the password has an effect on Credentials and on FullUri:

                                     >>> uri.Credentials
                                     ['dr scofield', 'secret']
                                     >>> uri.FullUri
                                     'rezzme://dr%20scofield:secret@opensim.foobar.com/island'
    
                                 ''')

    def _fullyQualified(self):
        return all((self.Avatar, self.Password))
    FullyQualified =property(fget = _fullyQualified,
                             doc = '''True if this uri object contains both avatar name and password

                                          >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield:SECRET@opensim.foobar.com/island')
                                          >>> uri.FullyQualified
                                          True

                                      but:
                                      
                                          >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island')
                                          >>> uri.FullyQualified
                                          False
                                          
                                      ''')

    def _autoLogin(self):
        return self.__auto and self.FullyQualified
    AutoLogin = property(fget = _autoLogin,
                         doc = '''True if this uri object is a auto-login Uri.

                                      >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield:SECRET@opensim.foobar.com/island?auto')
                                      >>> uri.AutoLogin
                                      True

                                   but:
                                      >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island?auto')
                                      >>> uri.AutoLogin
                                      False
                                   ''')
        
    def _userId(self):
        return self._keyValue('userID')
    def _suserId(self, value):
        if value is None and 'userID' in self.__dict:
            del self.__dict['userID']
        else:
            self.__dict['userID'] = value
    UserId = property(fget = _userId, fset = _suserId,
                      doc = '''user ID in case of authenticated grid (read-write)

                                   >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island')
                                   >>> uri.UserId
                                   >>> uri.UserId = 'drscofield@xyzzyxyzzy.net'
                                   >>> uri.UserId
                                   'drscofield@xyzzyxyzzy.net'
    
                               UserId is a pure meta property in that it has no effect on other properties such as FullUri:
                               
                                   >>> uri.FullUri
                                   'rezzme://dr%20scofield@opensim.foobar.com/island'
    

                               ''')

    def _display(self):
        display = self._keyValue('display')
        if not display: 

            display = ''
            if self.Avatar: 
                display += '%s@' % self.Avatar
            if self.Port:
                display += 'rezzme://%s:%s' % (self.Host, self.Port)
            else:
                display += 'rezzme://%s' % self.Host
            if self.Path:
                display += '/%s' % self.Path
            self.Display = display
        return display
    def _sdisplay(self, value):
        if value is None and 'display' in self.__dict:
            del self.__dict['display']
        else:
            self.__dict['display'] = value
        self._sync()
    Display = property(fget = _display, fset = _sdisplay,
                       doc = '''string that can be used in menus and so forth (read-write)

                                Unless explicitly set, the Display property will return a default value
                                constructed from other properties of the Uri object:

                                    >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foobar.com/island')
                                    >>> uri.Display
                                    'dr scofield@rezzme://opensim.foobar.com/island'

                                Once set, Display will return that value instead:

                                    >>> uri.Display = 'foobar island'
                                    >>> uri.Display
                                    'foobar island'

                                Even if we change another property that the default value of Display would use,
                                we still get the explicitly-set value:

                                    >>> uri.Avatar = 'dr who'
                                    >>> uri.Display
                                    'foobar island'

                                ''')

    def _scheme(self):
        return self._keyValue('scheme')
    Scheme = property(fget = _scheme,
                      doc = '''URI scheme (read-only)

                               Usually returns "rezzme":

                                   >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com:9000/island/1/2/3')
                                   >>> uri.Scheme
                                   'rezzme'
    
                               or "rezzmes":

                                   >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com:9000/island/1/2/3')
                                   >>> uri.Scheme
                                   'rezzmes'

                               Note, that this is a read-only property, setting it will raise an exception:
                               >>> uri.Scheme = 'http'
                               Traceback (most recent call last):
                               ...
                               AttributeError: can't set attribute

                               ''') #'

    def _port(self):
        return self._keyValue('port')
    Port = property(fget = _port,
                    doc = '''URI port (if specified) (read-only)

                             Example with port provided:

                                 >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com:9000/island/1/2/3?query')
                                 >>> uri.Port
                                 '9000'
    
                             Example without port:

                                 >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com/island/1/2/3?query')
                                 >>> uri.Port

                             Note, that Port is a read-only property; setting it will raise an exception:

                                 >>> uri.Port = 4000
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute

                          ''') #'

    def _host(self):
        return self._keyValue('host')
    Host = property(fget = _host,
                    doc = '''URI host (read-only)

                             Sample code:

                             >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com/island/1/2/3?query')
                             >>> uri.Host
                             'opensim.foobar.com'

                             Note, that Host is a read-only property; setting it will raise an exception:

                                 >>> uri.Host = 'opensim.foo.bar.com'
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute

                             ''') #'

    def _region(self):
        return self._keyValue('region')
    Region = property(fget = _region,
                      doc = '''URI region (if specified) (read-only)

                             Sample code:

                             >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com/island/1/2/3?query')
                             >>> uri.Region
                             'island'

                             Note, that Region is a read-only property; setting it will raise an exception:

                                 >>> uri.Host = 'wonderland'
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute
                      
                             ''') #'

    def _decodedRegion(self):
        return urllib.unquote(self._keyValue('region'))
    DecodedRegion = property(fget = _decodedRegion,
                      doc = '''Decoded URI region (if specified) (read-only)

                             Sample code:

                                 >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com/island/1/2/3?query')
                                 >>> uri.DecodedRegion
                                 'island'

                             but:

                                 >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com/treasure%20island/1/2/3?query')
                                 >>> uri.DecodedRegion
                                 'treasure island'

                             Note, that Region is a read-only property; setting it will raise an exception:

                                 >>> uri.Host = 'wonderland'
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute
                      
                             ''') #'

    def _xyz(self):
        return self._keyValue(['x', 'y', 'z'])
    XYZ = property(fget = _xyz,
                   doc = '''tuple containing (X, Y, Z) coordinates (if specified) (read-only)

                             Sample code:

                             >>> uri = RezzMe.uri.Uri('rezzmes://opensim.foobar.com/island/1/2/3?query')
                             >>> uri.XYZ
                             [1, 2, 3]

                             Note, that XYZ is a read-only property; setting it will raise an exception:

                                 >>> uri.XYZ = [4, 5, 6]
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute

                            ''') #'

    def _location(self):
        if self.Region and all(self.XYZ):
            return 'secondlife://%s/%s' % (self.Region, '/'.join([str(x) for x in self.XYZ])) # map(lambda x: str(x), self.XYZ)))
        elif self.Region:
            return 'secondlife://%s' % self.Region
        else:
            return None
    Location = property(fget = _location,
                        doc = '''location with in the target grid as a secondlife:// URI (read-only)

                                Sample code:
                                
                                    >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/island/1/2/3')
                                    >>> uri.Location
                                    'secondlife://island/1/2/3'

                                or:

                                    >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/wonder%20land/1/2/3')
                                    >>> uri.Location
                                    'secondlife://wonder%20land/1/2/3'

                                Note, that without a region we will get a None as return value:

                                    >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/')
                                    >>> uri.Location
    
                                Finally, Location is a read-only property; setting it will raise an exception:

                                    >>> uri.Location = 'secondlife://myland/1/2/3'
                                    Traceback (most recent call last):
                                    ...
                                    AttributeError: can't set attribute

                                 ''') #'

    def _path(self):
        return self._keyValue('path')
    Path = property(fget = _path,
                    doc = '''URI region(X/Y/Z)? component (if available) (read-only)

                             Sample code:

                                 >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
                                 >>> uri.Path
                                 'myland/127/128/33'
           
                             but also:

                                 >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/')
                                 >>> uri.Path

                             Note, Path is a read-only property; setting it will raise an exception:

                                 >>> uri.Path = 'yourland/127/126/32'
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute

                             ''') #'

    def _query(self):
        return self._keyValue('query')
    Query = property(fget = _query,
                    doc = '''URI query component (if available)

                             Sample code:

                                 >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33?query&p0=a&p1=b')
                                 >>> uri.Query
                                 'query&p0=a&p1=b'

                             but also:

                                 >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
                                 >>> uri.Query

                             Note, Query is a read-only property; setting it will raise an exception:

                                 >>> uri.Query = 'query&p0=x&p1=y'
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute

                             ''') #'

    def _dict(self):
        return self.__dict
    Dict = property(fget = _dict,
                    doc = '''returns dictionary with all recognized components (read-only)

                             Sample code:

                                 >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
                                 >>> uri.Dict
                                 {'z': 33, 'plain': 'rezzme://opensim.foobar.com', 'region': 'myland', 'userID': None, 'slurl': 'secondlife:///myland/127/128/33', 'host': 'opensim.foobar.com', 'client': None, 'x': 127, 'y': 128, 'path': 'myland/127/128/33', 'scheme': 'rezzme', 'display': None}
    
                                 Note, Dict is a read-only property; setting it will raise an exception:
                                 >>> uri.Dict = {'z': 33, 'plain': 'rezzme://opensim.foobar.com', 'region': 'myland', 'userID': None, 'slurl': 'secondlife:///myland/127/128/33', 'host': 'opensim.foobar.com', 'client': None, 'x': 127, 'y': 128, 'path': 'yourland', 'scheme': 'rezzme', 'display': None}
                                 Traceback (most recent call last):
                                 ...
                                 AttributeError: can't set attribute
    
                             ''') #'


    def __cmp__(self, other):
        '''Override the comparison method and compare on FullUri:

           Sample code:
           
               >>> uri0 = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
               >>> uri1 = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
               >>> uri0 == uri1
               True

           and:

               >>> uri0 = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
               >>> uri1 = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/3')
               >>> uri0 == uri1
               False
    
           As this will only compare on FullUri, meta properties will not be taken into
           account:

               >>> uri0 = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
               >>> uri1 = RezzMe.uri.Uri('rezzme://opensim.foobar.com/myland/127/128/33')
               >>> uri0 == uri1
               True

           '''
        return cmp(self.FullUri, other.FullUri)

    def __hash__(self):
        '''Override the hash method to use __hash__ of FullUri instead.

           >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/')
           >>> uri.__hash__()
           -968694205
           '''
        return self.FullUri.__hash__()

    def __str__(self):
        '''Override the str representation method and return all relevant properties.

           Sample code:
           
               >>> uri = RezzMe.uri.Uri('rezzme://opensim.foobar.com/')
               >>> str(uri)
               'rezzme://opensim.foobar.com/ client: None/userId: None/display: rezzme://opensim.foobar.com'

           Adding meta property values:

               >>> uri.Client = '/path/to/client'
               >>> str(uri)
               'rezzme://opensim.foobar.com/ client: /path/to/client/userId: None/display: rezzme://opensim.foobar.com'
               >>> uri.UserId = 'drscofield@foobar.com'
               >>> str(uri)
               'rezzme://opensim.foobar.com/ client: /path/to/client/userId: drscofield@foobar.com/display: rezzme://opensim.foobar.com'
    
           '''
        return '%s client: %s/userId: %s/display: %s' % (self.FullUri, self.Client, self.UserId, self.Display)
