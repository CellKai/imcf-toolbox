importClass(Packages.ij.IJ);
importClass(Packages.ij.gui.GenericDialog);

gd = new GenericDialog("Cells segmentation parameters");
//gd.addMessage("Binary Reconstruction v 2");
gd.addNumericField("Radius for Local Thresholding", 30.0, 0);
gd.addNumericField("Size minimum for particles", 50.0, 0);
gd.addNumericField("Circularity minimum value", 0.60, 2);
gd.showDialog();

values = gd.getNumericFields();
IJ.log("using firstElement()");
IJ.log(values.firstElement().text);
IJ.log("using getNextNumber()");
IJ.log(gd.getNextNumber());
IJ.log(gd.getNextNumber());
IJ.log(gd.getNextNumber());