#!/usr/bin/python

"""Parse one or more CSV files containing coordinates of tracklists generated
by the "MTrack2" plugin for ImageJ/FiJi.
"""

import csv
import sys
import argparse
import pprint
import logging

# we need to distinguish at least three possibilities, cells can be empty,
# strings or float numbers, so a more sohpisticated parsing is required:
def parse_cell(x):
    retval = 0
    # flag columns can contain '*', which we currently ignore
    if x == '*':
        return retval
    if x != "":
        try:
            retval = float(x)
        except ValueError:
            retval = str(x).strip()
            if retval == "":
                retval = 0
    return retval

argparser = argparse.ArgumentParser(description=__doc__)
# argparser.add_argument('-p', '--overlap', type=float, default='0.15',
#     help='tile overlap (default 0.15)')
argparser.add_argument('-i', '--infile', required=True, type=file,
    help='CSV file containing track positions')
argparser.add_argument('-o', '--outfile', type=argparse.FileType('w', 0),
    help='output file', required=True)
argparser.add_argument('-v', '--verbose', dest='verbosity',
    action='count', default=0)
try:
    args = argparser.parse_args()
except IOError as e:
    argparser.error(str(e))

pp = pprint.PrettyPrinter(indent=4)

# default loglevel is 30 (warn) while 20 (info) and 10 (debug) show more details
loglevel = (3 - args.verbosity) * 10

log = logging.getLogger(__name__)
# create console handler and add it to the logger
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(loglevel)

log.debug(pp.pformat(args.__contains__))
log.debug(pp.pformat(type(args)))
log.debug("Infile: %s" % args.infile)
log.debug("Outfile: %s" % args.outfile)

data = []

csvreader = csv.reader(args.infile, delimiter='\t')
# parse all lines into memory
# NOTE: this is bad if the files get too large, but we haven't seen result
# files from MTrack2 that are bigger than a couple of MB.
for row in csvreader:
    data.append([parse_cell(x) for x in row])
    # data.append(row)

# start parsing the header
header = []
header.append(data.pop(0))
header.append(data.pop(0))
if not header[0][0] == 'Frame':
    # exit because file is broken...
    sys.exit('Unable to find correct header, stopping.')
log.info("Header:\n%s\n" % pp.pformat(header))

# second line is 'Tracks 1 to N', so we can read the total number there:
trackmax = int(header[1][0].split(' ')[3])
log.info("Total number of tracks: %s" % pp.pformat(trackmax))

# last N lines are the stats per track
trackstats = []
while True:
    # pop returns the last element if no index is given
    cur = data.pop()
    if cur[0] == 'Track':
        # remove one more line (empty), then we're done
        cur = data.pop()
        break
    else:
        trackstats.append(cur)
# as we parsed from the last element, we need to reverse the list
trackstats.reverse()
log.info("Track statistics:\n%s" % pp.pformat(trackstats))


