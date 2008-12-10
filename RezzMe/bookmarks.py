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
import RezzMe.config.parser
import RezzMe.exceptions
import RezzMe.parse
import RezzMe.uri
import urllib

defaults = { 
    'rezzmes://login.agni.lindenlab.com/cgi-bin/login.cgi': 'SecondLife main grid',
    'rezzme://login.aditi.lindenlab.com/cgi-bin/login.cgi': 'SecondLife BETA grid',
    'rezzme://www.osgrid.org:8002/': 'OSgrid'}

class Bookmarks(object):
    '''Deal with rezzme:// bookmarks.
       '''

    def __init__(self, path = None):
        '''instantiate a Bookmarks object.

           loads bookmarks from ~/.rezzme.bookmarks

           path: if not None, path to bookmarks file
           '''

        self._bookmarks = []

        self._path = None
        if not path:
            return
        
        self._path = os.path.expanduser(path)
        logging.debug('RezzMe.bookmarks.Bookmarks: instantiating object: path %s', self._path)
        self._load()

        
    def __delete__(self):
        '''destructor.

           saves bookmarks to ~/.rezzme.bookmarks
           '''
        if self._path:
            self.Save()
        self._bookmarks = None
        
    def _load(self):
        if not self._path: 
            logging.debug('RezzMe.bookmarks.Bookmarks._load: path is empty')
            return

        if not os.path.exists(self._path): 
            logging.debug('RezzMe.bookmarks.Bookmarks._load: file "%s" does not exist', self._path)
            return
        
        try:
            bookmarks = RezzMe.config.parser.Parser(self._path)
            logging.debug('RezzMe.bookmarks.Bookmarks._load: sections %s', '|'.join(bookmarks.sections()))
            for bookmark in bookmarks.sections():
                tag = bookmarks.get(bookmark, 'tag')
                client = bookmarks.get(bookmark, 'client')
                display = bookmarks.get(bookmark, 'display')
                uri = RezzMe.uri.Uri(uri = bookmark, tag = tag, display = display, client = client)

                self.Add(uri)

                logging.debug('RezzMe.bookmarks.Bookmarks._load: adding uri %s', uri.SafeUri)

        except IOError:
            print 'failed to load bookmarks from "%s"' % self._path


    def Reload(self):
        logging.debug('RezzMe.bookmarks.Bookmarks.Reloading: reloading bookmarks')
        self._bookmarks = []
        self._load()

    def Save(self):
        if not self._path: 
            logging.debug('RezzMe.bookmarks.Bookmarks.Save: path is empty')
            return

        try:
            bookmarks = RezzMe.config.parser.Parser(self._path)
            for bookmark in self._bookmarks:
                bookmarks.add_section(bookmark.FullUri)
                if bookmark.Client:
                    bookmarks.set(bookmark.FullUri, 'client', bookmark.Client)
                if bookmark.Tag:
                    bookmarks.set(bookmark.FullUri, 'tag', bookmark.Tag)
                if bookmark.Display:
                    bookmarks.set(bookmark.FullUri, 'display', bookmark.Display)
            bookmarks.save()

        except IOError, e:
            logging.error('RezzMe.bookmarks.Bookmarks.Save: failed to save bookmarks: %s', e, exc_info = True)


    def Delete(self, bookmark):
        logging.debug('RezzMe.bookmarks.Bookmarks.Delete: uri %s', bookmark.SafeUri)
        if bookmark in self._bookmarks: 
            logging.debug('RezzMe.bookmarks.Bookmarks.Delete: deleting uri %s', bookmark.SafeUri)
            del self._bookmarks[self._bookmarks.index(bookmark)]

    def Change(self, old, new):
        logging.debug('RezzMe.bookmarks.Bookmarks.Change: old uri %s -> new uri %s', old.SafeUri, new.SafeUri)
        self.Delete(old)
        self.Add(new)

    def Add(self, bookmark):
        logging.debug('RezzMe.bookmarks.Bookmarks.Add: new uri %s', bookmark.SafeUri)
        if bookmark in self._bookmarks:
            logging.debug('RezzMe.bookmarks.Bookmarks.Add: new uri %s already exists, deleting it', bookmark.SafeUri)
            del self._bookmarks[self._bookmarks.index(bookmark)]
        self._bookmarks += [bookmark]

    def Bookmark(self, uri = None, display = None):
        if uri: 
            if not isinstance(uri, RezzMe.uri.Uri):
                uri = RezzMe.uri.Uri(uri)
            logging.debug('RezzMe.bookmarks.Bookmarks.Bookmark: uri %s', uri.SafeUri)

            best = None
            for bookmark in self._bookmarks:
                if bookmark.BaseUri.startswith(uri.BaseUri):
                    if all(bookmark.Credentials): return bookmark
                    if bookmark.Avatar: best = bookmark
                    if not best: best = bookmark
            logging.debug('RezzMe.bookmarks.Bookmarks.Bookmark: best match %s', best)
            return best

        elif display:
            logging.debug('RezzMe.bookmarks.Bookmarks.Bookmark: display %s', display)
            for bookmark in self._bookmarks:
                if display == bookmark.Display: 
                    logging.debug('RezzMe.bookmarks.Bookmarks.Bookmark: %s matches %s', display, bookmark.SafeUri)
                    return bookmark

        return None

    def _displays(self):
        return map(lambda x: x.Display, self._bookmarks)
    Displays = property(fget = _displays)

    def _bookmarks(self):
        return self._bookmarks
    Bookmarks = property(fget = _bookmarks)

