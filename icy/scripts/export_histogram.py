from icy.main import Icy
from icy.util import XLSUtil
from plugins.ylemontag.histogram import Histogram

NUM_BINS = 16
XLS_FILE = '/tmp/icy_py_excel_test.xls'


def get_histogram(seq, nbins, bin_min, bin_max):
	# hist = Histogram.compute(seq, NUM_BINS, val_min + bwh, val_max - bwh)
	hist = Histogram.compute(seq, nbins, bin_min, bin_max)
	hist_list = []
	for i in xrange(hist.getNbBins()):
		bin = hist.getBin(i)
		val = bin.getCentralValue()
		count = bin.getCount()
		hist_list.append([val, count])
	return hist_list


seq = Icy.getMainInterface().getFocusedSequence()

print "--------------------------------"
print('Sequence name: "%s"' % seq.name)
print "--------------------------------"

#print dir(seq)
num_c = seq.getSizeC()
bounds = seq.getChannelsGlobalBounds()
val_min = bounds[0]
val_max = bounds[1]
bwh = (val_max - val_min + 1) / (NUM_BINS * 2)  # bin width half

#  create excel document (workbook)
wb = XLSUtil.createWorkbook(XLS_FILE)
# create a new page (sheet) in the excel document
ws = XLSUtil.createNewPage(wb, "Histogram")

# set excel headers
XLSUtil.setCellString(ws, 0, 0, "File name")
XLSUtil.setCellString(ws, 1, 0, seq.name)
XLSUtil.setCellString(ws, 0, 2, 'Number of channels')
XLSUtil.setCellNumber(ws, 1, 2, num_c)
XLSUtil.setCellString(ws, 0, 3, 'Global min')
XLSUtil.setCellNumber(ws, 1, 3, val_min)
XLSUtil.setCellString(ws, 0, 4, 'Global max')
XLSUtil.setCellNumber(ws, 1, 4, val_max)

XLSUtil.setCellString(ws, 0, 6, 'Number of Histogram bins')
XLSUtil.setCellNumber(ws, 1, 6, NUM_BINS)
XLSUtil.setCellString(ws, 0, 7, 'Bin width')
XLSUtil.setCellNumber(ws, 1, 7, bwh*2)


row = 9  # internal row counter

for c in xrange(num_c):
	channel = seq.extractChannel(c)
	hist = get_histogram(channel, NUM_BINS, val_min + bwh, val_max - bwh)
	XLSUtil.setCellString(ws, 0, row, 'Histogram for channel')
	XLSUtil.setCellNumber(ws, 1, row, c)
	row += 1
	for i in hist:
		XLSUtil.setCellNumber(ws, 0, row, i[0])
		XLSUtil.setCellNumber(ws, 1, row, i[1])
		row += 1
	row += 2


# close and save the excel file
XLSUtil.saveAndClose(wb)
