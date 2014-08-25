Adding a new plugin to this package
===================================

* Open the plugin script in Fiji's script editor unless it is Java code.
* Use File > Export as .jar
* Extract the .java file from the generated .jar file (unzip).
* Add it to this directory.
* Edit "plugins.config" accordingly to have the new plugin show up in ImageJ's
  "Plugin" menu structure with the desired name.

Headless Operation
==================

To use headless operation mode on those plugins that are prepared for it (e.g.
the `FluoView_OIF_Stitcher.py`) use a command like this one (mind the TRIPLE
dash for plugin parameters like `mosaiclog`!):
```
./ImageJ-linux64 --headless /path/to/FluoView_OIF_Stitcher.py \
    ---mosaiclog /some/oif_dataset/MATL_Mosaic.log
```

Testing with the Jython Console
===============================

To test scripts and modules, the Jython Console is a very helpful tool. For
importing custom packages, the path needs to be extended.


```
import sys
imcftb = '/opt/imcf_toolbox/'
sys.path.insert(0, imcftb + 'fiji/tools')
sys.path.insert(0, imcftb + 'fiji/libs/src')
```

Then you can import and run the FluoView Stitcher:
```
import FluoView_OIF_Stitcher as st

st.main_interactive()
```

For running the mosaic parser directly, use this:
```
from microscopy import fluoview
from microscopy import imagej
(base, fname) = st.ui_get_input_file()
mosaic = fluoview.FluoViewOIFMosaic(base + fname)
```

To make the default log messages go to the ImageJ log window, use the custom
logging handler provided in the 'ijpy' module:
```
from log import log
import ijpy
ijlogger = ijpy.IJLogHandler()
log.addHandler(ijlogger)
log.warn('oooomph!')
```
