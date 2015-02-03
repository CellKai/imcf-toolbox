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
run("32-bit");
run("Enhance Contrast", "saturated=0 normalize");
run("16-bit");
run("Remove Outliers...", "radius=12 threshold=1 which=Bright");
run("Remove Outliers...", "radius=10 threshold=2 which=Dark");
run("Median...", "radius=5");
run("8-bit");
setThreshold(25, 255);
run("Convert to Mask");
run("Make Binary");
run("Fill Holes");
run("Watershed");
run("Analyze Particles...", "size=45-400 circularity=0.30-1.00 show=[Overlay Outlines] summarize");
}



