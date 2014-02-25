# TODO: present either a GUI to ask the user about the individual steps
# or allow passing all parameters as arguments for this plugin

# explicitly add our libs to PYTHONPATH
from java.lang.System import getProperty
from os.path import join
import sys.path
imcfpath = join(getProperty('fiji.dir'), 'plugins', 'IMCF', 'libs')
sys.path.append(imcfpath)


import fluoview as fv
from log import log, set_loglevel
from ij import IJ
from ij.io import DirectoryChooser, OpenDialog
import sys

# set_loglevel(1)

log.debug(fv.__file__)

od = OpenDialog("Choose a 'MATL_Mosaic.log' file")
fname = od.getFileName()
if (fname is None):
    sys.exit()
base = od.getDirectory()
mf = base + fname
log.warn(mf)

mosaic = fv.FluoViewMosaic(mf)
# FIXME: ask user where to put the tile configs
mosaic.write_all_tile_configs(fixpath=True)
code = mosaic.gen_stitching_macro_code('stitching', base)
flat = ""
for line in code:
	flat += line

# TODO: ask user how to proceed (show macro, run it, ...)
print flat
#IJ.runMacro(flat)
