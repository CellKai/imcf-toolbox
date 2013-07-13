#!/usr/bin/python

"""Parse one or more CSV files containing coordinates of tracklists generated
by the "MTrack2" plugin for ImageJ/FiJi.
"""

# TODO:
#  - check which functions should go into a central module
#  - split parsing, processing and generating output into functions
#  - look for clusters in the thresholded angles by defining a maximum gap
#    size between two adjacent / subsequent angles above the threshold
#  - check the "Knockout Mouse Phenotyping Program" (KOMP2) for behavioural
#    descriptors of our movement patterns
#  - ideas: calculate variance, combine speed+angle?

import csv
import sys
import argparse
import pprint
import numpy as np
import volpy as vp
from log import log
from aux import check_filehandle, filename


def parse_cell(x):
    '''Parse cells of MTrack2 result files.
    .
    Processes individual cells coming from an MTrack2 result file. Cells can be
    empty, contain strings or float numbers. Currently cells containing only an
    asterisk "*" sign (used by MTrack2 to "flag" a cell) are ignored and zero
    is returned there.
    .
    Parameters
    ----------
    x : str
        The cell's input content.
    .
    Returns
    -------
    content : float or str
    '''
    retval = 0
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
    '''Calculate the vectors between points in a given coordinate sequence.
    .
    Takes an n-dimensional list of coordinates and a step-width (optional)
    and calculates the vectors between each tuple of coordinates with the
    given stepping-distance.
    .
    Parameters
    ----------
    coords : np.ndarray
        The sequence of coordinates.
    .
    Returns
    -------
    vectors : np.ndarray
        The sequence of differential vectors.
    '''
    # TODO: move to volpy
    ret = np.zeros(coords.shape)
    ret[step:] = coords[step:] - coords[0:-step]
    return ret


def _save_results_labeled(f_out, data, lbl):
    """Save results in CSV using a header row with labels."""
    try:
        np.savetxt(f_out, data, fmt='%.5f', header=lbl, delimiter='\t')
        log.info("Finished writing CSV.")
    except TypeError:
        log.warn("Could not write column labels, most likely your numpy " +
            "version is too old (requires at least 1.7.0), falling back " +
            "to unlabeled CSV format.")
        _save_results_unlabeled(f_out, data)


def _save_results_unlabeled(f_out, data):
    """Save results in CSV without header row."""
    np.savetxt(f_out, data, fmt='%.5f', delimiter='\t')
    log.info("Finished writing CSV.")


def _save_results(f_out, data, label=False):
    """Call functions to save data depending on the 'label' setting."""
    if label:
        _save_results_labeled(f_out, data, label)
    else:
        _save_results_unlabeled(f_out, data)


def calc_rotation(deltas, normals, start):
    '''Calculate angle between two vectors in 2D.
    .
    Takes two vectors in 2D euclidean space and calculates the directional
    change from the second to the first vector in degrees. Positive values
    correspond to right-turns, negative to left-turns.
    .
    Parameters
    ----------
    deltas : np.ndarray, shape = (n, 2)
        Movement vectors.
    normals : np.ndarray, shape = (n, 1)
        Corresponding vector normals.
    start : int
        Optional parameter to skip a number of initial values.
    .
    Returns
    -------
    deg_rotation : float
        The rotation angle in arc degrees [-180, 180].
    '''
    # TODO: move to volpy
    res = np.zeros((deltas.shape[0], 1))
    for p in range(start, res.shape[0] - 1):
        # if any of the two normal vectors is zero, nothing moved
        if (normals[p - 1] * normals[p] == 0.):
            res[p + 1] = 0
        else:
            res[p + 1] = vp.angle2D(deltas[p - 1], deltas[p])
    return res


