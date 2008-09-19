#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys

from ConfigParser import RawConfigParser

config = RawConfigParser()
config.readfp(open('rezzme.cfg'))
config.read(['rezzme-site.cfg'])

if not config.has_option('deploy', 'remote'):
    print "could not find a [deploy] section with 'remote' variable. giving up."
    sys.exit(1)

version = config.get('package', 'version')
target = config.get(sys.platform, 'target')

source = config.get(sys.platform, 'source') % {'version': version }
remote = config.get('deploy', 'remote') % {'target': target}

distributable = 'dist/%s' % source


# sanity checks
if not os.path.exists(distributable):
    print 'distributable %s not (yet) existing. see later...' % distributable
    sys.exit(1)

print '- deploying %s installer %s to %s' % (sys.platform, distributable, remote)
os.system('scp %s %s' % (distributable, remote))
