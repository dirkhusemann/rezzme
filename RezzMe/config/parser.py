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

import ConfigParser
import logging
import os

class Parser(ConfigParser.RawConfigParser):

    def __init__(self, configFile = None):
        ConfigParser.RawConfigParser.__init__(self)

        self._file = configFile

        if not configFile:
            return

        self._file = os.path.expanduser(self._file)
        if not os.path.exists(self._file):
            return

        try:
            ConfigParser.RawConfigParser.readfp(self, open(self._file, 'r'))
        except IOError:
            logging.error('RezzMe.config.parser.Parser: cannot load config file %s', self._file)
        except ConfigParser.MissingSectionHeaders:
            logging.info('RezzMe.config.parser.Parser: encountered old style config file %s', self._file)
        finally:
            if os.path.exists('%s.broken' % self._file):
                os.remove('%s.broken' % self._file)
            os.rename(self._file, '%s.broken' % self._file)


    def save(self, configFile = None):
        if not configFile and not self._file:
            raise IOError('RezzMe.config.parser.Parser: missing config file name')
        if not configFile: configFile = self._file

        if os.path.exists(configFile):
            if os.path.exists('%s~' % configFile):
                os.remove('%s~' % configFile)
            os.rename(configFile, '%s~' % configFile)

        self.write(open(configFile, 'w'))

    def get(self, section, option):
        if not self.has_section(section):
            return None
        if not self.has_option(section, option):
            return None
        return ConfigParser.RawConfigParser.get(self, section, option)

    def set(self, section, option, value):
        if not self.has_section(section):
            self.add_section(section)
        ConfigParser.RawConfigParser.set(self, section, option, value)

    def add_section(self, section):
        if self.has_section(section):
            return
        ConfigParser.RawConfigParser.add_section(self, section)
