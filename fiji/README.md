TODO
====

This should rather describe the structure of the subdirectories, e.g. why
macros go into a JAR package that lives somewhere in the "plugins" tree.
Instructions for testing with Jython can go directly into the docstring of the
corresponding scripts themselves.

Packaging
=========

NOTE: The toplevel Makefile requires those sub-trees that should be processed
to be specified explicitly, so if a new directory is created, it has to be
added to the Makefile manually!

The default scenario for the subdirectories is a local Makefile and a file
containing the filename patterns to be used by "zip" for creating the .jar file
in the end. This package-list file has to be named identically to the jar that
it corresponds to except for the filename suffix ".jar" being replaced by
".lst".

Optionally, a "plugins.config" file can be present if the package contains
stuff that should be put into ImageJ's "Plugins" menu structure.

Running _make_ will assemble the required directory structure for Fiji as a
subtree of the "_dist/_" directory
