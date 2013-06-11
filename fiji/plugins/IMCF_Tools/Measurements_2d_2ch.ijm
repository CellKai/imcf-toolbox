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
Dialog.show();


ch_red = Dialog.getChoice();
ch_grn = Dialog.getChoice();
thr_method = Dialog.getChoice();
// ***** USER INPUT DIALOG ***** //

/*
print(ch_red);
print(ch_grn);
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
//close();


/* TODO:
 *  size : 100-infinity
 *  circularity: 0.5-1
 */

setBatchMode(false);