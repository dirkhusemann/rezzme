
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# AUTOMATICALLY GENERATED, CHANGES HERE WILL BE LOST FOREVER
def config():
    return {'linux2': {'source': 'rezzme-%(version)s.tar.bz2', 'build': 'sdist --format=bztar', 'target': 'rezzme.tar.bz2'}, 'package': {'publisher': 'IBM Research GmbH', 'protocol': 'rezzme', 'name': 'rezzme', 'license': 'IBM Internal', 'author': 'dirk husemann', 'url': 'http://opensim.zurich.ibm.com/', 'summary': 'rezzme:// protocol handler (IBM version)', 'version': '3.0.0', 'email': 'hud@zurich.ibm.com'}, 'deploy': {'remote': 'hud@opensim.zurich.ibm.com:/var/www/opensim.zurich.ibm.com/rezzme/%(target)s'}, 'win32': {'source': 'rezzme-setup.exe', 'build': 'py2exe', 'target': 'rezzme-setup.exe'}, 'default rezzmes': {'osgrid': 'rezzme://www.osgrid.org:8002/', 'secondlife main grid': 'rezzme://lindenlab.com/', 'secondlife beta grid': 'rezzme://aditi.lindenlab.com/'}, 'darwin': {'source': 'rezzme-%(version)s.dmg', 'build': 'py2app', 'target': 'rezzme.dmg'}}

# done
