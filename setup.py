#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
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

try:
    import PyQt4.QtCore
except:
    print '''
oops...you need to install PyQt4 first otherwise rezzme will not
work at all.
'''
    sys.exit(2)

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
if sys.argv.count > 1: command = sys.argv[1]

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
                    'Label': 'rezzme-%s'% cfg['package']['version'],
                    'ProgramArguments': ['rezzme'],
                    'KeepAlive': False,
                    'RunAtLoad': True,
                    'OnDemand': False,
                    }
                }
            }
        }
    
elif platform == 'win32':
    import py2exe
    import pkg_resources
    pkg_resources.require("setuptools")

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
                'includes': ['sip', 
                             'RezzMe.launchers.win32',
                             'setuptools'],
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

    for s in ['/usr/share/services', '/usr/share/kde4/services']:
        if os.path.exists(s):
            print 'setting up rezzme.py as KDE protocol handler for rezzme(s):// URIs via %s' % s
            os.system('cp rezzme.protocol %s/rezzme.protocol' % s)
            os.system('cp rezzmes.protocol %s/rezzmes.protocol' % s)

            print '''
    i tried to install rezzme.protocol as a KDE service into %s
    on your system to configure KDE for the rezzme:// protocol.
    ''' % s


    if os.path.exists('/usr/share/applications'):
        print 'copying rezzme.desktop to /usr/share/applications'
        os.system('cp rezzme.desktop /usr/share/applications')
        if not os.path.exists('/usr/share/icons/hicolor/32x32/apps'):
            os.system('mkdir -p /usr/share/icons/hicolor/32x32/apps')
        print 'copying %s to /usr/share/icons/hicolor/32x32/apps' % cfg['package']['icon_32']
        os.system('cp %s /usr/share/icons/hicolor/32x32/apps' % cfg['package']['icon_32'])
        

    print '''
you might need to add the following config entries to
firefox's and thundebird's configurations:

    network.protocol-handler.app.rezzme    "/usr/bin/rezzme.py"
    network.protocol-handler.app.rezzmes   "/usr/bin/rezzme.py"

the easiest way to do this is via about:config (a very good add-on
for both firefox and thunderbird to deal with about:config is "Mr
Tech Toolkit" available at

    https://addons.mozilla.org/en-US/firefox/addon/421

alternatively you could do this via the prefs.js file of firefox
and thunderbird.
'''

    sys.exit(0)
