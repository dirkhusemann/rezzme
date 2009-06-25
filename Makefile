PYUIC	= pyuic4
PYRCC	= pyrcc4
EXPAND  = python ./expand.py
# SVN2CL  = svn2cl --group-by-day --separate-daylogs --include-rev --authors=AUTHORS -r HEAD:1
# SVN2HTML = svn2cl --group-by-day --separate-daylogs --include-rev --html --authors=AUTHORS -r HEAD:1
GIT2CL = git log > ChangeLog

PYTHONPATH = $(shell pwd)


.PHONY: clean build deploy all changelog

-include Makefile.local

all: build deploy changelog

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
	python ./build.py

test: build
	PYTHONPATH=${PYTHONPATH} python testsuite.py

deploy:
	python ./deploy.py

RezzMe/config/config.py: rezzme.cfg 
	python ./config.py RezzMe/config/config.py

about.html : about.raw.html rezzme.cfg
	${EXPAND} $< $@

rezzme.desktop : rezzme.raw.desktop rezzme.cfg
	${EXPAND} $< $@

rezzme.qrc : rezzme.raw.qrc rezzme.cfg
	${EXPAND} $< $@

MANIFEST.in : MANIFEST.raw.in rezzme.cfg
	${EXPAND} $< $@

resources: rezzme.png about.html rezzme.qrc rezzme.desktop MANIFEST.in
	${PYRCC} -o RezzMe/resources.py rezzme.qrc

changelog: 
	@echo "attempting to update ChangeLog"
	@cat ChangeLog.pre.html > ChangeLog.html
	@git log >> ChangeLog.html
	@cat ChangeLog.post.html >> ChangeLog.html
