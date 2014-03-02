PKGLIST = $(wildcard *.lst)

BARS = $(wildcard bars/*.ijm)
ICONS = $(wildcard icons/*)
CONF = plugins.config

BARS_AUTORUN = $(wildcard macros/*.ijm)

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))
AUTO = $(DIST)/macros/AutoRun/imcf_toolbar.ijm

# NOTE: $(@D) references the directory part of a target

all: $(JAR) $(AUTO)

# copy autostart macro(s)
$(AUTO): $(BARS_AUTORUN)
	@ mkdir -pv $(@D)
	cp -v $(BARS_AUTORUN) $(AUTO)

# create the JAR file
$(JAR): $(BARS) $(ICONS) $(CONF) $(PKGLIST)
	@ mkdir -pv $(@D)
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))
	@ echo '------------- assembling JAR file -------------'
