FIJI = $(shell cat fijipath)
JAVA = $(FIJI)/java/linux-amd64/jdk1.6.0_24/jre/bin/java
JYTHON = $(FIJI)/jars/jython-2.7-b1.jar

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/imcf_libs.jar


.PHONY: $(JAR)

all: msg_01 build msg_02 $(JAR) msg_03

clean:
	rm -v $(JAR)

msg_01:
	@ echo '================= $(JAR) ================='
	@ echo '++++++++++ compiling jython bytecode ++++++++++'

msg_02:
	@ echo '---------- compiling jython bytecode ----------'
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'

msg_03:
	@ echo '------------- assembling JAR file -------------'
	@ echo '================= $(JAR) ================='

build:
	$(JAVA) -jar $(JYTHON) build.py

# create the JAR file
$(JAR):
	cd src ; zip -9 -r ../$(JAR) . --include '*.class'
