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

Testing with the Jython Console
===============================

To test scripts and modules, the Jython Console is a very helpful tool. For
importing custom packages, the path needs to be extended. The following example
does this for the FluoView Stitcher:

```
import sys
imcftb = '/full/path/to/imcf_toolbox/'
sys.path.insert(0, imcftb + 'fiji/tools')
sys.path.insert(0, imcftb + 'lib/python2.7/volpy')
sys.path.insert(0, imcftb + 'lib/python2.7')

import FluoView_OIF_Stitcher as st
import fluoview as fv
(base, fname) = st.ui_get_input_file()
mosaic = fv.FluoViewMosaic(base + fname)
```
