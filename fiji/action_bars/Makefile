PKGLIST = $(wildcard *.lst)

BARS = $(wildcard bars/*.ijm)
ICONS = $(wildcard icons/*)
CONF = plugins.config

BARS_AUTORUN = ../auto_run/IMCF_AutoRun_Safe.js

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))
AUTO = $(DIST)/plugins/Scripts/AutoRun/IMCF_AutoRun_Safe.js

# NOTE: $(@D) references the directory part of a target

all: msg_01 $(JAR) msg_02 $(AUTO) msg_03

clean:
	@ echo 'Nothing to clean here.'

msg_01:
	@ echo '================= $(JAR) ================='
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'

msg_02:
	@ echo '------------- assembling JAR file -------------'
	@ echo
	@ echo '++++++++++ copying autostart macros ++++++++++'

msg_03:
	@ echo '---------- copying autostart macros ----------'
	@ echo '================= $(JAR) ================='

# copy autostart macro(s)
$(AUTO): $(BARS_AUTORUN)
	@ mkdir -pv $(@D)
	cp -v $(BARS_AUTORUN) $(AUTO)

# create the JAR file
$(JAR): $(BARS) $(ICONS) $(CONF) $(PKGLIST)
	@ mkdir -pv $(@D)
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))
