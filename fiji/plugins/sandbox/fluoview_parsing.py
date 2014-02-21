from ij import IJ
from ij.io import DirectoryChooser
from sys import path
# from java.lang.System import getProperty
 
# extend the search path by $FIJI_ROOT/bin/
path.append('/home/ehrenfeu/.local/lib/python2.7')
path.append('/home/ehrenfeu/.local/lib/python2.7/site-packages/volpy')

import fluoview as fv
from log import log, set_loglevel

set_loglevel(1)

dc = DirectoryChooser("Choose a directory with a 'MATL_Mosaic.log' file")
base = dc.getDirectory()

mf = base + 'MATL_Mosaic.log'

mosaic = fv.FluoViewMosaic(mf)
mosaic.write_all_tile_configs(fixpath=True)
code = mosaic.gen_stitching_macro_code('stitching', base)
flat = ""
for line in code:
	flat += line

#print flat
IJ.runMacro(flat)
