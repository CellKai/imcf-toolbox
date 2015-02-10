importClass(Packages.ij.IJ);
importClass(Packages.ij.WindowManager);
importClass(Packages.ij.io.FileSaver);
importClass(Packages.java.io.File);

var dir = '/home/ehrenfeu/imageproc/data/fabia_morgane/BI19/';
files = File(dir).list();

for (var i = 0; i < files.length; i++) {
    print(files[i]);
    imp = IJ.openImage(dir + files[i]);
	imp.show();
	IJ.run(imp,  "Split Channels", "");
	ids = WindowManager.getIDList();
	print(ids.length);
   title = imp.getTitle();
	for (var j = 0; j < ids.length; j++) {
		impnew = WindowManager.getImage(ids[j]);
		channel = impnew.getTitle().split("-")[0];
		print(channel);
		File(dir + channel).mkdir();
		FileSaver(impnew.saveAsTiffStack(dir + ch_name + "/" + title);
	}

	break;
}
