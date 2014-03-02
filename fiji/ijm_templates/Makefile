PKGLIST = $(wildcard *.lst)

# read contents for ZIP (and thus dependencies) from the packagelist:
DEPS = $(shell cat ${PKGLIST})

DIST = ../dist
ZIP = $(DIST)/plugins/IMCF/$(subst .lst,.zip,$(PKGLIST))

# NOTE: $(@D) references the directory part of a target

all: $(ZIP)

# create the ZIP file
$(ZIP): $(DEPS) $(PKGLIST)
	@ mkdir -pv $(@D)
	@ echo
	@ echo '+++++++++++++ assembling ZIP file +++++++++++++'
	zip -9 -r $(ZIP) . --include @$(subst .zip,.lst,$(@F))
	@ echo '------------- assembling ZIP file -------------'

