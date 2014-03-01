"""Fiji plugin for stitching FluoView mosaics in OIF format."""

import sys
# before doing anything else check the Python version:
if not sys.version_info[:2] >= (2, 7):
    raise Exception('Python 2.7 or newer is required!')

# explicitly add our libs to the module search path
from java.lang.System import getProperty
from os.path import join, dirname, basename
sys.path.append(join(getProperty('fiji.dir'), 'plugins', 'IMCF', 'libs'))


from ij import IJ
from ij.io import OpenDialog
from ij.gui import GenericDialog
from optparse import OptionParser

import fluoview as fv
from log import log, set_loglevel
from misc import flatten


def ui_get_input_file():
    """Ask user for input file and process results."""
    dialog = OpenDialog("Choose a 'MATL_Mosaic.log' file")
    fname = dialog.getFileName()
    if (fname is None):
        log.warn('No input file selected!')
        return((None, None))
    base = dialog.getDirectory()
    return((base, fname))


def gen_mosaic_details(mosaics):
    """Generate human readable string of details about the parsed mosaics."""
    # TODO: could go into fluoview package
    msg = ""
    mcount = mosaics.experiment['mcount']
    msg += "Parsed %i mosaics from the FluoView project log.\n \n" % mcount
    for mos in mosaics.mosaics:
        msg += "Mosaic %i: " % mos['id']
        msg += "%i x %i tiles, " % (mos['xcount'], mos['ycount'])
        msg += "%i%% overlap.\n" % int(100 - mos['ratio'])
    return(msg)


def main_interactive():
    """The main routine for running interactively."""
    (base, fname) = ui_get_input_file()
    if (base is None):
        return
    log.warn(base + fname)
    mosaic = fv.FluoViewMosaic(base + fname)
    dialog = GenericDialog('FluoView OIF Stitcher')
    msg = gen_mosaic_details(mosaic)
    msg += "\n \nPress [OK] to write tile configuration files\n"
    msg += "and continue with running the stitcher."
    dialog.addMessage(msg)
    dialog.showDialog()
    if dialog.wasOKed():
        mosaic.write_all_tile_configs(fixpath=True)
        code = flatten(mosaic.gen_stitching_macro_code('stitching', base))
        IJ.runMacro(code)


def main_noninteractive():
    """The main routine for running non-interactively."""
    args = parse_arguments()
    set_loglevel(args.verbose)
    log.info('Running in non-interactive mode.')
    log.debug('Python FluoView package file: %s' % fv.__file__)
    base = dirname(args.fvlog)
    fname = basename(args.fvlog)
    mosaic = fv.FluoViewMosaic(join(base, fname))
    log.warn(gen_mosaic_details(mosaic))
    code = flatten(mosaic.gen_stitching_macro_code('stitching', base))
    if not args.dryrun:
        log.info('Writing tile configuration files.')
        mosaic.write_all_tile_configs(fixpath=True)
        log.info('Launching stitching macro.')
        IJ.runMacro(code)
    else:
        log.info('Dry-run was selected. Printing generated macro:')
        log.warn(code)


def parse_arguments():
    """Parse commandline arguments."""
    epi = ('NOTE: commandline arguments need to be prefixed by THREE dashes'
           '(e.g. "---dry-run") instead of the default two as Fiji otherwise '
           'parses the arguments and won\'t pass them to the plugin.')
    # preprocess argv for the above described workaround:
    for (i, arg) in enumerate(sys.argv):
        sys.argv[i] = arg.replace('---', '--')
        if (len(sys.argv[i]) == 3):
            sys.argv[i] = arg.replace('--', '-')

    parser = OptionParser(description=__doc__, epilog=epi)
    add = parser.add_option  # shorthand to improve readability
    add("--fvlog", help='path to "MATL_Mosaic.log" file', metavar="FILE")
    add("--dry-run", action="store_true", dest="dryrun", default=False,
        help="print generated macro but don't run stitcher")
    add("--verbose", action="count", default=0)

    (opts, args) = parser.parse_args()
    if (opts.fvlog is None):
        print('ERROR: No MATL_Mosaic.log file given.\n')
        parser.print_help()
        sys.exit(1)
    return(opts)  # we're not following this weird "args" idea of OptionParser

if (len(sys.argv) > 0):
    sys.exit(main_noninteractive())
else:
    main_interactive()
