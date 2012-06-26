from ij import IJ
from ij.io import FileSaver
from os import path

target = 'C:/Users/ehrenfeu/Desktop/tmpfast/ivana/stitch_test'
print "Using", target, "as destination folder"

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

#print "ID list of windows:", WindowManager.getIDList()
##idlist = WindowManager.getIDList()
##for wid in idlist:
##	print "window id:", wid
##
##print "front window:", WindowManager.getFrontWindow()


# wm.putBehind()

#print "width:", imp.width
#print "height:", imp.height
#print "number of pixels:", imp.width * imp.height
# print "# of slices:", imp.getNSlices(), ", cur:", imp.getSlice()
# print "stack size:", imp.getImageStackSize(), ", channels:", imp.getNChannels()
# framepos = imp.getT()
# print "# of time frames:", imp.getNFrames(), ", cur:", framepos


#print "switching to next hyperstack frame position..."
#imp.setT(framepos + 1)
#print "current hyperstack frame position:", imp.getT()

#print "getOpenAsHyperStack:", imp.getOpenAsHyperStack()

#types = {ImagePlus.COLOR_RGB : "RGB",
#         ImagePlus.GRAY8 : "8-bit",
#         ImagePlus.GRAY16 : "16-bit",
#         ImagePlus.GRAY32 : "32-bit",
#         ImagePlus.COLOR_256 : "8-bit color"}

#print "image type:", imp.type, types[imp.type]
