from ij import IJ
from ij.io import FileSaver
from os import path

def run():
	msg = "<html>"
	# Choose a directory to store each slice as a file
	target = DirectoryChooser("Choose target directory").getDirectory()
	if target is None:
		# User canceled the dialog
		IJ.showMessage("No directory chosen, aborting.")
		return
	msg += "Selected '" + target + "'as destination folder.<br/>"
	
	wm = WindowManager
	wcount = wm.getWindowCount()
	msg += "Number of open windows: " + wcount + "<br/>"

	# determine padding width for filename
	pad = len(str(wcount))

	for i in range(wcount):
		# image ID lists start with 1 instead of 0, so for convenience:
		wid = i + 1
		imp = wm.getImage(wid)
		imgid = wm.getNthImageID(wid)
		print "window id ", wid, ":", wm.getNthImageID(wid)
		
		# Construct filename
		filename = 'tile_' + str(wid).zfill(pad) + '.tif'
		filepath = target + '/' + filename
		#print "filename:", filename
		fs = FileSaver(imp)
		if fs.saveAsTiffStack(filepath):
			print "imageID", imgid, "saved as", filename
		else:
			IJ.error("could not save imageID " + imgid + " to file '" + filepath + "'")
	
	msg += "<br/>Successfully saved " + wcount + " files.<br/>"
	IJ.showMessage(msg)

run()
