Summary: Protocol handler and system tray utility for rezzme:// URIs
Name: rezzme
Version: %(version)s
Release: 1
License: OpenSim BSD License
Group: Applications/Network
Source: rezzme-%(version)s.tar.gz
BuildArch: noarch
Requires: python >= 2.4
Requires: ptyhon-qt4
Requires: gconf2

%%description
RezzMe is a protocol handler and system tray utility for rezzme://
URIs. A rezzme:// URI specifies a location in a virtual world.


%%prep
%%setup
cp $RPM_SOURCE_DIR/rezzme-redhat-readme.txt $RPM_BUILD_DIR/rezzme-%(version)s/README-RedHat-Fedora-SuSE.txt

%%build
make build
pod2man --release="$RPM_PACKAGE_VERSION" --center="rezzme" rezzme.pod > rezzme.1


%%install
make PYTHON=python2.6 DESTDIR="$RPM_BUILD_ROOT" install
make PYTHON=python2.5 DESTDIR="$RPM_BUILD_ROOT" install
make PYTHON=python2.4 DESTDIR="$RPM_BUILD_ROOT" install
find "$RPM_BUILD_ROOT" -type f -name "*.pyc" -exec rm -f {} \;
mkdir -p "$RPM_BUILD_ROOT"/usr/share/man/man1/
cp rezzme.1 "$RPM_BUILD_ROOT"/usr/share/man/man1/rezzme.1
gzip "$RPM_BUILD_ROOT"/usr/share/man/man1/rezzme.1

%%files
%%doc README.txt README-RedHat-Fedora-SuSE.txt LICENSE.txt ChangeLog.html

