from ij import IJ
from ij.io import FileSaver
from os import path

def run():
	msg = "<html>"
	# Choose a directory to store each slice as a file
	wm = WindowManager
	wcount = wm.getWindowCount()
	if wcount == 0:
		msg += "No windows open, nothing to do.<br/>"
		IJ.showMessage(msg)
		return
	msg += "Number of open windows: " + str(wcount) + "<br/>"

	target = DirectoryChooser("Choose target directory").getDirectory()
	if target is None:
		# User canceled the dialog
		IJ.showMessage("No directory chosen, aborting.")
		return
	msg += "Selected '" + target + "'as destination folder.<br/>"
	
	# determine padding width for filename
	pad = len(str(wcount))

	for i in range(wcount):
		# image ID lists start with 1 instead of 0, so for convenience:
		wid = i + 1
		imp = wm.getImage(wid)
		imgid = wm.getNthImageID(wid)
		print "window id:", wid, ", imageID:", wm.getNthImageID(wid)
		
		# Construct filename
		filename = 'tile_' + str(wid).zfill(pad) + '.tif'
		filepath = target + '/' + filename
		fs = FileSaver(imp)
		#FIXME: check if this is a stack!!
		if fs.saveAsTiffStack(filepath):
			print "imageID", imgid, "saved as", filename
		else:
			IJ.error("Error saving current image, stopping.")
			# FIXME: return a "bad" value
			return
	
	msg += "<br/>Successfully saved " + str(wcount) + " files.<br/>"
	IJ.showMessage(msg)

run()
