importClass(Packages.ij.IJ);

imp = IJ.getImage();
IJ.run(imp, "8-bit", "");
IJ.run(imp, "Auto Local Threshold", "method=Phansalkar radius=30 parameter_1=0 parameter_2=0");
IJ.run(imp, "Watershed", "");
IJ.run(imp, "Analyze Particles...", "size=50-Infinity circularity=0.60-1.00 exclude clear add in_situ");
