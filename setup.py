#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import optparse
import pprint
import re
import sys

from distutils.core import setup

import RezzMe.config.builder
import RezzMe.version

def incrementVersion(versionFile, version):
    (major, minor, rel) = version.split('.')
    rel = int(rel) + 1
    version = '%d.%d.%d' % (int(major), int(minor), rel)

    if os.path.exists(versionFile):
        if os.path.exists('%s~' % versionFile):
            os.unlink('%s~' % versionFile)
        os.rename(versionFile, '%s~' % versionFile)

    versionFile = open(versionFile, 'w')
    versionFile.write("""
#!/usr/bin/python
# -*- encoding: utf-8 -*-

'''Package version.

   You can access this via RezzMe.version.Version:

       >>> import RezzMe.version
       >>> RezzMe.version.Version
       '%(version)s'
   '''

Version = '%(version)s'
""" % dict(version = version))
    versionFile.close()

    print 'new version: %s' % version
        


onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

if not os.path.exists('rezzme.cfg') and not os.path.exists('rezzme-sealed.cfg'):
    print '''
oops...you need to create rezzme.cfg first!

copy rezzme.cfg.example to rezzme.cfg and adapt it to your needs,
and run me again.
'''
    sys.exit(1)

# try:
#     import PyQt4.QtCore
# except:
#     print '''
# oops...you need to install PyQt4 first otherwise rezzme will not
# work at all.
# '''
#     sys.exit(2)

# basic setup driven by rezzme.cfg and rezzme-site.cfg

cfg = RezzMe.config.builder.buildCfg('rezzme')

application  = 'rezzme.py'
packages     = ['RezzMe', 
                'RezzMe.config', 
                'RezzMe.launchers', 
                'RezzMe.ui']

package_data = { 'RezzMe.config': ['*.cfg'],
                 'RezzMe.ui' : ['*.ui']}

command = None
platform = sys.platform
root = '/'

if sys.argv.count > 1:
    command = sys.argv[1]

    parser = optparse.OptionParser()
    parser.add_option('--root', dest = 'root')
    parser.add_option('--install-layout', dest = 'layout')
    parser.add_option('--format', dest = 'layout')
    (options, args) = parser.parse_args(sys.argv[2:])

    if options.root:
        root = options.root

print 'using install root %s' % root


if command == 'newversion':
    incrementVersion('RezzMe/version.py', RezzMe.version.Version)
    sys.exit(0)


# platform specific tweaks
if onMacOSX:

    import py2app

    icon = cfg['package']['icon_mac']

    extra_options = {
        'app' : [application],
        'setup_requires': [ 'py2app' ],
        'options': {
            'py2app' : {
                'includes': ['sip', 
                             'appscript',
                             'RezzMe.launchers.darwin'],
                'argv_emulation' : False,
                'iconfile' : icon,
                'plist' : {
                    'CFBundleGetInfoString': cfg['package']['summary'],
                    'CFBundleURLTypes': [ 
                        { 
                            'CFBundleTypeRole': 'Viewer',
                            'CFBundleURLName' : cfg['package']['name'],
                            'CFBundleURLSchemes' : ['rezzme', 'rezzmes']
                            }
                        ],
                    'CFBundleVersion': cfg['package']['version'],
                    'CFBundleShortVersionString' : cfg['package']['version'],
                    'LSUIElement': '1',
                    'NSAppleScriptEnabled' : True,
                    }
                }
            }
        }
    
elif platform == 'win32':

    import py2exe
    # import pkg_resources
    # pkg_resources.require("setuptools")

    reIcon = re.compile(r'(?P<name>.*)\.png$', re.IGNORECASE)
    icon = cfg['package']['icon_32']
    im = reIcon.match(icon)
    if im:
        icon = '%s.ico' % im.group('name')

    extra_options = {
        'windows': [{'script' : application, 
                     'icon_resources': [(1, icon)]}],
        'options': {
            'py2exe': {
                'includes': ['sip', 'RezzMe.launchers.win32'],
                'dist_dir': 'dist-win32',
                'bundle_files': 1,
                'optimize': 2,
                }
            },
        'zipfile': None,
        }

else:

     extra_options = {
         'scripts': [application]
         }

setup(name = cfg['package']['name'], 
      version = cfg['package']['version'], 
      author = cfg['package']['author'], 
      author_email = cfg['package']['email'],
      description = cfg['package']['summary'], 
      license = cfg['package']['license'],
      url = cfg['package']['url'],

      packages = packages, 
      package_data = package_data,
      **extra_options)


            
# post setup install/py2app

if not command: sys.exit(0)

if command == 'install' and platform == 'linux2':

    cfg = RezzMe.config.builder.buildCfg('rezzme-sealed')

    for s in ['usr/share/services', 'usr/share/kde4/services']:

        s = '%s/%s' % (root, s)
        if not os.path.exists(s):
            os.system('mkdir -p %s' % s)

        print 'setting up rezzme.py as KDE protocol handler for rezzme(s):// URIs via %s' % s
        os.system('cp rezzme.protocol %s/rezzme.protocol' % s)
        os.system('cp rezzmes.protocol %s/rezzmes.protocol' % s)


    for s in ['usr/share/applications']:

        s = '%s/%s' % (root, s)
        if not os.path.exists(s):
            os.system('mkdir -p %s' % s)

        print 'copying rezzme.desktop to %s' % s
        os.system('cp rezzme.desktop %s' % s)

    
    for s in ['usr/share/icons/hicolor/32x32/apps', 'usr/share/pixmaps']:

        s = '%s/%s' % (root, s)
        if not os.path.exists(s):
            os.system('mkdir -p %s' % s)
        print 'copying %s to %s' % (cfg['package']['icon_32'], s)
        os.system('cp %s %s' % (cfg['package']['icon_32'], s))
        
    sys.exit(0)
