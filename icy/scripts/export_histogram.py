from icy.main import Icy
from icy.util import XLSUtil
from plugins.ylemontag.histogram import Histogram

NUM_BINS = 16
XLS_FILE = '/tmp/icy_py_excel_test.xls'


def get_histogram(seq, nbins, bin_min, bin_max):
    """Generate a list of [val, count] from the histogram."""
    hist = Histogram.compute(seq, nbins, bin_min, bin_max)
    hist_list = []
    for i in xrange(hist.getNbBins()):
        bin = hist.getBin(i)
        val = bin.getCentralValue()
        count = bin.getCount()
        hist_list.append([val, count])
    return hist_list


def new_xls_row(ws, values):
    """Add a new row from a list of values to a worksheet."""
    global row
    col = 0
    for val in values:
        if type(val) is str or type(val) is unicode:
            XLSUtil.setCellString(ws, col, row, val)
        else:
            XLSUtil.setCellNumber(ws, col, row, val)
        col += 1
    row += 1


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
row = 0
new_xls_row(ws, ["File name", seq.name])
row += 1
new_xls_row(ws, ['Number of channels', num_c])
new_xls_row(ws, ['Global min', val_min])
new_xls_row(ws, ['Global max', val_max])
row += 1
new_xls_row(ws, ['Number of Histogram bins', NUM_BINS])
new_xls_row(ws, ['Bin width', bwh*2])


row += 2

for c in xrange(num_c):
    channel = seq.extractChannel(c)
    hist = get_histogram(channel, NUM_BINS, val_min + bwh, val_max - bwh)
    new_xls_row(ws, ['Histogram for channel', c])
    overall = 0
    for i in hist:
        new_xls_row(ws, [i[0], i[1]])
        overall += i[1]
    new_xls_row(ws, ['Overall count from bins', overall])
    row += 2

# close and save the excel file
XLSUtil.saveAndClose(wb)
