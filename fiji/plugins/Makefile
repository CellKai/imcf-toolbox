.PHONY: wrapper

DIRS = IMCF_Tools
SCRIPTS = $(DIRS)/*.py
MACROS = $(DIRS)/*.ijm
BARS = $(DIRS)/ActionBar/*.ijm
ICONS = $(DIRS)/icons/*
CLASSES = $(DIRS)/*.class
CONF = $(DIRS)/plugins.config

all: wrapper IMCF_Tools.jar

# target to compile the Java wrapper classes for scripts and macros:
wrapper:
	for i in $(DIRS); do make --directory $$i; done

# create the JAR file
IMCF_Tools.jar: $(SCRIPTS) $(MACROS) $(BARS) $(ICONS) $(CLASSES) $(CONF)
	cd IMCF_Tools ; \
	zip -r -9 --exclude Makefile --suffixes .png ../IMCF_Tools.jar *

