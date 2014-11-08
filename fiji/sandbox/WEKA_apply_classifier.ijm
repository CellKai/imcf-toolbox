inpath="/scratch/data/__TESTFILES/weka/";
infile="1462_mko_ctx_1.tif";
outpath=inpath + "weka_results/"
model="bg_vs_tissue.model";

function start_weka() {
	open(inpath + infile);
	run("Trainable Weka Segmentation");
}

function load_classifier() {
	call("trainableSegmentation.Weka_Segmentation.loadClassifier",
	inpath + model);
}

function apply_classifier() {
	call("trainableSegmentation.Weka_Segmentation.applyClassifier",
	inpath,
	infile,
	"showResults=false",
	"storeResults=true",
	"probabilityMaps=true",
	outpath);
}


// NOTE: uncomment and run ONE AFTER THE OTHER, as currently the calls
// themselves fail to wait for completion and thus uncommenting all lines at
// once will cause the macro to fail!

start_weka();
// load_classifier();
// apply_classifier();