/usr/bin/rezzme.py
/usr/lib/python2.4/site-packages/RezzMe/__init__.py
/usr/lib/python2.4/site-packages/RezzMe/bookmarks.py
/usr/lib/python2.4/site-packages/RezzMe/config/__init__.py
/usr/lib/python2.4/site-packages/RezzMe/config/builder.py
/usr/lib/python2.4/site-packages/RezzMe/config/config.py
/usr/lib/python2.4/site-packages/RezzMe/config/desktop.py
/usr/lib/python2.4/site-packages/RezzMe/config/parser.py
/usr/lib/python2.4/site-packages/RezzMe/connect.py
/usr/lib/python2.4/site-packages/RezzMe/exceptions.py
/usr/lib/python2.4/site-packages/RezzMe/gridinfo.py
/usr/lib/python2.4/site-packages/RezzMe/launcher.py
/usr/lib/python2.4/site-packages/RezzMe/launchers/__init__.py
/usr/lib/python2.4/site-packages/RezzMe/launchers/darwin.py
/usr/lib/python2.4/site-packages/RezzMe/launchers/hippo.py
/usr/lib/python2.4/site-packages/RezzMe/launchers/linux2.py
/usr/lib/python2.4/site-packages/RezzMe/launchers/win32.py
/usr/lib/python2.4/site-packages/RezzMe/parse.py
/usr/lib/python2.4/site-packages/RezzMe/resources.py
/usr/lib/python2.4/site-packages/RezzMe/ui/__init__.py
/usr/lib/python2.4/site-packages/RezzMe/ui/about.py
/usr/lib/python2.4/site-packages/RezzMe/ui/about.ui
/usr/lib/python2.4/site-packages/RezzMe/ui/client.py
/usr/lib/python2.4/site-packages/RezzMe/ui/clientselector.py
/usr/lib/python2.4/site-packages/RezzMe/ui/clientselector.ui
/usr/lib/python2.4/site-packages/RezzMe/ui/edit.py
/usr/lib/python2.4/site-packages/RezzMe/ui/edit.ui
/usr/lib/python2.4/site-packages/RezzMe/ui/launcher.py
/usr/lib/python2.4/site-packages/RezzMe/ui/rezzme.py
/usr/lib/python2.4/site-packages/RezzMe/ui/rezzme.ui
/usr/lib/python2.4/site-packages/RezzMe/ui/tray.py
/usr/lib/python2.4/site-packages/RezzMe/uri.py
/usr/lib/python2.4/site-packages/RezzMe/utils.py
/usr/lib/python2.4/site-packages/RezzMe/version.py
/usr/lib/python2.4/site-packages/rezzme-%(version)s.egg-info
/usr/lib/python2.5/site-packages/RezzMe/__init__.py
/usr/lib/python2.5/site-packages/RezzMe/bookmarks.py
/usr/lib/python2.5/site-packages/RezzMe/config/__init__.py
/usr/lib/python2.5/site-packages/RezzMe/config/builder.py
/usr/lib/python2.5/site-packages/RezzMe/config/config.py
/usr/lib/python2.5/site-packages/RezzMe/config/desktop.py
/usr/lib/python2.5/site-packages/RezzMe/config/parser.py
/usr/lib/python2.5/site-packages/RezzMe/connect.py
/usr/lib/python2.5/site-packages/RezzMe/exceptions.py
/usr/lib/python2.5/site-packages/RezzMe/gridinfo.py
/usr/lib/python2.5/site-packages/RezzMe/launcher.py
/usr/lib/python2.5/site-packages/RezzMe/launchers/__init__.py
/usr/lib/python2.5/site-packages/RezzMe/launchers/darwin.py
/usr/lib/python2.5/site-packages/RezzMe/launchers/hippo.py
/usr/lib/python2.5/site-packages/RezzMe/launchers/linux2.py
/usr/lib/python2.5/site-packages/RezzMe/launchers/win32.py
/usr/lib/python2.5/site-packages/RezzMe/parse.py
/usr/lib/python2.5/site-packages/RezzMe/resources.py
/usr/lib/python2.5/site-packages/RezzMe/ui/__init__.py
/usr/lib/python2.5/site-packages/RezzMe/ui/about.py
/usr/lib/python2.5/site-packages/RezzMe/ui/about.ui
/usr/lib/python2.5/site-packages/RezzMe/ui/client.py
/usr/lib/python2.5/site-packages/RezzMe/ui/clientselector.py
/usr/lib/python2.5/site-packages/RezzMe/ui/clientselector.ui
/usr/lib/python2.5/site-packages/RezzMe/ui/edit.py
/usr/lib/python2.5/site-packages/RezzMe/ui/edit.ui
/usr/lib/python2.5/site-packages/RezzMe/ui/launcher.py
/usr/lib/python2.5/site-packages/RezzMe/ui/rezzme.py
/usr/lib/python2.5/site-packages/RezzMe/ui/rezzme.ui
/usr/lib/python2.5/site-packages/RezzMe/ui/tray.py
/usr/lib/python2.5/site-packages/RezzMe/uri.py
/usr/lib/python2.5/site-packages/RezzMe/utils.py
/usr/lib/python2.5/site-packages/RezzMe/version.py
/usr/lib/python2.5/site-packages/rezzme-%(version)s.egg-info
/usr/lib/python2.6/dist-packages/rezzme-%(version)s.egg-info
/usr/lib/python2.6/dist-packages/RezzMe/launcher.py
/usr/lib/python2.6/dist-packages/RezzMe/utils.py
/usr/lib/python2.6/dist-packages/RezzMe/config/desktop.py
/usr/lib/python2.6/dist-packages/RezzMe/config/builder.py
/usr/lib/python2.6/dist-packages/RezzMe/config/__init__.py
/usr/lib/python2.6/dist-packages/RezzMe/config/config.py
/usr/lib/python2.6/dist-packages/RezzMe/config/parser.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/launcher.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/edit.ui
/usr/lib/python2.6/dist-packages/RezzMe/ui/tray.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/edit.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/__init__.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/rezzme.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/clientselector.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/clientselector.ui
/usr/lib/python2.6/dist-packages/RezzMe/ui/about.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/about.ui
/usr/lib/python2.6/dist-packages/RezzMe/ui/client.py
/usr/lib/python2.6/dist-packages/RezzMe/ui/rezzme.ui
/usr/lib/python2.6/dist-packages/RezzMe/resources.py
/usr/lib/python2.6/dist-packages/RezzMe/connect.py
/usr/lib/python2.6/dist-packages/RezzMe/__init__.py
/usr/lib/python2.6/dist-packages/RezzMe/version.py
/usr/lib/python2.6/dist-packages/RezzMe/bookmarks.py
/usr/lib/python2.6/dist-packages/RezzMe/parse.py
/usr/lib/python2.6/dist-packages/RezzMe/uri.py
/usr/lib/python2.6/dist-packages/RezzMe/gridinfo.py
/usr/lib/python2.6/dist-packages/RezzMe/exceptions.py
/usr/lib/python2.6/dist-packages/RezzMe/launchers/hippo.py
/usr/lib/python2.6/dist-packages/RezzMe/launchers/__init__.py
/usr/lib/python2.6/dist-packages/RezzMe/launchers/win32.py
/usr/lib/python2.6/dist-packages/RezzMe/launchers/darwin.py
/usr/lib/python2.6/dist-packages/RezzMe/launchers/linux2.py
/usr/share/man/man1/rezzme.1.gz
/usr/share/kde4/services/rezzme.protocol
/usr/share/kde4/services/rezzmes.protocol
/usr/share/services/rezzme.protocol
/usr/share/services/rezzmes.protocol
/usr/share/applications/rezzme.desktop
/usr/share/pixmaps/rezzme.png
/usr/share/icons/hicolor/32x32/apps/rezzme.png
