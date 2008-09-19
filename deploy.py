#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
from ConfigParser import RawConfigParser
import RezzMe.config.builder

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
    print 'distributable %s not (yet) existing. see later...' % distributable
    sys.exit(1)

print '- deploying %s installer %s to %s' % (sys.platform, distributable, remote)
os.system('scp %s %s' % (distributable, remote))
