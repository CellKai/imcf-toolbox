PKGLIST = $(wildcard *.lst)

SCRIPTS = $(wildcard *.py)
CLASSES = $(subst .java,.class,$(wildcard *.java))
CONF = plugins.config

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))

all: msg_01 $(CLASSES) msg_02 $(JAR) msg_03

clean:
	@ rm -vf $(CLASSES)

msg_01:
	@ echo '================= $(JAR) ================='
	@ echo '++++++++++ compiling plugin wrappers ++++++++++'

msg_02:
	@ echo '---------- compiling plugin wrappers ----------'
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'

msg_03:
	@ echo '------------- assembling JAR file -------------'
	@ echo '================= $(JAR) ================='

# compile the plugin wrappers
%.class: %.java %.py
	fiji-linux64 --javac $<

# NOTE: $(@D) references the directory part of a target

# create the JAR file
$(JAR): $(SCRIPTS) $(CLASSES) $(CONF) $(PKGLIST)
	@ mkdir -pv $(@D)
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))

