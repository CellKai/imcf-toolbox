

// NOTE: the following only works for "Results" tables and returns
// the value of the first field (assuming it contains an ID or similar)
function get_table_selection(){
        String.copyResults();
        str = String.paste();
        fields = split(str, "\t");
        return fields[0];
}

function get_table_row_by_id(id){
    // look up a given ID in the Results table and return the
    // row (index number) if it exists, otherwise -1
    // TODO: after refactoring get_table_selection this should
    // not be required any more
    setOption("ShowRowNumbers", true);
    updateResults;
    id_ret = -1;
    for (i=0; i < nResults; i++){
        id_cur = getResult("ID", i);
        if (id == id_cur){
            id_ret = i;
        }
    }
    setOption("ShowRowNumbers", false);
    updateResults;
    return id_ret;
}

function get_table_row_by_roiname(name){
    // look up a given ROI-name in the Results table and return the
    // row (index number) if it exists, otherwise -1
    // TODO: after refactoring get_table_selection this needs to
    // be refactored as well
    setOption("ShowRowNumbers", true);
    updateResults;
    id_ret = -1;
    for (i=0; i < nResults; i++){
        name_cur = getResultString("ROI", i);
        if (name == name_cur){
            id_ret = i;
        }
    }
    setOption("ShowRowNumbers", false);
    updateResults;
    return id_ret;
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