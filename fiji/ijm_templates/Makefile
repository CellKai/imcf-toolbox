PKGLIST = $(wildcard *.lst)

# read contents for ZIP (and thus dependencies) from the packagelist:
DEPS = $(shell cat ${PKGLIST})

DIST = ../dist
ZIP = $(DIST)/plugins/IMCF/$(subst .lst,.zip,$(PKGLIST))

# NOTE: $(@D) references the directory part of a target

all: msg_01 $(ZIP) msg_02

clean:
	@ echo 'Nothing to clean here.'

msg_01:
	@ echo '================= $(ZIP) ================='
	@ echo '+++++++++++++ assembling ZIP file +++++++++++++'

msg_02:
	@ echo '------------- assembling ZIP file -------------'
	@ echo '================= $(ZIP) ================='

# create the ZIP file
$(ZIP): $(DEPS) $(PKGLIST)
	@ mkdir -pv $(@D)
	zip -9 -r $(ZIP) . --include @$(subst .zip,.lst,$(@F))

