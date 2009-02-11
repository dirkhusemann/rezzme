#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import with_statement

import codecs
import ConfigParser
import os
import sys

import RezzMe.config.builder

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

# check prereqs
if not os.path.exists('rezzme.cfg'):
    print '''
oops...you need to create rezzme.cfg first!

copy rezzme.cfg.example to rezzme.cfg and adapt it to your needs,
and run me again.
'''
    sys.exit(1)

if len(sys.argv) != 3:
    print 'usage: expand.py in-file out-file'
    sys.exit(2)

# read in configuration
cfg = RezzMe.config.builder.buildCfg('rezzme')

with codecs.open(sys.argv[1], 'r', 'utf8') as infile:
    infile = infile.read()

with codecs.open(sys.argv[2], 'w', 'utf8') as outfile:
    outfile.write(infile % cfg['package'])

