SCRIPTS = $(wildcard *.js)

DIST = ../dist
TGT = $(DIST)/plugins/Scripts/Plugins/IMCF_Utilities/

.PHONY: copy

all: head copy tail

clean:
	@ rm -rvf $(TGT)/*

head:
	@ echo '================= $(TGT) ================='

tail:
	@ echo '================= $(TGT) ================='

copy:
	@ mkdir -pv $(TGT)
	@ cp -uv $(SCRIPTS) $(TGT)
