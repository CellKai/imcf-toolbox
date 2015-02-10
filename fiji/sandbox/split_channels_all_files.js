importClass(Packages.ij.IJ);
importClass(Packages.ij.ImagePlus);
importClass(Packages.ij.process.ImageProcessor);
importClass(Packages.ij.plugin.ChannelSplitter);
importClass(Packages.ij.io.DirectoryChooser);
importClass(Packages.ij.io.FileSaver);
importClass(Packages.java.io.File);

var dir = DirectoryChooser("Select a directory...").getDirectory();
print(dir);

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
		for (var z=1; z<=stack.getSize(); z++) {
			ip = stack.getProcessor(z);
			fname = ch_name + "/" + t_name + "-z" + z + t_suff;
			print("Writing channel " + ch_name + ", slice " + z + ": " + fname);
			FileSaver(ImagePlus(title, ip)).saveAsTiff(dir + fname);
		}
	}
}
