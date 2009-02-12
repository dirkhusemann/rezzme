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

def InstallProtocolHandlers():
    if not sys.platform == 'linux2':
        return
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
