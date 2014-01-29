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
print 'finished reading stack'
width = bf.getWidth()
height = bf.getHeight()
size = bf.getSize()
print '%s %s %s' % (width, height, size)
proc = bf.getProcessor(1)
info = proc.toString()
print 'info: %s' % info
procreader = bf.getReader()
# meta = procreader.getMetadata()
# print meta
print procreader.getMetadataValue('AbsPositionValueX')
print procreader.getMetadataValue('AbsPositionValueY')