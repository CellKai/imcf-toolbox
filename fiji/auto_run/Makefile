.PHONY: all

DIRS = $(shell find -mindepth 1 -type d)

# process all dirs specified above:
all:
	@ for i in $(DIRS); do make --directory $$i; done

clean:
	@ for i in $(DIRS); do make --directory $$i clean; done
