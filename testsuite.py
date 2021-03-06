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
import unittest
import doctest

# import modules to test
import RezzMe.exceptions
import RezzMe.parse
import RezzMe.uri
import RezzMe.bookmarks
import RezzMe.version
import RezzMe.tests.gridinfo

# setup a test suite
def suite():
    s = unittest.TestSuite()

    s.addTest(doctest.DocTestSuite(RezzMe.exceptions))
    s.addTest(doctest.DocTestSuite(RezzMe.parse))
    s.addTest(doctest.DocTestSuite(RezzMe.uri))
    s.addTest(doctest.DocTestSuite(RezzMe.bookmarks))
    s.addTest(doctest.DocTestSuite(RezzMe.utils))
    s.addTest(doctest.DocTestSuite(RezzMe.version))
    s.addTest(unittest.TestLoader().loadTestsFromTestCase(RezzMe.tests.gridinfo.GridInfoTestCase))

    return s

# provide plumbing to run stand-alone
if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR)

    suite = suite()
    print '\n\nrezzme test suite: %d test case%s\n' % (suite.countTestCases(), 's' if suite.countTestCases() > 1 else '')

    runner = unittest.TextTestRunner(verbosity = 3)
    runner.run(suite)
    
