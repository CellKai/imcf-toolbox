import os
from timeit import default_timer as timer
from trainableSegmentation import WekaSegmentation
from ij import IJ

indir = "/scratch/data/__TESTFILES/weka"
# modelfile = os.path.join(indir, "bg_vs_tissue.model")
modelfile = os.path.join(indir, "tissue_fibrotic_bg.model")
infile = os.path.join(indir, "1462_mko_ctx_1.tif")

input_image = IJ.openImage(infile)

segmentator = WekaSegmentation(input_image)
# segmentator = WekaSegmentation()
IJ.log("Loading classifier...")
t_start = timer()
segmentator.loadClassifier(modelfile)
t_end = timer()
IJ.log("Loading classifier completed (%.2fs)." % (t_end - t_start))

for root, directories, filenames in os.walk(indir):
    for filename in filenames:
      # Skip non-TIFF files
      if not filename.endswith(".tif"):
        continue
      path = os.path.join(root, filename)
      IJ.log("Classifying %s..." % path)
      input_image = IJ.openImage(path)
      result = segmentator.applyClassifier(input_image, 0, True)
      IJ.log("Finished classification, saving results...")
      IJ.save(result, path + "_result.tif")
      IJ.log("Saved results as '%s'." % path + "_result.tif")
      input_image.close()
      result.close()
