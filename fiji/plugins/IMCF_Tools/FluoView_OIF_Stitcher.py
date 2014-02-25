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

# set_loglevel(1)

infile = OpenDialog("Choose a 'MATL_Mosaic.log' file", '*.log')
print(infile.getDirectory())
print(infile.getFileName())

# dc = DirectoryChooser("Choose a directory with a 'MATL_Mosaic.log' file")
# base = dc.getDirectory()

mf = base + 'MATL_Mosaic.log'

mosaic = fv.FluoViewMosaic(mf)
mosaic.write_all_tile_configs(fixpath=True)
code = mosaic.gen_stitching_macro_code('stitching', base)
flat = ""
for line in code:
	flat += line

#print flat
IJ.runMacro(flat)
