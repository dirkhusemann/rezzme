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
        logging.debug('RezzMe.credentials.Credentials: instantiating object, path %s', path)
        self._path = path
        self._credentials = {}
        self.__load()

    def __delete__(self):
        self.Save()
        self._credentials = None

    def __load(self):
        if not self._path: 
            logging.debug('RezzMe.credentials.Credentials.__load: empty path %s', self._path)
            return

        if not os.path.exists(self._path): 
            logging.debug('RezzMe.credentials.Credentials.__load: path "%s" does not exist', self._path)
            return
        
        try:
            creds = open(self._path, 'r')
            for cred in creds:
                if not ' ' in cred: continue

                (uri, userID) = cred.split(None, 1)
                userID = userID.rstrip()
                self._credentials[uri] = userID
                logging.debug('RezzMe.credentials.Credentials.__load: found userID %s for uri %s', userID, uri)

            creds.close()

        except IOError, e:
            logging.debug('RezzMe.credentials.Credentials.__load: failed to load credentials from "%s": %s', self._path, e)


    def Credential(self, uri):
        if uri.BaseUri in self._credentials:
            logging.debug('RezzMe.credentials.Credentials.Credential: found credential for uri %s', uri)
            return self._credentials[uri.BaseUri]
        else:
            logging.debug('RezzMe.credentials.Credentials.Credential: found no credential for uri %s', uri)
            return None

    def Add(self, uri, userID):
        logging.debug('RezzMe.credentials.Credentials.Add: adding userID %s for uri %s', userID, uri)
        self._credentials[uri.BaseUri] = userID

    def Save(self):
        if not self._path: 
            logging.debug('RezzMe.credentials.Credentials.Save: path "%s" empty', self._path)
            return

        try:
            if os.path.exists(self._path):
                bak = '%s.bak' % self._path
                if os.path.exists(bak): os.unlink(bak)
                os.rename(self._path, bak)
                logging.debug('RezzMe.credentials.Credentials.Save: path "%s" exist, backing up to "%s"', self._path, bak)
            creds = open(self._path, 'w')
            for cred in self._credentials:
                creds.write('%s %s\n' % (cred, self._credentials[cred]))
            creds.close()

        except IOError, e:
            logging.error('RezzMe.credentials.Credentials.Save: failed to save credentials to "%s": %s', 
                          self._path, e, exc_info = True)

