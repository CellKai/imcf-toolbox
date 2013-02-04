/* currently this macro just asks for a file, opens this file via the
 * bio-formats reader, only using a selected slice and a given stepping, then
 * scales it to half its size, runs the auto-contrast for each channel,
 * converts it to RGB and finally stores it as a JPEG-compressed avi
 */

infile = File.openDialog("Select file");

// exit cleanly if the user clicks on cancel:
if (infile == '') {
    exit;
}

// this should be asked via a dialog:
slice=15;
stepping=10;

// assemble the Bio-Formats options in advance as the string gets very long
bf_options=" color_mode=Composite specify_range stack_order=XYCZT";
bf_options+=" z_begin=" + slice + " z_end=" + slice + " t_begin=1 t_step=" + stepping;
setBatchMode(true);
run("Bio-Formats Importer", "open=" + infile + bf_options);
origname = getTitle();
// note: "create" is required, otherwise we get black borders
run("Scale...", "x=0.5 y=0.5 interpolation=Bilinear average create");
getDimensions(im_width, im_height, im_channels, im_slices, im_frames);
// channels numbers start with 1
for (c=1; c<=im_channels; c++) {
    Stack.setChannel(c);
    run("Enhance Contrast", "saturated=0.35");
}
//selectWindow("reduced_size_overview.tif");
run("RGB Color", "frames");
run("AVI... ", "compression=JPEG frame=5");
// disable the close() call if the result should get displayed after the macro
// terminates
close();
selectWindow(origname);
close();
setBatchMode(false);

