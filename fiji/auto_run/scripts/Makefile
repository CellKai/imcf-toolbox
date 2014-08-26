SCRIPTS = $(wildcard *.js)

DIST = ../../dist
TGT = $(DIST)/plugins/Scripts/AutoRun

.PHONY: copy

all: head copy tail

clean:
	@ rm -rvf $(TGT)

head:
	@ echo '================= $(TGT) ================='

tail:
	@ echo '================= $(TGT) ================='

# create the JAR file
copy:
	@ mkdir -pv $(TGT)
	@ cp -uv $(SCRIPTS) $(TGT)
