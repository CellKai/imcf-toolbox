macro "delete slice current channel [x]" {
run("Delete Slice", "delete=channel");
}

macro "save as tiff [s]" {
saveAs("Tiff");
}

macro "To ROI Manager [d]" {
run("To ROI Manager");
}

macro "From ROI Manager [f]" {
run("From ROI Manager");
}

macro "Nucleus [a]" {
name=getTitle;
run("Duplicate...", "title=" + name +"_forms");
run("Gaussian Blur...", "sigma=7");
setThreshold(0, 16);
run("Convert to Mask");
run("Make Binary");
run("Fill Holes");
run("Watershed");
run("Analyze Particles...", "size=50-400 circularity=0.30-1.00 show=[Overlay Outlines] summarize");
}
