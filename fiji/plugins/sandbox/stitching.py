from plugin import Stitching_Grid
from mpicbg.stitching import StitchingParameters

stitcher = Stitching_Grid()
params = StitchingParameters()

cdir = '/scratch/imageproc/data/paolo/FluoView_stitching/sample_experiment/'
cfile = 'TileConfiguration.txt'
cfileout = 'TileConfiguration.registered.txt'

print '-----------------'
for entry in  dir(stitcher):
	print entry
print '-----------------'

# stitcher.run('')
layout = stitcher.getLayoutFromFile(cdir, cfileout, None)

print '-----------------'
for entry in  dir(params):
	print entry

print stitcher.version

print 'success!'