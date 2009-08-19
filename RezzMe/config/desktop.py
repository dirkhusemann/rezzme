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
import subprocess
import os
import sys

import RezzMe.config.builder

def InstallProtocolHandlers():
    if sys.platform == 'linux2':
        LinuxInstallProtocolHandlers()
    elif sys.platform == 'darwin':
        MacOSXInstallLaunchdSupport()

def LinuxInstallProtocolHandlers():
    logging.debug('config.desktop: installing rezzme: protocol handlers for linux')
    gconftool2 = subprocess.Popen(['which', 'gconftool-2'], stdout = subprocess.PIPE)
    gconftool2 = gconftool2.communicate()[0].rstrip('\n')

    if gconftool2:
        logging.debug('config.desktop: setting up GNOME protocol handler for rezzme:// URIs')
        os.system('%s -t string -s /desktop/gnome/url-handlers/rezzme/command "/usr/bin/rezzme.py %%s"' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzme/needs_terminal false' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzme/enabled true' % gconftool2)

        logging.debug('config.desktop: setting up GNOME protocol handler for rezzmes:// URIs')
        os.system('%s -t string -s /desktop/gnome/url-handlers/rezzmes/command "/usr/bin/rezzme.py %%s"' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzmes/needs_terminal false' % gconftool2)
        os.system('%s -t bool -s /desktop/gnome/url-handlers/rezzmes/enabled true' % gconftool2)

def MacOSXInstallLaunchdSupport():
    cfg = RezzMe.config.builder.buildCfg('rezzme')

    rezzmePath = sys.argv[0]
    if not os.path.exists(rezzmePath):
        logging.info('config.desktop: funny, cannot find rezzme at %s', rezzmePath)
        return

    if not os.path.exists(os.path.expanduser('~/Library/LaunchAgents')):
        try:
            os.makedirs(os.path.expanduser('~/Library/LaunchAgents'))
        except:
            pass
    if not os.path.exists(os.path.expanduser('~/Library/LaunchAgents')):
        logging.info('config.desktop: funny, cannot create %s',
                     os.path.expanduser('~/Library/LaunchAgents'))
        return

    if os.path.exists(os.path.expanduser('~/Library/LaunchAgents/rezzme.plist')):
        os.unlink(os.path.expanduser('~/Library/LaunchAgents/rezzme.plist'))

    try:
        plist = open(os.path.expanduser('~/Library/LaunchAgents/rezzme.plist'), 'w')
        plist.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
        "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>Label</key>
        <string>rezzme-%s</string>
        <key>ProgramArguments</key>
        <array>
                <string>%s</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAliver</key>
        <false/>
        <key>OnDemand</key>
        <false/>
</dict>
</plist>''' % (cfg['package']['version'], rezzmePath))
        plist.close()
    except Exception, e:
        logging.info("config.desktop: couldn't create launchd agent: %s" % e)

            
