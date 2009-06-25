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
import RezzMe.utils

class Bookmarks(object):
    '''Deal with rezzme:// bookmarks.
       '''

    def __init__(self, path = None):
        '''instantiate a Bookmarks object.

           Loads bookmarks from bookmarks file "path"

           path: if not None, path to bookmarks file

           Sample code (no path specified, in-memory bookmarks object):

               >>> import RezzMe.bookmarks
               >>> b = RezzMe.bookmarks.Bookmarks()

           In-memory Bookmarks object is empty as we have not added
           any Uri objects to it, yet:
           
               >>> b.Bookmarks
               []

           This example instantiates a Bookmarks object with a file
           name (using a temporary file name here):

               >>> import os
               >>> import tempfile
               >>> import RezzMe.uri
               >>> import RezzMe.bookmarks
               >>> bf = tempfile.mktemp()
               >>> b = RezzMe.bookmarks.Bookmarks(bf)

           At this point in time the bookmarks file does not yet
           exist, as we have not yet added any Uri objects nor have we
           invoked the Save() method on our Bookmarks object:
           
               >>> os.path.exists(bf)
               False
               
               >>> b.Add(RezzMe.uri.Uri('rezzme://opensim.foobar.com:9000/my%20island'))
               >>> b.Save()

           Once we have added a Uri object and invoked Save() the file
           exists:
           
               >>> os.path.exists(bf)
               True

           We can now instantiate a new Bookmarks object from that saved file:

               >>> b = None
               >>> b = RezzMe.bookmarks.Bookmarks(bf)

           Listing the content shows us the Uri object we saved earlier:

               >>> [x.FullUri for x in b.Bookmarks]
               [u'rezzme://opensim.foobar.com:9000/my%20island']

           (cleanup)

               >>> if os.path.exists(bf): os.remove(bf)
    
           '''

        self._bookmarks = []

        self._path = None
        if not path:
            return
        
        self._path = RezzMe.utils.ExpandUser(path)
        logging.debug('bookmarks.Bookmarks: instantiating object: path %s', self._path)
        self._load()

    def __del__(self):
        '''(destructor)'''

        self._bookmarks = None
        

    def _load(self):
        '''(internal method'''

        if not self._path: 
            logging.debug('bookmarks.Bookmarks._load: path is empty')
            return

        if not os.path.exists(self._path): 
            logging.debug('bookmarks.Bookmarks._load: file "%s" does not exist', self._path)
            return
        
        try:
            bookmarks = RezzMe.config.parser.Parser(self._path)
            for bookmark in bookmarks.sections():
                client = bookmarks.get(bookmark, 'client')
                display = bookmarks.get(bookmark, 'display')
                userId = bookmarks.get(bookmark, 'userID')
                try:
                    uri = RezzMe.uri.Uri(uri = bookmark, display = display, client = client, userId = userId)
                except:
                    continue

                # collect extension value used by other apps
                for ext in bookmarks.options(bookmark):
                    if ext.startswith('x_'):
                        uri.Extensions[ext] = bookmarks.get(bookmark, ext)

                self.Add(uri)

                logging.debug('bookmarks.Bookmarks._load: adding uri %s', uri.SafeUri)

        except IOError:
            print 'failed to load bookmarks from "%s"' % self._path


    def Reload(self):
        '''Reload the bookmarks from the bookmarks file

           Useful if other applications are updating a bookmarks file
           concurrently.

           For example, let\'s instantiate our Bookmarks object using
           a temporary file as bookmarks file:

               >>> import os
               >>> import tempfile
               >>> import RezzMe.uri
               >>> import RezzMe.bookmarks
               >>> bf = tempfile.mktemp()
               >>> b = RezzMe.bookmarks.Bookmarks(bf)

           Next, add a Uri object to it:
           
               >>> b.Add(RezzMe.uri.Uri('rezzme://opensim.foobar.com:9000/'))
               >>> b.Save()

           Quickly display the current content:
           
               >>> [x.FullUri for x in b.Bookmarks]
               ['rezzme://opensim.foobar.com:9000/']

           Then, pretending to be another application sharing the
           bookmarks file, we add a bookmark entry "manually"...
           
               >>> f = open(bf, 'a')
               >>> f.write('[rezzme://opensim.barfoo.com:9000/]\\n')
               >>> f.write('display = bar foo island\\n')
               >>> f.close()

           ...and invoke Reload() on our Bookmarks object:
           
               >>> b.Reload()

           Checking the number of bookmarks in it reveals that we now
           have 2 Uri objects:
           
               >>> len(b.Bookmarks)
               2

           A sorted display of the content shows our manually added
           Uri to be the second one:
           
               >>> bm = [str(x) for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://opensim.barfoo.com:9000/ client: None/userId: None/display: bar foo island', 'rezzme://opensim.foobar.com:9000/ client: None/userId: None/display: rezzme://opensim.foobar.com:9000']

           (cleanup)

               >>> if os.path.exists(bf): os.remove(bf)

           '''

        logging.debug('bookmarks.Bookmarks.Reloading: reloading bookmarks')
        self._bookmarks = []
        self._load()

    def Save(self):
        '''save all bookmarks to the underlying file (if a path is set)

           Sample code: First we, again, setup our file-backed
           Bookmarks object:

               >>> import os
               >>> import tempfile
               >>> import RezzMe.bookmarks
               >>> import RezzMe.uri
               >>> bf = tempfile.mktemp()
               >>> b = RezzMe.bookmarks.Bookmarks(bf)

           Then we add a couple of Uri objects to it:
           
               >>> evil = RezzMe.uri.Uri('rezzme://wonkytonky.foo.com:666/evil%20island')
               >>> evil.Display = 'evil island'
               >>> evil.UserId = 'devil@hotplace.com'
               >>> evil.Client = '/bad/very/bad/client'
               >>> b.Add(evil)
               >>> good = RezzMe.uri.Uri('rezzme://heaven.bar.com:777/heavenly%20isles')
               >>> good.Display = 'heavenly isles'
               >>> good.UserId = 'angel@coolplace.com'
               >>> good.Client = '/opt/petrus/bin/angel'
               >>> b.Add(good)

           Finally we save it to file:
           
               >>> b.Save()

           A quick sorted dump of the content shows our two Uri
           objects:
           
               >>> bm = [str(x) for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://heaven.bar.com:777/heavenly%20isles client: /opt/petrus/bin/angel/userId: angel@coolplace.com/display: heavenly isles', 'rezzme://wonkytonky.foo.com:666/evil%20island client: /bad/very/bad/client/userId: devil@hotplace.com/display: evil island']

           Next, we try verify that we can instantiate a new Bookmarks
           object from our bookmarks file and that all URIs are still
           present and correct:

               >>> b = None
               >>> b = RezzMe.bookmarks.Bookmarks(bf)

           Now we should have a new Bookmarks object with 2 Uri
           objects in it:
           
               >>> len(b.Bookmarks)
               2

           We do. Let\'s check the content:
           
               >>> bm = [str(x) for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://heaven.bar.com:777/heavenly%20isles client: /opt/petrus/bin/angel/userId: angel@coolplace.com/display: heavenly isles', 'rezzme://wonkytonky.foo.com:666/evil%20island client: /bad/very/bad/client/userId: devil@hotplace.com/display: evil island']

           Looks identical to the previous dump.

           (cleanup)

               >>> if os.path.exists(bf): os.remove(bf)
           '''

        if not self._path: 
            logging.debug('bookmarks.Bookmarks.Save: path is empty')
            return

        try:
            bookmarks = RezzMe.config.parser.Parser()
            for uri in self._bookmarks:
                bookmarks.add_section(uri.FullUri)
                if uri.Client:
                    bookmarks.set(uri.FullUri, 'client', uri.Client)
                if uri.Display:
                    bookmarks.set(uri.FullUri, 'display', uri.Display)
                if uri.UserId:
                    bookmarks.set(uri.FullUri, 'userID', uri.UserId)

                # take care of potential extension values
                for ext in uri.Extensions:
                    bookmarks.set(uri.FullUri, ext, uri.Extensions[ext])
                    
            bookmarks.save(self._path)
            logging.debug('bookmarks.Save: saved bookmarks to %s', self._path)

        except IOError, e:
            logging.error('bookmarks.Bookmarks.Save: failed to save bookmarks: %s', e, exc_info = True)


    def Delete(self, uri, save = False):
        '''delete a bookmark from bookmarks.

           Example use: First, setup our sample Bookmarks object using
           a temporary file as bookmarks file:

               >>> import os
               >>> import tempfile
               >>> import RezzMe.bookmarks
               >>> import RezzMe.uri
               >>> bf = tempfile.mktemp()
               >>> b = RezzMe.bookmarks.Bookmarks(bf)
               >>> # populate Bookmarks object
               >>> uri0 = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.bar:9000/')
               >>> uri1 = RezzMe.uri.Uri('rezzme://dr%20who@opensim.foo.bar:9000/')
               >>> uri2 = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.bar:9000/an%20island')
               >>> uri3 = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.bar:9000/another%20island')
               >>> b.Add(uri0)
               >>> b.Add(uri1)
               >>> b.Add(uri2)
               >>> b.Add(uri3)

           Our Bookmarks object should now contain 4 Uri objects:

               >>> len(b.Bookmarks)
               4

           It does. Next, do a quick dump of the contents:

               >>> bm = [x.FullUri for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://dr%20scofield@opensim.foo.bar:9000/', 'rezzme://dr%20scofield@opensim.foo.bar:9000/an%20island', 'rezzme://dr%20scofield@opensim.foo.bar:9000/another%20island', 'rezzme://dr%20who@opensim.foo.bar:9000/']

           Now, delete the second Uri object that we added before:

               
               >>> b.Delete(RezzMe.uri.Uri('rezzme://dr%20who@opensim.foo.bar:9000/'))

           If all went according to plan we should now have 3 Uri
           objects left:
           
               >>> len(b.Bookmarks)
               3

           Yes, we do. Do a quick dump to visually verify that the
           correct Uri object was deleted:
           
               >>> bm = [x.FullUri for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://dr%20scofield@opensim.foo.bar:9000/', 'rezzme://dr%20scofield@opensim.foo.bar:9000/an%20island', 'rezzme://dr%20scofield@opensim.foo.bar:9000/another%20island']

           The'rezzme://dr%20who@opensim.foo.bar:9000/' Uri object is no longer
           in the Bookmarks collection, good.

           Let\'s delete another Uri:

               >>> b.Delete(RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.bar:9000/'))

           We should now be down to 2 Uri objects:
           
               >>> len(b.Bookmarks)
               2

           Another deletion should leave us with just 1 Uri object in
           our Bookmarks object:
           
               >>> b.Delete(RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.bar:9000/an%20island'))
               >>> len(b.Bookmarks)
               1

           Yes, just 1 left.

           Trying to delete a non-existing URI from bookmarks will
           just be ignored:

               Our bookmarks object currently only contains one Uri
               object:

                   >>> [x.FullUri for x in b.Bookmarks]
                   ['rezzme://dr%20scofield@opensim.foo.bar:9000/another%20island']

               Trying to delete the non-existent Uri 'rezzme://mary%20poppins@banks.london.uk:9000/'

                   >>> b.Delete(RezzMe.uri.Uri('rezzme://mary%20poppins@banks.london.uk:9000/'))

               results in an unchanged Bookmarks object:

                   >>> [x.FullUri for x in b.Bookmarks]
                   ['rezzme://dr%20scofield@opensim.foo.bar:9000/another%20island']
                   
           (cleanup)

               >>> if os.path.exists(bf): os.remove(bf)

           '''
        logging.debug('bookmarks.Bookmarks.Delete: uri %s', uri.SafeUri)
        # logging.debug('bookmarks.Bookmarks.Delete: uri %s', uri)
        bookmarks = []
        for b in self._bookmarks:
            if b.SafeUri != uri.SafeUri:
                bookmarks += [b]
            else:
                logging.debug('bookmarks.Bookmarks.Delete: found & deleting uri %s', uri.SafeUri)
        self._bookmarks = bookmarks

        if save:
            self.Save()
            
    def Change(self, old, new, save = False):
        '''change (replace) a Uri object with a new one

           Sample code: First setup our example in-memory Bookmarks
           object:

               >>> import RezzMe.uri
               >>> import RezzMe.bookmarks
               >>> b = RezzMe.bookmarks.Bookmarks()

           Then add our test Uri objects:

               >>> uri0 = RezzMe.uri.Uri('rezzme://dr%20who@opensim.foo.bar:9000/island')
               >>> uri1 = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.bar:9000/island')
               >>> b.Add(uri0)
               >>> b.Add(uri1)

           Do a quick dump to show the content before we replace one
           of the Uris:
           
               >>> bm = [x.FullUri for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://dr%20scofield@opensim.foo.bar:9000/island', 'rezzme://dr%20who@opensim.foo.bar:9000/island']

           Then create the new Uri object...

               >>> uri2 = RezzMe.uri.Uri('rezzme://dr%20who@opensim.foo.bar:9000/isle')

           ...and replace uri0 with it:

               >>> b.Change(uri0, uri2)

           We should now have 'rezzme://dr%20who@opensim.foo.bar:9000/isle'
           instead of'rezzme://dr%20who@opensim.foo.bar:9000/island' in our
           Bookmarks object:
           
               >>> bm = [x.FullUri for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['rezzme://dr%20scofield@opensim.foo.bar:9000/island', 'rezzme://dr%20who@opensim.foo.bar:9000/isle']

           We do.

           Another example, changing the Display property:

               >>> uri3 = RezzMe.uri.Uri('rezzme://opensim.bar.com:9000/paradise%20lost')
               >>> uri3.Display
               'rezzme://opensim.bar.com:9000/paradise%20lost'

           Adding that Uri object to our Bookmarks object...

               >>> b.Add(uri3)

           ...should then have uri3 show up in the contents of our
           Bookmarks object with the Display attribute having the
           default value (note that we are only showing the Display
           properties in the following dumps):
           
               >>> bm = [x.Display for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['dr scofield@rezzme://opensim.foo.bar:9000/island', 'dr who@rezzme://opensim.foo.bar:9000/isle', 'rezzme://opensim.bar.com:9000/paradise%20lost']

           which it does.

           Next, create another Uri object and set the Display
           attribute explicitly...
           
               >>> uri4 = RezzMe.uri.Uri(uri3)
               >>> uri4.Display = 'Paradise List'

           ...and replace uri3 with it:
           
               >>> b.Change(uri3, uri4)

           A dump of the contents of our Bookmarks object should now
           show that uri4 has replaced uri3:
           
               >>> bm = [x.Display for x in b.Bookmarks]
               >>> bm.sort()
               >>> bm
               ['Paradise List', 'dr scofield@rezzme://opensim.foo.bar:9000/island', 'dr who@rezzme://opensim.foo.bar:9000/isle']

           '''
        logging.debug('bookmarks.Bookmarks.Change: old uri %s -> new uri %s', old.SafeUri, new.SafeUri)
        self.Delete(old)
        self.Add(new)

        if save:
            self.Save()

    def Add(self, uri, save = False):
        '''add a Uri to bookmarks

           Sample code: First setup our in-memory Bookmarks object:

               >>> import RezzMe.uri
               >>> import RezzMe.bookmarks
               >>> b = RezzMe.bookmarks.Bookmarks()

           As it\'s newly instantiated it countains no Uri objects:

               >>> len(b.Bookmarks)
               0

           Next, let\'s add a new Uri object to it:
               >>> b.Add(RezzMe.uri.Uri('rezzme://opensim.wonky.org:19999/sandbay'))

           A dump of the contents shows that our Uri object got added:

               >>> [str(x) for x in b.Bookmarks] 
               ['rezzme://opensim.wonky.org:19999/sandbay client: None/userId: None/display: rezzme://opensim.wonky.org:19999/sandbay']

           Note, if the bookmark already exists it will just be replaced:

               Instantiate a new in-memory Bookmarks object:

                   >>> b = RezzMe.bookmarks.Bookmarks()

               Create a new Uri object, explicitly set its Display
               string and add it:
               
                   >>> uri0 = RezzMe.uri.Uri('rezzme://sim.salabim.org:4711/cave%20of%20aladin')
                   >>> uri0.Display = "Aladins Cave"
                   >>> b.Add(uri0)

               Dump the contents of the Bookmarks object:
               
                    >>> [str(x) for x in b.Bookmarks]
                    ['rezzme://sim.salabim.org:4711/cave%20of%20aladin client: None/userId: None/display: Aladins Cave']

               Next, clone Uri object uri0 as uri1 and change its
               Display string and add it as well:
               
                   >>> uri1 = RezzMe.uri.Uri(uri0)
                   >>> uri1.Display = "Aladin\'s Cave"
                   >>> b.Add(uri1)

               Now, display the contents of the Bookmarks object:

                   >>> [str(x) for x in b.Bookmarks]
                   ["rezzme://sim.salabim.org:4711/cave%20of%20aladin client: None/userId: None/display: Aladin\'s Cave"]

               uri0 has been replaced by uri1
    
           Similarly when using the UserId attribute:

               Instantiate a new in-memory Bookmarks object
               
                   >>> b = RezzMe.bookmarks.Bookmarks()

               Instantiate a new Uri object and add it to the
               Bookmarks object:
               
                   >>> uri0 = RezzMe.uri.Uri('rezzme://sim.salabim.org:4711/cave')
                   >>> b.Add(uri0)
    
               Show the contents of the Bookmarks object:
               
                   >>> [str(x) for x in b.Bookmarks]
                   ['rezzme://sim.salabim.org:4711/cave client: None/userId: None/display: rezzme://sim.salabim.org:4711/cave']

               Next, clone uri0 as uri1, add a UserId attribute to
               uri1, and add it:

                   >>> uri1 = RezzMe.uri.Uri(uri0)
                   >>> uri1.UserId = 'aladdin@salabim.org'
                   >>> b.Add(uri1)

               Display the contents of our Bookmarks object once more:
               
                   >>> [str(x) for x in b.Bookmarks]
                   ['rezzme://sim.salabim.org:4711/cave client: None/userId: aladdin@salabim.org/display: rezzme://sim.salabim.org:4711/cave']

               uri0 has been replaced with uri1.
           ''' 

        logging.debug('bookmarks.Bookmarks.Add: new uri %s', uri.SafeUri)
        # logging.debug('bookmarks.Bookmarks.Add: new uri %s', uri)
        if uri in self._bookmarks:
            logging.debug('bookmarks.Bookmarks.Add: new uri %s already exists, deleting it', uri.SafeUri)
            del self._bookmarks[self._bookmarks.index(uri)]
        self._bookmarks += [uri]

        if save:
            self.Save()

    def FindBestMatch(self, uri = None, display = None):
        '''Find the best matching URI in Bookmarks given either a Uri object (or string) or a display string.

           The 'best' match for a given URI is the most specific Uri object in the
           Bookmarks collection:

           - if the target Uri object has the avatar name specified,
             then the best match is the first Uri that matches on
             host, port and region; the next best match is the one
             that matches on host and port

           - if the target Uri object has no avatar name specified,
             then the best match is the first Uri that matches on
             host, port and region; the next match is that Uri object
             that matches on host and port and has a UserId attribute;
             the next best match is that Uri object that matches on
             host and port.

           Sample code: first setup a Bookmarks object

               >>> import RezzMe.bookmarks
               >>> import RezzMe.uri
               >>> b = RezzMe.bookmarks.Bookmarks()

           and add a Uri object:

               >>> uri = RezzMe.uri.Uri('rezzme://opensim.foo.com:9000/')
               >>> b.Add(uri)

           The best match for 'rezzme://opensim.foo.com:9000/' should be just that:

               >>> m = b.FindBestMatch(uri = 'rezzme://opensim.foo.com:9000/')
               >>> str(m)
               'rezzme://opensim.foo.com:9000/ client: None/userId: None/display: rezzme://opensim.foo.com:9000'


           Now, let\'s add a more specific Uri object:
           
               >>> uri = RezzMe.uri.Uri('rezzme://opensim.foo.com:9000/')
               >>> uri.UserId = 'drscofield@foo.com'
               >>> b.Add(uri)

           The best match for 'rezzme://opensim.foo.com:9000/' should now be the Uri with the UserId attribute:

               >>> m = b.FindBestMatch(uri = 'rezzme://opensim.foo.com:9000/')
               >>> str(m)
               'rezzme://opensim.foo.com:9000/ client: None/userId: drscofield@foo.com/display: rezzme://opensim.foo.com:9000'

           Adding a Uri with avatar name...

               >>> uri = RezzMe.uri.Uri('rezzme://dr%20scofield@opensim.foo.com:9000/')
               >>> b.Add(uri)

           ...should then still return the Uri with UserId attribute
           as the best match, since we are not specifying an avatar
           name in the search uri parameter:

               >>> m = b.FindBestMatch(uri = 'rezzme://opensim.foo.com:9000/')
               >>> str(m)
               'rezzme://opensim.foo.com:9000/ client: None/userId: drscofield@foo.com/display: rezzme://opensim.foo.com:9000'

           repeating the search using an avatar name, however, returns
           the Uri with the avatar name attribute:

               >>> m = b.FindBestMatch(uri = 'rezzme://dr%20scofield@opensim.foo.com:9000/')
               >>> str(m)
               'rezzme://dr%20scofield@opensim.foo.com:9000/ client: None/userId: None/display: dr scofield@rezzme://opensim.foo.com:9000'
            
           Let\'s add a Uri object with a region...

               >>> uri = RezzMe.uri.Uri('rezzme://opensim.foo.com:9000/island')
               >>> b.Add(uri)

           ...and search for just that uri...

               >>> m = b.FindBestMatch(uri = 'rezzme://opensim.foo.com:9000/island')
               >>> str(m)
               'rezzme://opensim.foo.com:9000/island client: None/userId: None/display: rezzme://opensim.foo.com:9000/island'

           If we add the same region Uri object with a UserId
           attribute set...

               >>> uri= RezzMe.uri.Uri('rezzme://opensim.foo.com:9000/island')
               >>> uri.UserId = 'drwho@tardis.net'
               >>> b.Add(uri)

           ...and then repeat the search, we should get that Uri
           object returned:
           
               >>> m = b.FindBestMatch(uri = 'rezzme://opensim.foo.com:9000/island')
               >>> str(m)
               'rezzme://opensim.foo.com:9000/island client: None/userId: drwho@tardis.net/display: rezzme://opensim.foo.com:9000/island'
               

           Adding a Uri object with avatar name...

               >>> uri= RezzMe.uri.Uri('rezzme://dr%20who@opensim.foo.com:9000/my%20land')
               >>> b.Add(uri)

           should return that Uri when searching for it:

               >>> m = b.FindBestMatch(uri = 'rezzme://dr%20who@opensim.foo.com:9000/my%20land')
               >>> str(m)
               'rezzme://dr%20who@opensim.foo.com:9000/my%20land client: None/userId: None/display: dr who@rezzme://opensim.foo.com:9000/my%20land'

           Searching for a Uri without avatar specified and a region
           that we have not bookmarked should return None:
           
               >>> m = b.FindBestMatch(uri = 'rezzme://opensim.foo.com:9000/your%20land')
               >>> str(m)
               'None'

           Searching for on the Display attribute is straight forward:

               We setup our in-memory Bookmarks object and add two Uri
               objects with explictly set Display attributes:

                   >>> b = RezzMe.bookmarks.Bookmarks()
                   >>> b.Add(RezzMe.uri.Uri('rezzme://foo.bar.com:9999/island', display = 'foo bar island'))
                   >>> b.Add(RezzMe.uri.Uri('rezzme://bar.com:9999/archipelago', display = 'bar archipelago'))

               Searching for 'foo bar island' should then
               return 'rezzme://foo.bar.com:9999/island':
               
                   >>> m = b.FindBestMatch(display = 'foo bar island')
                   >>> m.FullUri
                   'rezzme://foo.bar.com:9999/island'

               And searching for 'bar archipelago' should return
               'rezzme://bar.com:9999/archipelago':

                   >>> m = b.FindBestMatch(display = 'bar archipelago')
                   >>> m.FullUri
                   'rezzme://bar.com:9999/archipelago'
           '''

        if uri: 
            if not isinstance(uri, RezzMe.uri.Uri):
                uri = RezzMe.uri.Uri(uri)
            logging.debug('bookmarks.Bookmarks.FindBestMatch: uri %s', uri.SafeUri)

            best = None

            if uri.Avatar:
                # we've got an avatar specified: so we are only going
                # to look at bookmarks that have this avatar
                # explicitly set
                for u in [b for b in self._bookmarks if b.Avatar and b.Avatar == uri.Avatar]:
                    logging.debug('bookmarks.Bookmarks.FindBestMatch: looking at %s', u.SafeUri)
                    
                    if uri.Host == u.Host and uri.Port == u.Port and uri.Region == u.Region:
                        # host, port, region match: perfect, done
                        best = u
                        break

                    if uri.Host == u.Host and uri.Port == u.Port:
                        # host, port match: let's keep it in mind and continue looking
                        best = u

            else:
                # no avatar specified: let's see whether we can find a match
                for u in self._bookmarks:
                    logging.debug('bookmarks.Bookmarks.FindBestMatch(no avatar): looking at %s', u.SafeUri)
                    if uri.Host == u.Host and uri.Port == u.Port and uri.Region == u.Region:
                        # host, port, region match: perfect, done
                        best = u
                        break

                    ## disabling this: it confuses our users and might not have been such a hot idea
                    # if uri.Host == u.Host and uri.Port == u.Port:
                    #     # host, port match: let's keep it in mind and continue looking
                    #     if best:
                    #         if not best.UserId and u.UserId:
                    #             best = u
                    #     else:
                    #         best = u

            if best:
                logging.debug('bookmarks.Bookmarks.FindBestMatch: best match %s', best.SafeUri)
                # logging.debug('bookmarks.Bookmarks.FindBestMatch: best match %s', best)
            return best

        elif display:
            logging.debug('bookmarks.Bookmarks.FindBestMatch: display %s', display)
            for u in self._bookmarks:
                if display == u.Display: 
                    logging.debug('bookmarks.Bookmarks.FindBestMatch: %s matches %s', display, u.SafeUri)
                    return u

        return None

    def _displays(self):
        '''(internal method)'''

        return map(lambda x: x.Display, self._bookmarks)
    Displays = property(fget = _displays)

    def _bookmarks(self):
        '''(internal method)'''

        return self._bookmarks
    Bookmarks = property(fget = _bookmarks)

