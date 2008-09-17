#!/usr/bin/python
# -*- encoding: utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

import os
import sys
from setuptools import setup
from ConfigParser import RawConfigParser
import pprint

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

if not os.path.exists('rezzme.cfg'):
    print '''
oops...you need to create rezzme.cfg first!'

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

# basic setup driven by rezzme.cfg
config = RawConfigParser()
config.readfp(open('rezzme.cfg'))


# convert rezzme.cfg to RezzMe/config/config.py
cfg = {}
for section in config.sections():
    cfg[section] = {}
    for option in config.options(section):
        cfg[section][option] = config.get(section, option)
try:
    py = open('RezzMe/config/config.py', 'w')
    py.write('''
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# AUTOMATICALLY GENERATED, CHANGES HERE WILL BE LOST FOREVER
def config():
    return %s

# done
''' % str(cfg))
    py.close()
except IOError, (errno, strerror):
    print 'failed to create RezzMe/config/config.py (%s)' % strerror
    sys.exit(0)


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



# platform specific tweaks
if onMacOSX:
    extra_options = {
        'app' : [application],
        'setup_requires': [ 'py2app' ],
        'options': {
            'py2app' : {
                'includes': ['sip', 
                             'appscript',
                             'RezzMe.launchers.darwin'],
                'argv_emulation' : True,
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
    import pkg_resources
    pkg_resources.require("setuptools")

    extra_options = {
        'windows': [{'script' : application, 
                     'icon_resources': [(1, 'rezzme.ico')]}],
        'options': {
            'py2exe': {
                'includes': ['sip', 
                             'RezzMe.launchers.win32',
                             'setuptools'],
                'dist_dir': 'dist-win32',
                }
            }
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
    import subprocess
    gconftool2 = subprocess.Popen(['which', 'gconftool-2'], stdout = subprocess.PIPE)
    gconftool2 = gconftool2.communicate()[0].rstrip('\n')

    if gconftool2:
        print 'setting up rezzme.py as GNOME protocol handler for rezzme:// URIs'
        os.system('%s -t string -s /desktop/gnome/url-handlers/rezzme/command "/usr/bin/rezzme.py %%s"' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzme/needs_terminal false' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzme/enabled true' % gconftool2)

        os.system('%s -t string -s /desktop/gnome/url-handlers/rezzmes/command "/usr/bin/rezzme.py %%s"' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzmes/needs_terminal false' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzmes/enabled true' % gconftool2)

        print '''
    i tried to use gconftool-2 on your system to configure gnome,
    firefox, and thunderbird for the rezzme:// protocol. 
    '''
        
    if os.path.exists('/usr/share/services'):
        print 'setting up rezzme.py as KDE protocol handler for rezzme(s):// URIs'
        os.system('cp rezzme.protocol /usr/share/services/rezzme.protocol')
        os.system('cp rezzmes.protocol /usr/share/services/rezzmes.protocol')

        print '''
    i tried to install rezzme.protocol as a KDE service into /usr/share/services
    on your system to configure KDE for the rezzme:// protocol.
    '''

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
