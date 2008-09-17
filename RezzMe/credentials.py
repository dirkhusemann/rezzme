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

import os
import RezzMe.exceptions
import RezzMe.parse
import RezzMe.uri
import urllib

class Credentials(object):
    '''Deal with user IDs for authenticated grids.
       '''

    def __init__(self, path = None):
        '''instantiate a Credentials object.
           '''

        self._path = path
        self._credentials = {}
        self.__load()

    def __delete__(self):
        self.Save()
        self._credentials = None

    def __load(self):
        if not self._path: return
        if not os.path.exists(self._path): return
        
        try:
            creds = open(self._path, 'r')
            for cred in creds:
                if not ' ' in cred: continue

                (uri, userID) = cred.split(None, 1)
                self._credentials[uri] = userID.rstrip()

            creds.close()

        except IOError:
            print 'failed to load credentials from "%s"' % self._path


    def Credential(self, uri):
        if uri.BaseUri in self._credentials:
            return self._credentials[uri.BaseUri]
        else:
            return None

    def Add(self, uri, userID):
        self._credentials[uri.BaseUri] = userID

    def Save(self):
        if not self._path: return

        try:
            if os.path.exists(self._path):
                bak = '%s.bak' % self._path
                if os.path.exists(bak): os.unlink(bak)
                os.rename(self._path, bak)
            creds = open(self._path, 'w')
            for cred in self._credentials:
                creds.write('%s %s\n' % (cred, self._credentials[cred]))
            creds.close()

        except IOError:
            print 'failed to save credentials to "%s"' % self._path
