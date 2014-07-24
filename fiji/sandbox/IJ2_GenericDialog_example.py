from ij import IJ
from ij.gui import GenericDialog

gd = GenericDialog("Cells segmentation parameters");
gd.addNumericField("Radius for Local Thresholding", 30.0, 0);
gd.addNumericField("Size minimum for particles", 50.0, 0);
gd.addNumericField("Circularity minimum value", 0.60, 2);
gd.showDialog();

values = gd.getNumericFields();
for val in values:
	IJ.log(val.text)