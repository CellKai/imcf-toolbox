SCRIPTS = $(wildcard *.ijm)

DIST = ../../dist
TGT = $(DIST)/macros/AutoRun

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
