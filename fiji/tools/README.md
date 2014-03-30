Adding a new plugin to this package
===================================

* Open the plugin script in Fiji's script editor unless it is Java code.
* Use File > Export as .jar
* Extract the .java file from the generated .jar file (unzip).
* Add it to this directory.
* Edit "plugins.config" accordingly to have the new plugin show up in ImageJ's
  "Plugin" menu structure with the desired name.

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
