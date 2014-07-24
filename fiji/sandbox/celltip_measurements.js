importClass(Packages.ij.IJ);
importClass(Packages.ij.plugin.frame.RoiManager);

imp = IJ.getImage();
name = imp.title;

rm = RoiManager.getInstance();
if (rm==null) rm = new RoiManager();
IJ.run(imp, "Split Channels", "");

imp = WindowManager.getImage("C1-" + name);
imp.close();

imp1 = WindowManager.getImage("C2-" + name);
imp2 = WindowManager.getImage("C3-" + name);

ic = new ImageCalculator();
imp3 = ic.run("Add create stack", imp1, imp2);
imp3.show();

IJ.run(imp3, "Median...", "radius=1.3 stack");
Prefs.blackBackground = true;
IJ.setAutoThreshold(imp3, "IJ_IsoData dark");
IJ.run(imp3, "Convert to Mask", "method=IJ_IsoData background=Dark black");

/*
IJ.run("Close");
//IJ.run("Threshold...");
IJ.resetThreshold(imp);
IJ.resetThreshold(imp);
IJ.resetThreshold(imp);
IJ.run("Close");
*/

IJ.run("Set Measurements...", "area mean min center integrated redirect=None decimal=0");
IJ.run(imp3, "Analyze Particles...", "size=25-Infinity pixel exclude clear include add slice");
//IJ.run(imp, "Measure", "");
IJ.selectWindow("C3-" + name);
rm.runCommand("Measure");

