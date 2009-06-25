#!/usr/bin/python
# -*- encoding: utf-8 -*-

from ConfigParser import RawConfigParser
import os
import sys

import RezzMe.config.builder

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'


cfg = RezzMe.config.builder.buildCfg('rezzme')

if not 'remote' in cfg['deploy']:
    print "could not find a [deploy] section with 'remote' variable. giving up."
    sys.exit(1)

version = cfg['package']['version']
target = cfg[sys.platform]['target']

source = cfg[sys.platform]['source'] % {'version': version }
remote = cfg['deploy']['remote'] % {'target': target}

distributable = 'dist/%s' % source


# sanity checks
if not os.path.exists(distributable):
    print 'distributable %s not (yet) existing. see you later...' % distributable
    sys.exit(1)

print '- deploying %s installer %s to %s' % (sys.platform, distributable, remote)
os.system('scp %s %s' % (distributable, remote))
