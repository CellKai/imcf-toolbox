// an auto-run script with some sanity checking (which is almost impossible
// with using the macro language

importClass(Packages.ij.IJ);

// make sure we only launch the bar if the ActionBar plugin is installed:
try {
    importClass(Packages.Action_Bar);
    IJ.run("IMCF Default Toolbar", "");
    // print('success');
}
catch(e) {
    // print('fail');
}
