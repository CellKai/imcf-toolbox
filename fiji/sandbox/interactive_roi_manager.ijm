/*
//print(Roi.getName);
Roi.setProperty("celltype", "mother");
//print(Roi.getProperties);
Roi.setStrokeColor("red");
Roi.setStrokeWidth(5);
*/


// NOTE: the following only works for "Results" tables and returns
// the value of the first field (assuming it contains an ID or similar)
function get_table_selection(){
        String.copyResults();
        str = String.paste();
        fields = split(str, "\t");
        return(fields[0]);
}

function upd_roim_selection_from_results(){
        sel = get_table_selection();
        //print(sel);
        roiManager("Deselect");
        roiManager("select", sel - 1);
}

function create_advanced_results_table(){
        // make sure the ID column is disabled:
        setOption("ShowRowNumbers", false);
        updateResults;

        // get the data and close the original Results table:
        selectWindow("Results");
        lines = split(getInfo("window.contents"), "\n");
        run("Close");

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
}

function create_status_table(title){
        name = "[" + title + "]";
        run("New... ", "name="+name+" type=Table");
        return name;
}

/*
for (i=0; i < nResults; i++) {
    
}
*/