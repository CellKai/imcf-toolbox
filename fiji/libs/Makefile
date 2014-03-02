PKGLIST = $(wildcard *.lst)

# read contents for JAR (and thus dependencies) from the packagelist:
DEPS = $(shell cat ${PKGLIST})

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))

# NOTE: $(@D) references the directory part of a target

all: msg_01 $(JAR) msg_02

clean:
	@ echo 'Nothing to clean here.'

msg_01:
	@ echo '================= $(JAR) ================='
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'

msg_02:
	@ echo '------------- assembling JAR file -------------'
	@ echo '================= $(JAR) ================='

# create the JAR file
$(JAR): $(DEPS) $(PKGLIST)
	@ mkdir -pv $(@D)
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))

