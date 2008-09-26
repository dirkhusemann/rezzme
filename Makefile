PYUIC	= pyuic4
PYRCC	= pyrcc4
EXPAND  = python ./expand.py

.PHONY: clean build deploy all

-include Makefile.local

all: build deploy

clean:
	rm -rf dist build dist_win32
	rm -rf rezzme*.dmg
	rm -rf RezzMe/resources.py
	rm -rf RezzMe/config/config.py
	make -C RezzMe/ui clean

build: resources rezzme.ico RezzMe/config/config.py
	make -C RezzMe/ui all
	python ./build.py

deploy:
	python ./deploy.py

RezzMe/config/config.py: rezzme.cfg rezzme-site.cfg
	python ./config.py RezzMe/config/config.py

about.html : about.raw.html rezzme.cfg
	${EXPAND} $< $@

resources: rezzme.png about.html rezzme.qrc 
	${PYRCC} -o RezzMe/resources.py rezzme.qrc
