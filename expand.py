#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import with_statement

import ConfigParser
import os
import sys

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

# check prereqs
if not os.path.exists('rezzme.cfg'):
    print '''
oops...you need to create rezzme.cfg first!'

copy rezzme.cfg.example to rezzme.cfg and adapt it to your needs,
and run me again.
'''
    sys.exit(1)

if len(sys.argv) != 3:
    print 'usage: expand.py in-file out-file'
    sys.exit(2)

# read in configuration
config = ConfigParser.RawConfigParser()
config.readfp(open('rezzme.cfg'))

# convert rezzme.cfg to RezzMe/config/config.py
cfg = {}
for section in config.sections():
    cfg[section] = {}
    for option in config.options(section):
        cfg[section][option] = config.get(section, option)

with open(sys.argv[1], 'r') as infile:
    infile = infile.read()

with open(sys.argv[2], 'w') as outfile:
    outfile.write(infile % cfg['package'])

