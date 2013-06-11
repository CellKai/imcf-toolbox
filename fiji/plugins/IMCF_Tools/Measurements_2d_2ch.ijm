if (nImages < 2) {
    msg = "Requires at least 2 open images.";
    showMessage("Error", msg);
    exit;
}

// print("number of images: " + nImages);
names = newArray(nImages);
for (i=0; i < nImages; i++){
    selectImage(i+1);
    names[i] = getTitle();
    // print(names[i]);
}

// sort the names array so we can try to pre-assign the correct
// channels (given the files are named in a sensible way)
Array.sort(names);

// ***** USER INPUT DIALOG ***** //
Dialog.create("Thresholded Measurements / 2Ch, single slices");
msg = "Assign images to channels:";
Dialog.addMessage(msg);
Dialog.addChoice("red channel:", names, names[0]);
Dialog.addChoice("green channel:", names, names[1]);
// threshold method selection
methods = getList("threshold.methods");
Dialog.addChoice("threshold method:", methods, "RenyiEntropy");
Dialog.addNumber("size min: ", 100);
Dialog.addNumber("size max (0 for infinity): ", 0);
Dialog.addSlider("circularity min:", 0, 1, 0.5);
Dialog.addSlider("circularity max:", 0, 1, 1);
Dialog.show();


ch_red = Dialog.getChoice();
ch_grn = Dialog.getChoice();
thr_method = Dialog.getChoice();
size_min = Dialog.getNumber();
size_max = Dialog.getNumber();
if(size_max == 0)
    size_max = "Infinity";
circ_min = Dialog.getNumber();
circ_max = Dialog.getNumber();
// ***** USER INPUT DIALOG ***** //

/*
print(ch_red);
print(ch_grn);
print(size_min);
print(size_max);
print(circ_min);
print(circ_max);
*/

setBatchMode(true);
// make sure the ROI Manager is empty
roiManager("reset");

// duplicate the red channel to create the mask
selectImage(ch_red);
run("Duplicate...", "title=masking_channel");
selectImage("masking_channel");
setAutoThreshold(thr_method + " dark");
// setOption("BlackBackground", false);
run("Convert to Mask");
run("Fill Holes");
run("Watershed");
run("Analyze Particles...",
    "size=" + size_min + "-" + size_max + " pixel"
    + " circularity=" + circ_min + "-" + circ_max
    + " show=Nothing exclude clear add");
//close();

selectImage(names[0]);
roiManager("Show None");
roiManager("Show All");
run("Set Measurements...", "area mean min "
	+ " redirect=" + names[0]
	+ " decimal=10");
roiManager("Measure");
IJ.renameResults("Results-" + names[0]);

selectImage(names[1]);
roiManager("Show None");
roiManager("Show All");
run("Set Measurements...", "area mean min "
	+ " redirect=" + names[1]
	+ " decimal=10");
roiManager("Measure");
IJ.renameResults("Results-" + names[1]);

setBatchMode(false);