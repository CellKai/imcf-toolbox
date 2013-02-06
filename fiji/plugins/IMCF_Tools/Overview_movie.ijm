/* currently this macro just asks for a file, opens this file via the
 * Bio-Formats reader, only using a selected slice and a given stepping, then
 * scales it to half its size, runs the auto-contrast for each channel,
 * converts it to RGB and finally stores it as a JPEG-compressed avi
 */

/*
Dialog.create("input dialog");
Dialog.addMessage("my description");
Dialog.addNumber("value 1:", 0);
Dialog.addNumber("value 2:", 0);
Dialog.addCheckbox("really?", true);
Dialog.show;
val1 = Dialog.getNumber();
val2 = Dialog.getNumber();
really = Dialog.getCheckbox();
*/

infile = File.openDialog("Select file");

// exit cleanly if the user clicks on cancel:
if (infile == '') {
    exit;
}

msg = "Set the step size for creating the movie:";
stepping = getNumber(msg, 10);

msg = "Use Maximum Intensity Projection for stacks?";
mip = getBoolean(msg);
if (!mip) {
	msg = "Set slice number to use for the movie:";
	slice = getNumber(msg, 15);
} else {
	slice = 0;
}

mk_overview_movie(infile, stepping, mip, slice);

function mk_overview_movie(infile, stepping, mip, slice) {
// TODO: add MIP projection code:
// run("Z Project...", "start=1 stop=5 projection=[Max Intensity] all");
// assemble the Bio-Formats options in advance as the string gets very long
bf_options =  " color_mode=Composite specify_range stack_order=XYCZT";
bf_options += " z_begin=" + slice + " z_end=" + slice;
bf_options += " t_begin=1 t_step=" + stepping;
setBatchMode(true);
run("Bio-Formats Importer", "open=" + infile + bf_options);
origname = getTitle();
// "create" is required, otherwise "scale" adds black borders
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
}
