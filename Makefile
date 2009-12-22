PYUIC	= pyuic4
PYRCC	= pyrcc4
EXPAND  = python ./expand.py
# SVN2CL  = svn2cl --group-by-day --separate-daylogs --include-rev --authors=AUTHORS -r HEAD:1
# SVN2HTML = svn2cl --group-by-day --separate-daylogs --include-rev --html --authors=AUTHORS -r HEAD:1
GIT2CL = git log > ChangeLog

PYTHONPATH = $(shell pwd)
PYTHON = python
DESTDIR = /

.PHONY: clean build deploy all changelog newversion

-include Makefile.local

all: build deploy changelog

newversion:
	${PYTHON} ./setup.py newversion
	rm -f VERSION
	${MAKE} deb-newversion

clean:
	rm -rf dist build dist_win32 dist-win32
	rm -rf rezzme*.dmg
	rm -rf MANIFEST.in
	rm -rf rezzme-sealed.cfg
	rm -rf rezzme.desktop
	rm -rf rezzme.qrc
	rm -rf RezzMe/resources.py
	rm -rf RezzMe/config/config.py
	make -C RezzMe/ui clean

build: changelog resources rezzme.ico RezzMe/config/config.py 
	make -C RezzMe/ui all
	${PYTHON} ./build.py

install: 
	${PYTHON} setup.py install --install-layout=deb --root=$(DESTDIR)

test: build
	PYTHONPATH=${PYTHONPATH} ${PYTHON} testsuite.py

deploy:
	${PYTHON} ./deploy.py

RezzMe/config/config.py: rezzme.cfg RezzMe/version.py
	${PYTHON} ./config.py RezzMe/config/config.py

about.html : about.raw.html rezzme.cfg RezzMe/version.py
	${EXPAND} $< $@

rezzme.desktop : rezzme.raw.desktop rezzme.cfg RezzMe/version.py
	${EXPAND} $< $@

rezzme.qrc : rezzme.raw.qrc rezzme.cfg RezzMe/version.py 
	${EXPAND} $< $@

MANIFEST.in : MANIFEST.raw.in rezzme.cfg RezzMe/version.py
	${EXPAND} $< $@

VERSION: VERSION.raw
	${EXPAND} $< $@

resources: rezzme.png about.html rezzme.qrc rezzme.desktop MANIFEST.in VERSION
	${PYRCC} -o RezzMe/resources.py rezzme.qrc

changelog: 
	@echo "attempting to update ChangeLog"
	@cat ChangeLog.pre.html > ChangeLog.html
	@git log >> ChangeLog.html
	@cat ChangeLog.post.html >> ChangeLog.html

deb-newversion: VERSION
	git tag -f debian/$(shell cat VERSION)
	git-dch --new-version=$(shell cat VERSION) --release

deb:	clean build
	@echo "building debian package"
	@rm -rf packaging
	@mkdir packaging
	@(cd packaging; \
		tar xvf ../dist/rezzme-$(shell cat VERSION).tar.gz; \
		cp ../dist/rezzme-$(shell cat VERSION).tar.gz rezzme_$(shell cat VERSION | sed -e 's/-/_/g').orig.tar.gz)
	@cp -a debian packaging/rezzme-$(shell cat VERSION)
	@(cd packaging/rezzme-$(shell cat VERSION); \
		debuild)
	@cp packaging/rezzme_$(shell cat VERSION)*.deb dist
