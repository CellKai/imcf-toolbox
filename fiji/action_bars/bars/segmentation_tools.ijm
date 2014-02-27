// This Action Bar description file is meant for being included in a .jar file
// and thus has no ImageJ macro language section, instead this part is in the
// "plugins.config" file included in the .jar.

<line>
<button>
label=Recent commands
arg=<macro>
run("*recent commands");
</macro>
<button>
label=Monitor Events (Log)
arg=<macro>
run("Monitor Events...");
</macro>
<button>
label=Remove Outliers
arg=<macro>
run("Remove Outliers...");
</macro>
<button>
label=Despeckle
arg=<macro>
run("Despeckle");
</macro>
</line>

<line>
<button>
label=Subtract
arg=<macro>
run("Subtract...");
</macro>
<button>
label=Threshold
arg=<macro>
run("Threshold...");
</macro>
<button>
label=Local Threshold
arg=<macro>
run("Auto Local Threshold");
</macro>
<button>
label=(void)
arg=<macro>
run("");
</macro>
</line>

<line>
<button>
label=Watershed
arg=<macro>
run("Watershed");
</macro>
<button>
label=Analyze Particles
arg=<macro>
run("Analyze Particles...");
</macro>
<button>
label=(void)
arg=<macro>
run("");
</macro>
<button>
label=(void)
arg=<macro>
run("");
</macro>
</line>

<line>
<button>
label=Stack to RGB
arg=<macro>
run("Stack to RGB");
</macro>
<button>
label=16-bit
arg=<macro>
run("16-bit");
</macro>
<button>
label=8-bit
arg=<macro>
run("8-bit");
</macro>
<button>
label=Make Binary
arg=<macro>
run("Make Binary");
</macro>
</line>

// end of file
