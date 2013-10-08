// Action Bar description file :icons
run("Action Bar","/plugins/ActionBar/icons.ijm");
exit();

<DnDAction>
file=getArgument();
param = "open=[" + file + "]";
run("Bio-Formats Importer", param);
//run("Bio-Formats Macro Extensions");
//Ext.openImagePlus(file)
</DnDAction>

<line>
<button> 1 line 1
label=Bio-Formats Importer
icon=icons/loci-import.png
arg=<macro>
run("Bio-Formats Importer");
</macro>

<button> 2 line 1
label=Bio-Formats Exporter
icon=icons/loci-export.png
arg=<macro>
run("Bio-Formats Exporter");
</macro>

<button> 3 line 1
label=Histogram
icon=icons/dHist.png
arg=<macro>
run("Histogram");
</macro>

//cmd of "auto" button in B&C
//run("Enhance Contrast", "saturated=0.35");
<button> 4 line 1
label=B & C
arg=<macro>
run("Brightness/Contrast...");
</macro>

<button> 5 line 1
label=Channels Tool
icon=icons/maxim2_tango_rgb.png
arg=<macro>
run("Channels Tool...");
</macro>

<button> 6 line 1
label=Median Filter
icon=icons/median.png
arg=<macro>
run("Median...");
</macro>

<button> 7 line 1
label=Gaussian Blur
icon=icons/gauss_filter.png
arg=<macro>
run("Gaussian Blur...");
</macro>

<button> 8 line 1
label=FFT BandPass
icon=icons/bandpass.png
arg=<macro>
run("Bandpass Filter...");
</macro>
</line>

// LINE 2:

<line>
<button> 1 line 2
label=Image Calculator
icon=icons/calculator.png
arg=<macro>
run("Image Calculator...");
</macro>

<button> 2 line 2
label=Subtract Background
icon=icons/subtract_background.png
arg=<macro>
run("Subtract Background...");
</macro>

<button> 3 line 2
label=stitchPairs
icon=icons/stitchpairs.png
arg=<macro>
run("Pairwise stitching");
</macro>

<button> 4 line 2
label=stitchGrid
icon=icons/stitchgrid.png
arg=<macro>
run("Grid/Collection stitching");
</macro>

<button> 5 line 2
label=Stack Registration
icon=icons/stack_reg.png
arg=<macro>
run("StackReg");
</macro>

<button> 6 line 2
label=Segmentation Toolbar
icon=icons/segmentation.png
arg=<macro>
run("Segmentation Toolbar");
</macro>
</line>

// end of file
