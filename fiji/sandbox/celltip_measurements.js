/* TODO:
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

imp_c1 = WindowManager.getImage("C1-" + name);
imp_c2 = WindowManager.getImage("C2-" + name);
imp_c3 = WindowManager.getImage("C3-" + name);

ic = new ImageCalculator();
imp_combined = ic.run("Add create stack", imp_c2, imp_c3);
imp_combined.show();
imp_combined.setZ(z_slice);

IJ.run(imp_combined, "Median...", "radius=1.3 stack");
Prefs.blackBackground = true;
IJ.setAutoThreshold(imp_combined, "IJ_IsoData dark");
IJ.run(imp_combined, "Convert to Mask", "method=IJ_IsoData background=Dark black");


IJ.run("Set Measurements...", "area mean min center integrated redirect=None decimal=0");
IJ.run(imp_combined, "Analyze Particles...", "size=25-Infinity pixel exclude clear include add slice");

// prepare the ROI Manager
rm = RoiManager.getInstance();
if (rm==null) rm = new RoiManager();


function measure_save(imp) {
	WindowManager.setCurrentWindow(imp.getWindow())
	rm.runCommand("Measure");
	rt = ResultsTable.getResultsTable();
	rtw = ResultsTable.getResultsWindow();
	rtw.rename('Results ' + imp.shortTitle);
	
	sd = new SaveDialog('Save measurement results as...',
		imp.shortTitle + "_z" + z_slice + "_results", ".csv");
	fout = sd.getFileName();
	if (fout != null) {
		fout = sd.getDirectory() + fout;
		rt.saveAs(fout);
	}
}

measure_save(imp_c2);
measure_save(imp_c3);
