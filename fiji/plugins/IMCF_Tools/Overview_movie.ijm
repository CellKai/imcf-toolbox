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

function update_focus_close_old(title) {
    curfocus = getTitle();
    selectWindow(title);
    close();
    selectWindow(curfocus);
    return curfocus;
}

function mk_overview_movie(infile, stepping, mip, slice) {
    // assemble the Bio-Formats options in advance as the string gets very long
    bf_options =  " color_mode=Composite specify_range stack_order=XYCZT";
    if (!mip) {
        bf_options += " z_begin=" + slice + " z_end=" + slice;
    }
    bf_options += " t_begin=1 t_step=" + stepping;
    // print(bf_options);
    setBatchMode(true);
    run("Bio-Formats Importer", "open=" + infile + bf_options);
    focused = getTitle();

    if (mip) {
        run("Z Project...", "projection=[Max Intensity] all");
        focused = update_focus_close_old(focused);
    }

    // "create" is required, otherwise "scale" adds black borders
    run("Scale...", "x=0.5 y=0.5 interpolation=Bilinear average create");
    focused = update_focus_close_old(focused);
    getDimensions(im_width, im_height, im_channels, im_slices, im_frames);
    // channels numbers start with 1
    for (c=1; c<=im_channels; c++) {
        Stack.setChannel(c);
        run("Enhance Contrast", "saturated=0.35");
    }
    run("RGB Color", "frames");
    run("AVI... ", "compression=JPEG frame=5");
    // disable the close() call if the result should get displayed after the macro
    // terminates
    close();
    setBatchMode(false);
}
