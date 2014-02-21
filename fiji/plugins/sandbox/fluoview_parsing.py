from ij import IJ
from sys import path
# from java.lang.System import getProperty
 
# extend the search path by $FIJI_ROOT/bin/
path.append('/home/ehrenfeu/.local/lib/python2.7')
path.append('/home/ehrenfeu/.local/lib/python2.7/site-packages/volpy')

import fluoview as fv
from log import log, set_loglevel

set_loglevel(1)

base = '/home/ehrenfeu/usr/packages/imcf_toolbox/sample_data/fluoview/minimal_1mosaic_15pct/'
mf = base + 'MATL_Mosaic.log'

mosaic = fv.FluoViewMosaic(mf)
mosaic.write_all_tile_configs(fixpath=True)
code = mosaic.gen_stitching_macro_code('stitching')
flat = ""
for line in code:
	flat += line

#print flat
IJ.runMacro(flat)
