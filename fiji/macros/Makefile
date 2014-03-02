PKGLIST = $(wildcard *.lst)

SCRIPTS = $(wildcard *.ijm)
CLASSES = $(subst .java,.class,$(wildcard *.java))
CONF = plugins.config

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))

# NOTE: $(@D) references the directory part of a target

all: $(CLASSES) $(JAR)

clean:
	@ rm -vf $(CLASSES)

# compile the plugin wrappers
%.class: %.java %.ijm
	@ echo
	@ echo '++++++++++ compiling plugin wrappers ++++++++++'
	fiji-linux64 --javac $<
	@ echo '---------- compiling plugin wrappers ----------'

# create the JAR file
$(JAR): $(SCRIPTS) $(CLASSES) $(CONF) $(PKGLIST)
	@ mkdir -pv $(@D)
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))
	@ echo '------------- assembling JAR file -------------'

