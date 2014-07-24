/* TODO:
 *  - measure both channels
 *  - pick the z-slice with the slider before running the macro
 *  - save results and ROIs into files
 */

importClass(Packages.ij.IJ);
importClass(Packages.ij.Prefs);
importClass(Packages.ij.WindowManager);
importClass(Packages.ij.plugin.ImageCalculator);
importClass(Packages.ij.plugin.frame.RoiManager);

imp = IJ.getImage();
name = imp.title;
IJ.log(name);

/*
cs = new ChannelSplitter();
channels = cs.split(imp);
//channels[0]
//imp[C1-140328-AtT20-3-V-ACTH-30-60-30.lsm (1024x1024x1x23x1)]
channels[0].show();
*/

IJ.run(imp, "Split Channels", "");

imp = WindowManager.getImage("C1-" + name);
imp.close();

imp1 = WindowManager.getImage("C2-" + name);
imp2 = WindowManager.getImage("C3-" + name);

ic = new ImageCalculator();
imp3 = ic.run("Add create stack", imp1, imp2);
imp3.show();

z_slice = 9;
imp1.setZ(z_slice);
imp2.setZ(z_slice);
imp3.setZ(z_slice);

IJ.run(imp3, "Median...", "radius=1.3 stack");
Prefs.blackBackground = true;
IJ.setAutoThreshold(imp3, "IJ_IsoData dark");
IJ.run(imp3, "Convert to Mask", "method=IJ_IsoData background=Dark black");


IJ.run("Set Measurements...", "area mean min center integrated redirect=None decimal=0");
IJ.run(imp3, "Analyze Particles...", "size=25-Infinity pixel exclude clear include add slice");
IJ.selectWindow("C3-" + name);

rm = RoiManager.getInstance();
if (rm==null) rm = new RoiManager();
rm.runCommand("Measure");

