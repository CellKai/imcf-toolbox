FIJI = $(shell cat fijipath)
JAVA = $(FIJI)/java/linux-amd64/jdk1.6.0_24/jre/bin/java
JYTHON = $(shell cat jythonpath)/jython-2.7-b1.jar

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/imcf_libs.jar


.PHONY: $(JAR)

all: head build $(JAR) tail

clean:
	@ rm -vf $(JAR)

head:
	@ echo '================= $(JAR) ================='

tail:
	@ echo '================= $(JAR) ================='

build:
	@ echo '++++++++++ compiling jython bytecode ++++++++++'
	$(JAVA) -jar $(JYTHON) build.py
	@ echo '---------- compiling jython bytecode ----------'

# NOTE: $(@D) references the directory part of a target

# create the JAR file
$(JAR):
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'
	@ mkdir -pv $(@D)
	cd src ; zip -9 -r ../$(JAR) . --include '*.class'
	@ echo '------------- assembling JAR file -------------'
