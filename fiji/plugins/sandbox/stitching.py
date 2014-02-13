from plugin import Stitching_Grid
from mpicbg.stitching import StitchingParameters

stitcher = Stitching_Grid()
params = StitchingParameters()

cdir = '/scratch/imageproc/data/paolo/FluoView_stitching/sample_experiment/'
cfile = 'TileConfiguration.txt'

layout = stitcher.getLayoutFromFile(cdir, cfile)
# for entry in  dir(stitcher):
# 	print entry

print '-----------------'
for entry in  dir(params):
	print entry

print stitcher.version

print 'success!'