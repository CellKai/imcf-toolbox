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
import logging
import numpy as np
import math
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

def angle(v1u, v2u, normalize=False):
    # TODO: should go into the volpy module
    ''' Calculates the angle between vectors (in arc degrees).
    .
    Calculates the angle in degrees given to n-dimensional unit vectors given
    as np.ndarrays. The normalization can be done by the function if desired.
    Note that when calculating angles between large number of vectors, it is
    most likely more efficient to normalize them in advance.
    .
    Parameters
    ----------
    v1u, v2u : np.ndarray
        The vectors to compare.
    normalize : bool
        Defines whether we should normalize the given vectors. Otherwise they
        need to be normalized already.
    .
    Returns
    -------
    rad : float
        The angle between the vectors in arc degrees.
    .
    Example
    -------
    >>> import numpy as np
    >>> x = np.array([[1,0,0],[1,0,1]])
    >>> angle(x[0], x[1], normalize=True)
    45.000000000000007
    >>> x = np.array([[1,2,3],[1,2,1]])
    >>> angle(x[0], x[1], normalize=True)
    29.205932247399399
    '''
    # print(v1u.shape)
    if normalize:
        v1u = v1u / np.linalg.norm(v1u)
        v2u = v2u / np.linalg.norm(v2u)
    rad = np.arccos(np.dot(v1u, v2u))
    if math.isnan(rad):
        if (v1u == v2u).all():
            rad = 0.0
        else:
            rad = np.pi
    return rad * (180/np.pi)

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
    gen_stats(args.infile, args.outfile, args.label, args.verbosity)

def gen_stats(f_in, f_out, label=False, verbosity=0):
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
        sys.exit('Unable to find correct header, stopping.')
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
    #         print row
    #         sys.exit()
    
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
        sys.exit("*** WARNING: Found overlapping tracks! ***")
    
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
    
    # calculate the movement vectors:
    movement_v = movement_vectors(t_combined, 1)
    movement5_v = movement_vectors(t_combined, 5)
    
    # movement vector normals:
    movement_n = np.zeros((movement_v.shape[0], 1))
    movement5_n = np.zeros((movement5_v.shape[0], 1))
    for p in range(1, movement_n.shape[0]):
        movement_n[p] = np.linalg.norm(movement_v[p])
        movement5_n[p] = np.linalg.norm(movement5_v[p])
    
    rotation = np.zeros((movement_n.shape[0], 1))
    for p in range(1, rotation.shape[0]-1):
        # print movement_v[p-1]
        # print movement_n[p-1]
        rotation[p+1] = angle(movement_v[p-1]/movement_n[p-1],
                            movement_v[p]/movement_n[p])
    
    rotation5 = np.zeros((movement5_n.shape[0], 1))
    for p in range(5, rotation5.shape[0]-1):
        rotation5[p+1] = angle(movement5_v[p-1]/movement5_n[p-1],
                            movement5_v[p]/movement5_n[p])
    
    comb = np.hstack((t_combined, movement_v, movement_n, rotation,
        movement5_n, rotation5))

    save_results(f_out, comb, label)

if __name__ == "__main__":
    sys.exit(main())
