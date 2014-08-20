dir = '/scratch/imageproc/data/keith/BPP2n86_FV10__20140817_131026/';
dir = '/scratch/imageproc/data/keith/FV10__20140705_103301_BPP2n129';

function printArray(a) {
      print("----- printArray() -----");
      for (i=0; i<a.length; i++)
          print(i+": "+a[i]);
}

function get_tileconfig_files(dir) {
	filelist = getFileList(dir);
	tileconfigs = newArray(filelist.length);
	ti = 0;  // the tileconfig index
	for (fi=0; fi<filelist.length; fi++) {
		if(matches(filelist[fi], 'mosaic_[0-9]+\.txt')) {
			tileconfigs[ti] = filelist[fi];
			//print(tileconfigs[ti]);
			ti++;
		}
	}
	return Array.trim(tileconfigs, ti);
}

tileconfigs = get_tileconfig_files(dir);
printArray(tileconfigs);
