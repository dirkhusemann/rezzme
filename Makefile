PYUIC	= pyuic4
PYRCC	= pyrcc4

.PHONY: clean build deploy all

all: build deploy

clean:
	rm -rf dist build dist_win32
	rm -rf rezzme*.dmg
	rm -rf RezzMe/resources.py
	make -C RezzMe/ui clean

build: resources rezzme.ico
	make -C RezzMe/ui all
	python ./build.py

deploy:
	python ./deploy.py


# %.ico : %.png
# 	${CONVERT} $< $@

resources: rezzme.png rezzme.qrc
	${PYRCC} -o RezzMe/resources.py rezzme.qrc
