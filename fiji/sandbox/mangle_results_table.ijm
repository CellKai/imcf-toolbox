selectWindow("Results");

// make sure the ID column is disabled:
setOption("ShowRowNumbers", false);
updateResults;

orig = "Original Results";
IJ.renameResults("Results", orig);

lines = split(getInfo("window.contents"), "\n");

headings = split(lines[0], "\t");
for (i=1; i < lines.length; i+=1) {
    roiManager("select", i-1);
    name = Roi.getName;
    setResult("ID", i-1, i);
    setResult("ROI", i-1, name);
    fields = split(lines[i], "\t");
    for (j=0; j < fields.length; j++) {
        setResult(headings[j], i-1, fields[j]);
    }
}

// make sure the ID column is disabled:
setOption("ShowRowNumbers", false);
updateResults;
