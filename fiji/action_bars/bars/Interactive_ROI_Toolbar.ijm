// This Action Bar description file is meant for being included in a .jar file
// and thus has no ImageJ macro language section, instead this part is in the
// "plugins.config" file included in the .jar.

<line>
<button>
label=Initialize
arg=<macro>
runMacro("InteractiveROIManager", "init");
</macro>
</line>

<line>
<button>
label=Show selected Result
arg=<macro>
runMacro("InteractiveROIManager", "update_selection");
</macro>
</line>

<line>
<button>
label=Primary
arg=<macro>
runMacro("InteractiveROIManager", "mark_primary");
</macro>
<button>
label=Secondary
arg=<macro>
runMacro("InteractiveROIManager", "mark_secondary");
</macro>
</line>

// end of file
