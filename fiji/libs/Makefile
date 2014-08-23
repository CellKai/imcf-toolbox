FIJI = $(shell cat fijipath)
JAVA = $(FIJI)/java/linux-amd64/jdk1.6.0_24/jre/bin/java
JYTHON = $(FIJI)/jars/jython-2.7-b1.jar

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/imcf_libs.jar


.PHONY: $(JAR)

all: head update_ver build $(JAR) tail

clean:
	rm -v $(JAR)

head:
	@ echo '================= $(JAR) ================='

tail:
	@ echo '================= $(JAR) ================='

update_ver:
	@ echo
	@ echo '+++++++++++++ updating version file +++++++++++++'
	./update_imcf_version.sh
	@ echo '------------- updating version file -------------'
build:
	@ echo '++++++++++ compiling jython bytecode ++++++++++'
	$(JAVA) -jar $(JYTHON) build.py
	@ echo '---------- compiling jython bytecode ----------'

# create the JAR file
$(JAR):
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'
	cd src ; zip -9 -r ../$(JAR) . --include '*.class'
	@ echo '------------- assembling JAR file -------------'
