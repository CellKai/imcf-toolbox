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
run("Set Measurements...", "area redirect=None decimal=3");
run("Measure");
run("Make Inverse");
run("Fill", "slice");
run("Next Slice [>]");
run("Fill", "slice");
run("Previous Slice [<]");
run("Make Composite");
run("Stack to RGB");
run("16-bit");
run("Remove Outliers...", "radius=12 threshold=1 which=Bright");
run("Remove Outliers...", "radius=10 threshold=2 which=Dark");
run("Median...", "radius=7");
run("Subtract...", "value=20");
run("8-bit");
run("Auto Local Threshold", "method=Niblack radius=55 parameter_1=0 parameter_2=0 white");
run("Make Binary");
run("Watershed");
run("Analyze Particles...", "size=20-150 circularity=0.30-1.00 show=[Overlay Outlines] summarize");
}
