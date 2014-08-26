.PHONY: all

DIRS = action_bars tools libs macros

# process all dirs specified above:
all:
	@ for i in $(DIRS); do make --directory $$i; done

clean:
	@ for i in $(DIRS); do make --directory $$i clean; done
	@ rm -rvf dist/
