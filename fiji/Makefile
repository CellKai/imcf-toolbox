.PHONY: all

DIRS = action_bars tools libs ijm_templates

# process all dirs specified above:
all:
	@ for i in $(DIRS); do make --directory $$i; done

clean:
	@ rm -rv dist/
