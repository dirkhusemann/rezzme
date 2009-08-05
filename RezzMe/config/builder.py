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

import codecs
import ConfigParser
import os
import RezzMe.config.parser
import RezzMe.version

def buildCfg(name):
    
    config = RezzMe.config.parser.Parser()
    sealed = False

    if os.path.exists('%s.cfg' % name):
        config.readfp(codecs.open('%s.cfg' % name, 'r', 'utf8'))
        config.read(['%s-site.cfg' % name])
    elif os.path.exists('%s-sealed.cfg' % name):
        config.readfp(codecs.open('%s-sealed.cfg' % name, 'r', 'utf8'))
        sealed = True

    # convert rezzme.cfg to RezzMe/config/config.py
    # using the following presets
    cfg = {
        'package': {
            'version'   : RezzMe.version.Version,
            'name'      : 'rezzme',
            'author'    : 'dirk husemann',
            'email'     : 'hud@zurich.ibm.com',
            'summary'   : 'rezzme:// protocol handler',
            'license'   : 'http://opensimulator.org/wiki/BSD_Licensed',
            'url'       : 'http://forge.opensimulator.org/gf/project/rezzme/',
            'protocol'  : 'rezzme',
            'publisher' : 'he who must not be named',
            },
        'deploy' : {},
        'linux2' : {},
        'win32'  : {},
        'darwin' : {},
        'deploy' : {},
        'debug'  : {},
        }

    for section in config.sections():
        if not section in cfg:
            cfg[section] = {}
        for option in config.options(section):
            cfg[section][option] = config.get(section, option)

    if not sealed:
        writeCfg(cfg, name)

    return cfg

def writeCfg(cfg, name):

    config = ConfigParser.RawConfigParser()
    for section in cfg:
        if not config.has_section(section):
            config.add_section(section)
        for option in cfg[section]:
            config.set(section, option, cfg[section][option])

    try:
        c = codecs.open('%s-sealed.cfg' % name, 'w', 'utf8')
        config.write(c)
        c.close()
    except: pass
