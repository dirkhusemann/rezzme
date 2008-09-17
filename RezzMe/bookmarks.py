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

defaults = { 
    'rezzmes://login.agni.lindenlab.com/cgi-bin/login.cgi': 'SecondLife main grid',
    'rezzmes://login.aditi.lindenlab.com/cgi-bin/login.cgi': 'SecondLife BETA grid',
    'rezzmes://www.osgrid.org:8002/': 'OSgrid'}

class Bookmarks(object):
    '''Deal with rezzme:// bookmarks.
       '''

    def __init__(self, path = None):
        '''instantiate a Bookmarks object.

           loads bookmarks from ~/.rezzme.bookmarks

           path: if not None, path to bookmarks file
           '''

        self._path = path
        self._bookmarks = []
        self._load()
        
    def __delete__(self):
        '''destructor.

           saves bookmarks to ~/.rezzme.bookmarks
           '''
        self.Save()
        self._bookmarks = None
        
    def _load(self):
        if not self._path: return
        if not os.path.exists(self._path): return
        
        try:
            bookmarks = open(self._path, 'r')
            for bookmarkline in bookmarks:
                if ' ' in bookmarkline:
                    (bookmark, tag) = bookmarkline.split(None, 1)
                    bookmark = bookmark.strip()
                    tag = tag.strip()
                else:
                    bookmark = bookmarkline.strip()
                    bookmark = bookmark.strip()
                    tag = None
                
                self.Add(RezzMe.uri.Uri(uri = bookmark, tag = tag))

            bookmarks.close()

        except IOError:
            print 'failed to load bookmarks from "%s"' % self._path


    def Reload(self):
        self._bookmarks = []
        self._load()

    def Save(self):
        if not self._path: return

        try:
            if os.path.exists(self._path):
                bak = '%s.bak' % self._path
                if os.path.exists(bak): os.unlink(bak)
                os.rename(self._path, bak)
            bookmarks = open(self._path, 'w')
            for bookmark in self._bookmarks:
                bookmarks.write('%s\n' % bookmark.BookmarkAndTag)
            bookmarks.close()
        except IOError:
            print 'failed to save bookmarks to "%s"' % self._path


    def Delete(self, bookmark):
        if bookmark in self._bookmarks: 
            del self._bookmarks[self._bookmarks.index(bookmark)]

    def Change(self, old, new):
        self.Delete(old)
        self.Add(new)

    def Add(self, bookmark):
        if bookmark in self._bookmarks:
            del self._bookmarks[self._bookmarks.index(bookmark)]
        self._bookmarks += [bookmark]

    def Bookmark(self, uri = None, display = None):
        if uri: 
            if not isinstance(uri, RezzMe.uri.Uri):
                uri = RezzMe.uri.Uri(uri)

            best = None
            for bookmark in self._bookmarks:
                if bookmark.BaseUri.startswith(uri.BaseUri):
                    if all(bookmark.Credentials): return bookmark
                    if bookmark.Avatar: best = bookmark
                    if not best: best = bookmark
            return best

        elif display:
            for bookmark in self._bookmarks:
                if display == bookmark.Display: return bookmark

        return None

    def _displays(self):
        return map(lambda x: x.Display, self._bookmarks)
    Displays = property(fget = _displays)

    def _bookmarks(self):
        return self._bookmarks
    Bookmarks = property(fget = _bookmarks)
