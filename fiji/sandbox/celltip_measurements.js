/* TODO:
 *  - use proper imp# names
 *  - use ChannelSplitter() etc.?
 */

importClass(Packages.ij.IJ);
importClass(Packages.ij.Prefs);
importClass(Packages.ij.WindowManager);
importClass(Packages.ij.io.SaveDialog);
importClass(Packages.ij.plugin.ImageCalculator);
importClass(Packages.ij.plugin.frame.RoiManager);
importClass(Packages.ij.plugin.filter.ParticleAnalyzer);
importClass(Packages.ij.measure.ResultsTable);
importClass(Packages.ij.measure.Measurements);


imp = IJ.getImage();
name = imp.title;
z_slice = imp.z;  // remember the z-position

/*
cs = new ChannelSplitter();
channels = cs.split(imp);
//channels[0]
//imp[C1-140328-AtT20-3-V-ACTH-30-60-30.lsm (1024x1024x1x23x1)]
//channels[0].show();
ic = new ImageCalculator();
combined = ic.run("Add create stack", channels[1], channels[2]);
*/

IJ.run(imp, "Split Channels", "");

imp = WindowManager.getImage("C1-" + name);
//imp.close();

imp1 = WindowManager.getImage("C2-" + name);
imp2 = WindowManager.getImage("C3-" + name);

ic = new ImageCalculator();
imp3 = ic.run("Add create stack", imp1, imp2);
imp3.show();

imp1.setZ(z_slice);
imp2.setZ(z_slice);
imp3.setZ(z_slice);

IJ.run(imp3, "Median...", "radius=1.3 stack");
Prefs.blackBackground = true;
IJ.setAutoThreshold(imp3, "IJ_IsoData dark");
IJ.run(imp3, "Convert to Mask", "method=IJ_IsoData background=Dark black");


IJ.run("Set Measurements...", "area mean min center integrated redirect=None decimal=0");
IJ.run(imp3, "Analyze Particles...", "size=25-Infinity pixel exclude clear include add slice");

// prepare the ROI Manager
rm = RoiManager.getInstance();
if (rm==null) rm = new RoiManager();

// channel 3 measuring and saving
IJ.selectWindow("C3-" + name);
rm.runCommand("Measure");
rt = ResultsTable.getResultsTable();
rtw = ResultsTable.getResultsWindow();
rtw.rename('Results ' + imp2.shortTitle);

sd = new SaveDialog('Save measurement results as...', imp2.shortTitle + "_results", ".csv");
fout = sd.getFileName();
if (fout != null) {
	fout = sd.getDirectory() + fout;
	rt.saveAs(fout);
}

// channel 2 measuring and saving
IJ.selectWindow("C2-" + name);
rm.runCommand("Measure");
rt = ResultsTable.getResultsTable();
rtw = ResultsTable.getResultsWindow();
rtw.rename('Results ' + imp1.shortTitle);

sd = new SaveDialog('Save measurement results as...', imp1.shortTitle + "_results", ".csv");
fout = sd.getFileName();
if (fout != null) {
	fout = sd.getDirectory() + fout;
	rt.saveAs(fout);
}