import os
from loci.plugins.util import BFVirtualStack, ImageProcessorReader

print '---------------------------------------------------------------------------------------'
base = '/scratch/imageproc/data/paolo/FluoView_stitching/oib_format/TVA4vglut2_n2_4X_20140126_234209'
infile = 'Slide1sec001/Slide1sec001_01.oib'
path = os.path.join(base, infile)
#print 'file: %s' % path

irdr = ImageProcessorReader()
irdr.setId(path)

bf = BFVirtualStack(path, irdr, False, False, False)
print 'Successfully created virtual stack.'

width = bf.getWidth()
height = bf.getHeight()
size = bf.getSize()
procreader = bf.getReader()
# meta = procreader.getMetadata()
# print meta
absposx = procreader.getMetadataValue('AbsPositionValueX')
absposy = procreader.getMetadataValue('AbsPositionValueY')
print 'Dimensions (x, y, size): %s, %s, %s' % (width, height, size)
print 'Absolute positions: %s, %s' % (absposx, absposy)