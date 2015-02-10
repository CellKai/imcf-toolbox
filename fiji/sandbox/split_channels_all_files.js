importClass(Packages.ij.IJ);
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
	//imp.show();
	channels = ChannelSplitter().split(imp);
	for (var j = 0; j < channels.length; j++) {
		ch_name = channels[j].getTitle().split("-")[0];
		//print(ch_name);
		File(dir + ch_name).mkdir();
		print("Writing channel " + ch_name);
		FileSaver(channels[j]).saveAsTiffStack(dir + ch_name + "/" + title);
	}
	break;
}
