from ij import IJ
from ij.io import FileSaver
from os import path

def run():
	# Choose a directory to store each slice as a file
	target = DirectoryChooser("Choose target directory").getDirectory()
	if target is None:
		# User canceled the dialog
		IJ.showMessage("No directory chosen, aborting.")
		return
	#print "Using", target, "as destination folder"

	return

	wm = WindowManager

	wcount = wm.getWindowCount()
	print "number of windows:", wcount

	# determine padding width
	pad = len(str(wcount))

	for i in range(wcount):
		### image ID lists start with 1, not 0
		## wid = id + 1
		imgid = wm.getNthImageID(i+1)
		# print "window id ", i+1, ":", wm.getNthImageID(i+1)
		imp = wm.getImage(i+1)
		fs = FileSaver(imp)
		# Print image details
		# print "  title:", imp.title
		# print "  current window:", wm.getCurrentWindow()
		# Construct filename
		filename = 'tile_' + str(i+1).zfill(pad) + '.tif'
		filepath = target + '/' + filename
		#print "filename:", filename
		if fs.saveAsTiffStack(filepath):
			print "imageID", imgid, "saved as", filename
		else:
			print "ERROR saving imageID", imgid, "file at", filepath

run()