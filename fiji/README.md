TODO
====

This should rather describe the structure of the subdirectories, e.g. why
macros go into a JAR package that lives somewhere in the "plugins" tree.
Instructions for testing with Jython can go directly into the docstring of the
corresponding scripts themselves.

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
