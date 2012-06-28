// Action Bar description file :IMCF_toolbar
run("Action Bar","/plugins/ActionBar/IMCF_toolbar.ijm");
exit();


<line>
<button> 1 line 1
label=Bio-Formats Importer
icon=IMCF_toolbar/loci-import.png
arg=<macro>
run("Bio-Formats Importer");
</macro>

<button> 2 line 1
label=Bio-Formats Exporter
icon=IMCF_toolbar/loci-export.png
arg=<macro>
run("Bio-Formats Exporter");
</macro>

<button> 3 line 1
label=Histogram
icon=IMCF_toolbar/dHist.png
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
icon=IMCF_toolbar/maxim2_tango_rgb.png
arg=<macro>
run("Channels Tool...");
</macro>

<button> 6 line 1
label=Median Filter
icon=IMCF_toolbar/median.png
arg=<macro>
run("Median...");
</macro>

<button> 7 line 1
label=Gaussian Blur
icon=IMCF_toolbar/gauss_filter.png
arg=<macro>
run("Gaussian Blur...");
</macro>

<button> 8 line 1
label=FFT BandPass
icon=IMCF_toolbar/bandpass.png
arg=<macro>
run("Bandpass Filter...");
</macro>
</line>

// LINE 2:

<line>
<button> 1 line 2
label=Image Calculator
icon=IMCF_toolbar/calculator.png
arg=<macro>
run("Image Calculator...");
</macro>

<button> 2 line 2
label=Subtract Background
icon=IMCF_toolbar/subtract_background.png
arg=<macro>
run("Subtract Background...");
</macro>

<button> 3 line 2
label=stitchPairs
arg=<macro>
run("Pairwise stitching");
</macro>

<button> 4 line 2
label=stitchGrid
arg=<macro>
run("Grid/Collection stitching");
</macro>

<button> 5 line 2
label=Stack Registration
icon=IMCF_toolbar/stack_reg.png
arg=<macro>
run("StackReg");
</macro>
</line>

// end of file