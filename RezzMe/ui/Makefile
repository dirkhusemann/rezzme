PYUIC	= pyuic4
TARGETS = $(patsubst %.ui,%.py,$(wildcard *.ui))

all: ${TARGETS}

clean:
	rm -f ${TARGETS}

debug:
	@echo "targets: " ${TARGETS}

%.py : %.ui
	${PYUIC} $< --output=$@ 
