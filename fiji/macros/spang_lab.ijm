/*
 * ImageJ macro for Spang Lab segmentation, 2014-03.
 *
 * Asks the user in a dialog to select one image for processing, select the
 * desired thresholding method and the filtering values for size and
 * circularity that that are passed to "Analyze Particles" later.
 *
 */


if (nImages < 1) {
    msg = "Please open one image before running the macro!";
    showMessage("Error", msg);
    exit;
}

// assemble an array containing the currently open images:
// print("number of images: " + nImages);
setBatchMode(true);
names = newArray(nImages);
for (i=0; i < nImages; i++){
    selectImage(i+1);
    names[i] = getTitle();
}
// sort the names array so we can try to pre-assign the correct
// channels (given the files are named in a sensible way)
Array.sort(names);
setBatchMode(false);


// ***** USER INPUT DIALOG ***** //
Dialog.create("Cells segmentation parameters");
msg = "Assign images to channels:";
//Dialog.addMessage(msg);
Dialog.addChoice("Select image to use for SEGMENTATION:", names, names[0]);
Dialog.addNumber("CLAHE slope maximum: ", 4);
// threshold method selection (FIXME: complete the list!)
methods = newArray('Phansalkar', 'Niblack', 'Otsu', 'Mean', 'Median');
Dialog.addChoice("Local Thresholding method:", methods, "Phansalkar");
Dialog.addSlider("Local Thresholding radius:", 5, 50, 15);
Dialog.addNumber("Object size minimum: ", 50);
Dialog.addNumber("Object size maximum (0 for infinity): ", 0);
Dialog.addSlider("Circularity minimum:", 0, 1, 0.5);
Dialog.addSlider("Circularity maximum:", 0.1, 1, 1);
Dialog.show();


ch_segm = Dialog.getChoice();
clahe_max = Dialog.getNumber();
thr_method = Dialog.getChoice();
thr_radius = Dialog.getNumber();
size_min = Dialog.getNumber();
size_max = Dialog.getNumber();
if(size_max == 0)
    size_max = "Infinity";
circ_min = Dialog.getNumber();
circ_max = Dialog.getNumber();
// ***** USER INPUT DIALOG ***** //

setBatchMode(true);
// make sure the ROI Manager is empty
roiManager("reset");
// make sure nothing is selected
run("Select None");

// duplicate the red channel to create the mask
selectImage(ch_segm);
run("Duplicate...", "title=masking_channel");
selectImage("masking_channel");
//run("Enhance Contrast", "saturated=5.0");
run("Enhance Local Contrast (CLAHE)",
	"blocksize=127 histogram=256 maximum=&clahe_max "
	+ "mask=*None* fast_(less_accurate)");
run("8-bit");  // local threshold only works on 8-bit images
run("Auto Local Threshold", "method=&thr_method radius=&thr_radius "
    + "parameter_1=0 parameter_2=0 white");
// setOption("BlackBackground", false);
run("Convert to Mask");
run("Fill Holes");
run("Open");
run("Watershed");
run("Analyze Particles...",
    "size=&size_min-&size_max pixel circularity=&circ_min-&circ_max"
    + " show=Nothing exclude clear add");
selectImage("masking_channel");
close(); // not required in batch mode
selectImage(ch_segm);
roiManager("Show All");


setBatchMode(false);
