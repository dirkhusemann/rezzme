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

import unittest
import BaseHTTPServer
import RezzMe.gridinfo
import threading

class TestGridInfoRequest(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        gridInfo = '''<gridinfo>
            <login>http://opensim.foo.com:9000/</login>
            <authenticator>http://reception.foo.com/let/me/in</authenticator>
        </gridinfo>'''

        self.send_response(200)
        self.send_header('Content-Type', 'text/xml')
        self.send_header('Content-Length', len(gridInfo))
        self.end_headers()

        self.wfile.write(gridInfo)
        self.wfile.close()

    def log_request(self, code, size = 0):
        pass


class GridInfoTestCase(unittest.TestCase):
    def setUp(self):
        # instantiate HttpServer for GridInfo
        self.server = BaseHTTPServer.HTTPServer(('127.0.0.1', 0), TestGridInfoRequest)
        self.port = self.server.server_address[1]
        
        t = threading.Thread(name = 'TestGridInfoRequest',
                             target = lambda: self.server.handle_request())
        t.setDaemon(True)
        t.start()

    def testGridInfo(self):
        info = RezzMe.gridinfo.GetGridInfo(RezzMe.uri.Uri('rezzme://127.0.0.1:%d' % self.port))
        self.failUnless(info['login'] == 'http://opensim.foo.com:9000/')
        self.failUnless(info['authenticator'] == 'http://reception.foo.com/let/me/in')
