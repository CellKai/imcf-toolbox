from ij import IJ
from ij.io import DirectoryChooser, OpenDialog
# explicitly add our libs to PYTHONPATH
from os.path import join
import sys.path
from java.lang.System import getProperty
imcfpath = join(getProperty('fiji.dir'), 'plugins', 'IMCF', 'libs')
sys.path.append(imcfpath)


import fluoview as fv
from log import log, set_loglevel
import sys

# set_loglevel(1)

log.warn(fv.__file__)

od = OpenDialog("Choose a 'MATL_Mosaic.log' file")
# dc = DirectoryChooser("Choose a directory with a 'MATL_Mosaic.log' file")
# base = dc.getDirectory()
fname = od.getFileName()
if (fname is None):
    sys.exit()
base = od.getDirectory()
mf = base + fname
log.warn(mf)

mosaic = fv.FluoViewMosaic(mf)
mosaic.write_all_tile_configs(fixpath=True)
code = mosaic.gen_stitching_macro_code('stitching', base)
flat = ""
for line in code:
	flat += line

#print flat
IJ.runMacro(flat)
