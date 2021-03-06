#!/usr/bin/python
# -*- encoding: utf-8 -*-

import ConfigParser
import os
import sys
import RezzMe.config.builder

onMacOSX = sys.platform == 'darwin'
onLinux = sys.platform == 'linux2'
onWindows = sys.platform == 'win32'

if not os.path.exists('rezzme.cfg'):
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


if onWindows: import _winreg

# required for windows :-(
cmdKeys = {
    'python': '\\Python.File\\shell\\open\\command',
    'istool': '\\InnoSetupScriptFile\\shell\\OpenWithISTool\\command'
    }

def system(cmd):
    (cmd, args) = cmd.split(' ', 1)

    if onWindows:
        # sigh, we cannot just invoke "python ...", no, we need to
        # locate it via the almighty egistry...
        cmdKey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, cmdKeys[cmd])
        if not cmdKey: 
            print 'cannot find registry entry for %s...' % cmd
            sys.exit(1)
        # ...and, adding insult to injury, we need to quote the
        # command ("C:\Program Files\..." and you are hosed)
        cmd = '"%s"' %_winreg.QueryValueEx(cmdKey, None)[0].split('"')[1]

    os.system('%s %s' % (cmd, args))

# read in configuration
cfg = RezzMe.config.builder.buildCfg('rezzme')

version = cfg['package']['version']
name = cfg['package']['name']

command = cfg[sys.platform]['build']

# use platform independent system(), this needs to run on all platforms
system('python -OO setup.py %s' % command)

# post processing: mac osx: create disk image
if onMacOSX:
    folder = '%s-%s' % (name, version)

    # create diskimage folder
    print 'creating internet disk image %s.dmg' % folder

    if os.path.exists(folder): os.system('rm -rf %s' % folder)
    os.mkdir(folder)

    # copy rezzme.app to diskimage folder
    os.system('cp -R dist/%s.app %s/%s.app' % (name, folder, name))
    # create new diskimage
    os.system('rm -rf %s.dmg' % folder)
    os.system('hdiutil create -volname %s -srcfolder %s %s.dmg' % (folder, folder, folder))
    # convert to internet format
    os.system('hdiutil internet-enable -yes %s.dmg' % folder)
    os.system('cp %s.dmg dist/%s.dmg' % (folder, folder))
    os.system('rm -rf %s' % folder)

# post processing: windows: create installer
if onWindows:

    # build dict with package parameters
    pkg = {
        'source': os.getcwd(),
        'name': cfg['package']['name'],
        'version': cfg['package']['version'],
        'url': cfg['package']['url'],
        'protocol': cfg['package']['protocol'],
        }
    
    issRaw = open('setup.iss', 'r')
    iss = open('%s.iss' % name, 'w')

    for line in issRaw:
        iss.write(line % pkg)

    issRaw.close()
    iss.close()

    system('istool %s.iss' % name)