def main():
    """Parse commandline arguments and run calculations."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-l', '--label', action='store_const', const=True,
        default=False, help='add column labels (requires numpy >= 1.7)')
    argparser.add_argument('-i', '--infile', required=True, type=file,
        dest='f_in', help='CSV file containing track positions')
    argparser.add_argument('-o', '--outfile', type=argparse.FileType('w', 0),
        dest='f_out', help='output file', required=True)
    argparser.add_argument('-v', '--verbose', action='count',
        dest='verbosity', default=0)
    argparser.add_argument('-d', '--delta', type=int, action='append',
        dest='deltas', help='stepping widths, can be repeated')
    argparser.add_argument('-t', '--threshold', type=float, default=0,
        dest='threshold', help='thresholding value for rotation in degrees')
    try:
        args = argparser.parse_args()
    except IOError as e:
        argparser.error(str(e))
    # after successful argument-parsing, we can call the "real" main function:
    gen_stats(args.f_in, args.f_out, args.label, args.deltas,
        args.threshold, args.verbosity)


def gen_stats(f_in, f_out, label=False, deltas=[], thresh=0, verbosity=0):
    """Parse and process tracks and calculate statistics from the data."""
    # default loglevel is 30 while 20 and 10 show more details
    loglevel = (3 - verbosity) * 10
    log.setLevel(loglevel)

    log.warn("Infile: %s" % f_in)
    log.debug("Outfile: %s" % f_out)
    if deltas:
        deltas = [1] + deltas
    else:
        deltas = [1]
    log.info("Stepping width(s): %s" % deltas)
    log.info("Angle threshold: %s" % thresh)

    pp = pprint.PrettyPrinter(indent=4)

    ######### tracks parsing #########

    # TODO: parsing can be done in a nicer way be reading the header lines via
    # csvreader.next(), checking for the expected values and the number of
    # tracks and then directly reading the trackpoints into a numpy ndarray...
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

    # create the ndarray from the remaining data while removing column 0
    # (indices), and every subsequent third column (flags)
    todelete = range(0, (trackmax + 1) * 3, 3)
    npdata = np.delete(data, todelete, axis=1)
    npdata_bool = npdata > 0

    ######### tracks processing (combining etc.) #########

    tracklen = [0] * trackmax
    t_overlap = npdata_bool[:, 0]
    for track in range(trackmax):
        tracklen[track] = sum(npdata_bool[:, track * 2])
        t_overlap = t_overlap * npdata_bool[:, track * 2]

    if trackmax > 1 and sum(t_overlap) > 0:
        raise SystemExit("*** WARNING: Found overlapping tracks! ***")

    t_combined = np.zeros((npdata.shape[0], 2))
    for track in range(trackmax):
        t_combined += npdata[:, track * 2:(track + 1) * 2]

    comb_mask = np.zeros(t_combined.shape[0])
    for i, row in enumerate(t_combined):
        if (row == [0., 0.]).all():
            # print 'row %i is zerooooo' % i
            comb_mask[i] = True

    t_combined = np.ma.compress_rows(np.ma.array(t_combined,
            mask=np.repeat(comb_mask, 2)))

    ######### calculations #########
    mv = {}
    mn = {}
    rot = {}
    rot_t = {}
    outdata = t_combined
    if label:
        label = 'pos_x\tpos_y'
    for step in deltas:
        # calculate movement vectors (mv):
        mv[step] = movement_vectors(t_combined, step)
        # calculate vector normals (mn):
        mn[step] = np.zeros((mv[step].shape[0], 1))
        for p in range(1, mn[step].shape[0]):
            mn[step][p] = np.linalg.norm(mv[step][p])
        # calculate rotation:
        rot[step] = calc_rotation(mv[step], mn[step], step)
        # for the movement vectors all values need to be written to the output,
        # but it is not necessary to repeat them for every stepping, so they
        # are only added for stepping '1':
        if (step == 1):
            outdata = np.hstack((outdata, mv[1]))
            if label:
                label += '\tdelta_x\tdelta_y'
        outdata = np.hstack((outdata, mn[step], rot[step]))
        # threshold rotation angles:
        if thresh > 0:
            rot_t[step] = np.where(abs(rot[step]) > thresh, rot[step], 0)
            outdata = np.hstack((outdata, rot_t[step]))
        if label:
            label += '\tdistance_%s\tangle_%s' % (step, step)
            if thresh > 0:
                label += '\tthresholded_angle_%s' % step

    if label:
        log.info('label: %s' % label)
    _save_results(f_out, outdata, label)
    log.warn("Wrote results to '%s'" % filename(f_out))

if __name__ == "__main__":
    sys.exit(main())
