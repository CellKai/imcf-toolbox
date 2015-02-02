inpath="/scratch/data/__TESTFILES/weka/";
infile="1462_mko_ctx_1.tif";
outpath=inpath + "weka_results/"
model="bg_vs_tissue.model";

function start_weka() {
	open(inpath + infile);
	run("Trainable Weka Segmentation");
}

function load_classifier() {
	time_start = getTime();
	getDateAndTime(year, month, dow, dom, hour, minute, second, msec);
	tstamp = "" + year + "-" + month + "-" + dom + "_" + hour + "" + minute;
	IJ.log("--------------" + tstamp + "--------------");
	IJ.log("Starting to load classifier: " + inpath + modelfile);
	call("trainableSegmentation.Weka_Segmentation.loadClassifier",
		inpath + modelfile);
	duration = (getTime() - time_start) / 1000;
	IJ.log("Loading classifier completed (" + duration + ").");
}

function apply_classifier(file) {
	time_start = getTime();
	getDateAndTime(year, month, dow, dom, hour, minute, second, msec);
	tstamp = "" + year + "-" + month + "-" + dom + "_" + hour + "" + minute;
	IJ.log("--------------" + tstamp + "--------------");
	IJ.log("Applying classifier on " + file);
	call("trainableSegmentation.Weka_Segmentation.applyClassifier",
	inpath,
	file,
	"showResults=false",
	"storeResults=true",
	"probabilityMaps=true",
	outpath);
	duration = (getTime() - time_start) / 1000;
	IJ.log("Finished classifying " + file + " (" + duration + ").");
}


// NOTE: uncomment and run ONE AFTER THE OTHER, as currently the calls
// themselves fail to wait for completion and thus uncommenting all lines at
// once will cause the macro to fail!

start_weka();
// load_classifier();
// apply_classifier();
