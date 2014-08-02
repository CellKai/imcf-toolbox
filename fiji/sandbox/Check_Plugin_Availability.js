try {
    importClass(Packages.Action_Bar);
    // print('success');
    IJ.run("IMCF Default Toolbar", "");
}
catch(e) {
    print('fail');
}
