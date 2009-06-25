
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# AUTOMATICALLY GENERATED, CHANGES HERE WILL BE LOST FOREVER
def config():
    return {'linux2': {u'source': u'rezzme-%(version)s.tar.bz2', u'build': u'sdist --format=bztar', u'target': u'rezzme.tar.bz2'}, u'feedback': {u'to': u'hud@zurich.ibm.com', u'smtp': u'mailer.zurich.ibm.com'}, 'deploy': {u'winzip': u'dirk@opensim.zurich.ibm.com:/var/www/opensim.zurich.ibm.com/rezzme/%(name)s-win32-dist.zip', u'remote': u'dirk@opensim.zurich.ibm.com:/var/www/opensim.zurich.ibm.com/rezzme/%(target)s'}, 'package': {u'icon_16': u'rezzme.png', 'publisher': u'IBM Corporation', u'about': u'about.html', 'protocol': 'rezzme', 'name': 'rezzme', 'license': 'http://opensimulator.org/wiki/BSD_Licensed', 'author': 'dirk husemann', 'url': 'http://forge.opensimulator.org/gf/project/rezzme/', 'summary': 'rezzme:// protocol handler', u'version': u'7.0.4', u'icon_mac': u'rezzme.icns', 'email': 'hud@zurich.ibm.com', u'icon_32': u'rezzme.png'}, 'win32': {u'source': u'rezzme-setup.exe', u'build': u'py2exe', u'target': u'rezzme-setup.exe'}, 'debug': {u'level': u'DEBUG'}, 'darwin': {u'source': u'rezzme-%(version)s.dmg', u'build': u'py2app', u'target': u'rezzme.dmg'}}

# done
