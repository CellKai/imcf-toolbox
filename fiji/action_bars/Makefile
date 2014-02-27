BARS = bars/*.ijm
ICONS = icons/*
CONF = plugins.config
PKGLIST = imcf_actionbars.lst

BARS_AUTORUN = macros/*.ijm

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/imcf_actionbars.jar
AUTO = $(DIST)/macros/AutoRun/imcf_toolbar.ijm

# NOTE: $(@D) references the directory part of a target

all: $(JAR) $(AUTO)

$(JAR): $(BARS) $(ICONS) $(CONF) $(PKGLIST)
	mkdir -pv $(@D) ; \
	zip -9 -r $(JAR) . --include @imcf_actionbars.lst

$(AUTO): $(BARS_AUTORUN)
	mkdir -pv $(@D) ; \
	cp -v $(BARS_AUTORUN) $(AUTO)
