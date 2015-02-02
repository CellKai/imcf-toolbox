inpath="D:\\WEKA_Niko\\";
modelfile="fibrosis_group1.model";
infile="1462_mko_ctx.tif";
outpath="D:\\WEKA_Niko\\results\\";

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

//start_weka();
//load_classifier();
//apply_classifier("1442_wt_ctx.tif");
//apply_classifier("1442_wt_ctx.tif");
apply_classifier("1455_mko_ctx.tif");
apply_classifier("1456_mko_ctx.tif");
apply_classifier("1461_mko_ctx.tif");
apply_classifier("1462_mko_ctx.tif");
apply_classifier("1463_mko_ctx.tif");
apply_classifier("1467_mko_ctx.tif");
apply_classifier("1468_mko_ctx.tif");
apply_classifier("1469_wt_ctx.tif");
apply_classifier("1470_wt_ctx.tif");
apply_classifier("1475_wt_ctx.tif");

