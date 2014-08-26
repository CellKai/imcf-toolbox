.PHONY: all

DIRS = action_bars auto_run libs macros scripts tools

# process all dirs specified above:
all:
	@ for i in $(DIRS); do make --directory $$i; done

clean:
	@ for i in $(DIRS); do make --directory $$i clean; done
	@ rm -rvf dist/
