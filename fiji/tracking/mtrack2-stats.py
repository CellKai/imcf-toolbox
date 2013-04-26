#!/usr/bin/python

"""Parse one or more CSV files containing coordinates of tracklists generated
by the "MTrack2" plugin for ImageJ/FiJi.
"""

import csv
import sys
import argparse
import pprint
import logging

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

# parse elements of the row and discard all non-numerical ones:
csvreader = csv.reader(args.infile, delimiter='	')
for row in csvreader:
    data.append(row)

# last N lines are the stats per track
trackstats = []
while True:
    cur = data.pop()
    if cur[0].strip() == 'Track':
        # remove one more line (empty), then we're done
        data.pop()
        break
    else:
        trackstats.append(cur)
