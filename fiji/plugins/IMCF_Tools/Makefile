# Makefile to compile all plugin wrappers.

CLASSES = *.class

all: $(CLASSES)

%.class: %.java %.py
	fiji-linux64 --javac $<
