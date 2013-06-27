#!/usr/bin/python

"""Parse one or more CSV files containing coordinates of tracklists generated
by the "MTrack2" plugin for ImageJ/FiJi.
"""

# TODO:
#  - check which functions should go into a central module

import csv
import sys
import argparse
import pprint
import numpy as np
import volpy as vp
from log import log
from aux import check_filehandle

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

def movement_vectors(coords, step=1):
    ret = np.zeros(coords.shape)
    ret[step:] = coords[step:] - coords[0:-step]
    return ret

def save_results_labeled(f_out, data, lbl):
    try:
        np.savetxt(f_out, data, fmt='%.5f', header=lbl, delimiter='\t')
        log.info("Finished writing CSV.")
    except TypeError:
        log.warn("Could not write column labels, most likely your numpy " +
            "version is too old (requires at least 1.7.0), falling back " +
            "to unlabeled CSV format.")
        save_results_unlabeled(f_out, data)

def save_results_unlabeled(f_out, data):
    np.savetxt(f_out, data, fmt='%.5f', delimiter='\t')
    log.info("Finished writing CSV.")

def save_results(f_out, data, labeled=False):
    lbl = 'x\ty\tdx\tdy\tdist\tangle\tdist5\tangle5'
    if labeled:
        save_results_labeled(f_out, data, lbl)
    else:
        save_results_unlabeled(f_out, data)

def calc_rotation(deltas, normals, start):
    # TODO: add description, move to volpy
    res = np.zeros((deltas.shape[0], 1))
    for p in range(start, res.shape[0]-1):
        # if any of the two normal vectors is zero, nothing moved
        if (normals[p-1] * normals[p] == 0.):
            res[p+1] = 0
        else:
            res[p+1] = vp.angle2D(deltas[p-1], deltas[p])
    return res

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-l', '--label', action='store_const', const=True,
        default=False, help='add column labels (requires numpy >= 1.7)')
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
    # after successful argument-parsing, we can call the "real" main function:
    gen_stats(args.infile, args.outfile, args.label, verbosity=args.verbosity)

def gen_stats(f_in, f_out, label=False, delta=5, verbosity=0):
    # default loglevel is 30 (warn) while 20 (info) and 10 (debug) show more details
    loglevel = (3 - verbosity) * 10
    log.setLevel(loglevel)
    log.warn("Infile: %s" % f_in)
    log.debug("Outfile: %s" % f_out)
    
    pp = pprint.PrettyPrinter(indent=4)
    
    # TODO: parsing can be done in a nicer way be reading the header lines via
    # csvreader.next(), checking for the expected values and the number of tracks
    # and then directly reading the trackpoints into a numpy ndarray...
    mtrack2_file = check_filehandle(f_in, 'r')
    csvreader = csv.reader(mtrack2_file, delimiter='\t')

    # parse all lines into memory
    # NOTE: this is bad if the files get too large, but we haven't seen result
    # files from MTrack2 that are bigger than a couple of MB.
    data = []
    for row in csvreader:
        data.append([parse_cell(x) for x in row])
        # data.append(row)
    
    # start parsing the header
    header = []
    header.append(data.pop(0))
    header.append(data.pop(0))
    if not header[0][0] == 'Frame':
        # exit because file is broken...
        raise SystemExit('Unable to find correct header, stopping.')
    log.debug("Header:\n%s\n" % pp.pformat(header))
    
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
    log.warn("Track statistics:\n%s" % pp.pformat(trackstats))
    
    # this code can help debugging problematic files:
    # for row in data:
    #     try:
    #         np.array(row, dtype='float')
    #     except ValueError:
    #         raise SystemExit(row)
    
    # remove column 0 (indices), and every third one (flags)
    todelete= range(0, (trackmax+1)*3, 3)
    npdata = np.delete(data, todelete, axis=1)
    npdata_bool = npdata > 0
    
    tracklen = [0] * trackmax
    t_overlap = npdata_bool[:,0]
    for track in range(trackmax):
        tracklen[track] = sum(npdata_bool[:,track*2])
        t_overlap = t_overlap * npdata_bool[:,track*2]
    
    if trackmax > 1 and sum(t_overlap) > 0:
        raise SystemExit("*** WARNING: Found overlapping tracks! ***")
    
    t_combined = np.zeros((npdata.shape[0],2))
    for track in range(trackmax):
        t_combined += npdata[:,track*2:(track+1)*2]
    
    comb_mask = np.zeros(t_combined.shape[0])
    for i, row in enumerate(t_combined):
        if (row == [0., 0.]).all():
            # print 'row %i is zerooooo' % i
            comb_mask[i] = True
    
    t_combined = np.ma.compress_rows(np.ma.array(t_combined,
            mask=np.repeat(comb_mask, 2)))
    
    mv = {}
    mn = {}
    rot = {}
    for step in (1, delta):
        # calculate movement vectors (mv):
        mv[step] = movement_vectors(t_combined, step)
        # calculate vector normals (mn):
        mn[step] = np.zeros((mv[step].shape[0], 1))
        for p in range(1, mn[step].shape[0]):
            mn[step][p] = np.linalg.norm(mv[step][p])
        # calculate rotation:
        rot[step] = calc_rotation(mv[step], mn[step], step)

    outdata = np.hstack((t_combined, mv[1], mn[1], rot[1],
        mn[delta], rot[delta]))

    save_results(f_out, outdata, label)
    log.warn("Wrote results to '%s'" % f_out.name)

if __name__ == "__main__":
    sys.exit(main())
