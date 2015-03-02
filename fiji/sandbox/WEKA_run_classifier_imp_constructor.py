import os
from timeit import default_timer as timer
from trainableSegmentation import WekaSegmentation
from ij import IJ

indir = "/scratch/data/__TESTFILES/weka"
infile = os.path.join(indir, "1462_mko_ctx_1.tif")
modelfile = os.path.join(indir, "tissue_fibrotic_bg.model")

input_image = IJ.openImage(infile)
segmentator = WekaSegmentation(input_image)
segmentator.loadClassifier(modelfile)
### Field of view: max sigma = 16.0, min sigma = 0.0
### Membrane thickness: 1, patch size: 19
### Read class name: tissue
### Read class name: fibrotic
### Read class name: bg

segmentator.enabledFeatures
### array('z', [True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False])

segmentator.getClassLabel(0)
### u'tissue'

segmentator.getClassLabel(1)
### u'fibrotic'

segmentator.getClassLabel(2)
### u'bg'

result = segmentator.applyClassifier(input_image, 0, True)
### Processing slices of 1462_mko_ctx_1.tif in 1 thread(s)...
### Starting thread 0 processing 1 slices, starting with 1
### Creating features for slice 1...
### Filtering feature stack by selected attributes...
### Classifying slice 1 in 4 thread(s)...
### Classifying whole image data took: 4724ms

