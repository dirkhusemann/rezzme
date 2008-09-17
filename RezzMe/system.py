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

import sys
import RezzMe.exceptions
import RezzMe.parse

# on MacOS X we are running as an apple event server and receive the
# URL as a GUR,GURL event
if sys.platform == 'darwin':
    import aemreceive.sfba as AE

def PlugIn(connect):
    '''Plug into the specific platform as a protocol handler.

       depending on the platform will operate on one-shot-mode or as a
       server for rezzme:// URI events.
       '''
    if sys.platform == 'linux2' or sys.platform == 'win32':

        if not sys.argv:
            raise RezzMe.exceptions.RezzMeException('Oops: no rezzme:// URI found. Is your protocol handler set up correctly?')

        uri = None
        for uri in sys.argv:
            uriLower = uri.lower()
            if uriLower.startswith('rezzme://'): 
                connect(uri)
                sys.exit(0)

        raise RezzMe.exceptions.RezzMeException("hmm...couldn't find a rezzme:// URI in %s" % ' '.join(sys.argv))

    elif sys.platform == 'darwin':
            
        def OsXUrlHandler(uri):
            connect(uri)

        AE.installeventhandler(OsXUrlHandler, 'GURLGURL', ('----', 'uri', AE.kAE.typeUnicodeText))
        AE.starteventloop()

    else:
        raise RezzMe.exceptions.RezzMeException('oops...what platform did we end up on? no idea what "%s" is suppposed to be...' % 
                                                sys.platform)

