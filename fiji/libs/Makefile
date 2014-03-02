PKGLIST = $(wildcard *.lst)

# read contents for JAR (and thus dependencies) from the packagelist:
DEPS = $(shell cat ${PKGLIST})

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))

# NOTE: $(@D) references the directory part of a target

all: $(JAR)

# create the JAR file
$(JAR): $(DEPS) $(PKGLIST)
	@ mkdir -pv $(@D)
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))
	@ echo '------------- assembling JAR file -------------'

