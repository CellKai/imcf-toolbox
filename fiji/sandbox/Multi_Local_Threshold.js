importClass(Packages.ij.IJ);
//importClass(Packages.ij.gui.GenericDialog);

imp = IJ.getImage();
IJ.run(imp, "8-bit", "");
for (i=10; i<=50; i+=10) {
	IJ.run(imp, "Auto Local Threshold",
		"method=[Try all] radius=" + i +
		" parameter_1=0 parameter_2=0");
	imp_new = IJ.getImage();
	imp_new.setTitle(i);
}
