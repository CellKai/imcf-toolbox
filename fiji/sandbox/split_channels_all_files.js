importClass(Packages.ij.IJ);
importClass(Packages.ij.ImagePlus);
importClass(Packages.ij.gui.GenericDialog);
importClass(Packages.ij.io.DirectoryChooser);
importClass(Packages.ij.io.FileSaver);
importClass(Packages.ij.process.ImageProcessor);
importClass(Packages.ij.plugin.ChannelSplitter);
importClass(Packages.java.io.File);

var dir = DirectoryChooser("Select a directory...").getDirectory();
print(dir);
gd = new GenericDialog("Skip slices");
gd.addNumericField("Skip slices at top", 0, 0);
gd.addNumericField("Skip slices at bottom", 0, 0);
gd.showDialog();
skip_t = gd.getNextNumber();
skip_b = gd.getNextNumber();
//IJ.log(skip_t + " " + skip_b);
//print(foo);

files = File(dir).list();
for (var i = 0; i < files.length; i++) {
    print("Processing file " + files[i]);
    imp = IJ.openImage(dir + files[i]);
    title = imp.getTitle();
    splitpos = title.lastIndexOf(".");
    if (splitpos === -1) {
		t_name = title;
		t_suff = "";
    } else {
		t_name = title.substr(0, splitpos);
		t_suff = title.substr(splitpos, title.length());
    }
	channels = ChannelSplitter().split(imp);
	for (var j = 0; j < channels.length; j++) {
		ch_name = channels[j].getTitle().split("-")[0];
		File(dir + ch_name).mkdir();
		stack = channels[j].getStack();
		z_start = 1 + skip_t;
		z_stop  = stack.getSize() - skip_b;
		for (var z=z_start; z<=z_stop; z++) {
			ip = stack.getProcessor(z);
			fname = ch_name + "/" + t_name + "-z" + z + t_suff;
			print("Writing channel " + ch_name + ", slice " + z + ": " + fname);
			FileSaver(ImagePlus(title, ip)).saveAsTiff(dir + fname);
		}
	}
}
