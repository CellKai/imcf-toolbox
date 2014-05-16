// String.paste requires 1.48j
requires("1.48j");

selectWindow("Results");

// make sure the ID column is disabled:
setOption("ShowRowNumbers", false);
updateResults;

lines = split(getInfo("window.contents"), "\n");
// fields = split(lines[0], "\t");

title_short = "Segmentation Results Table";
title = "[" + title_short + "]";
run("Table...", "name=" + title + " width=450 height=600");

print(title, "\\Headings:ID\t" + lines[0]);
for (i=1; i < lines.length; i+=1) {
    roiManager("select", i-1);
    name = Roi.getName;
    print(title, name + "\t" + lines[i]);
}