"""Fiji plugin for stitching FluoView mosaics."""

"""
NOTE: this plugin requires your Jython environment to be updated to 2.7 (beta)
as it will not work with Fiji's default Jython 2.5!

The plugin reads a "MATL_Mosaic.log" file created by Olympus FluoView,
identifies the mosaics configured in this experiment and creates an appropriate
tile configuration for each mosaic exploiting the fact that the coherence of
tiles to mosaics is stored in the experiment configuration as well as the
individual stage positions for each tile (which greatly speeds up the actual
stitching process.

After identifying the mosaics and their corresponding tiles, it creates a macro
to control the stitching of the individual mosaics given in the above
experiment file and runs this macro. Stitching results are saved as OME-TIFF
using the BioFormats exporter.

The plugin can be run from within Fiji's menu as well as completely headless
from the console using a command line like the one shown below. It uses the
"argparse" module to parse the commandline arguments, however to "trick" the
ImageJ launcher into passing on those arguments meant for the plugin instead of
parsing them itself, plugin-arguments have to be prefixed with a TRIPLE dash
"---" (both long and short versions):

MOSAICLOG="../../sample_data/fluoview/minimal_1mosaic_15pct/MATL_Mosaic.log"
ImageJ-linux64 --headless FluoView_OIF_OIB_Stitcher.py ---mosaiclog $MOSAICLOG


For debugging the interactive mode within Fiji, start the Jython Interpreter
and run the following commands:

>>> import sys
>>> sys.path.insert(0, '/opt/imcf_toolbox/fiji/tools')
>>> import FluoView_OIF_OIB_Stitcher as st
>>> st.main_interactive()

To use the script that is actually deployed in a Fiji installation (in the
.jar file), use the following commands to adjust the Python path:

import sys
from os.path import join
from java.lang.System import getProperty
imcfdir = join(getProperty('fiji.dir'), 'plugins', 'IMCF')
sys.path.insert(0, join(imcfdir, 'imcf_tools.jar'))
import FluoView_OIF_OIB_Stitcher as st
st.main_interactive()
"""

import sys
# before doing anything else check the Python version:
if not sys.version_info[:2] >= (2, 7):
    raise Exception('Python 2.7 or newer is required!')
import argparse
from os.path import join, dirname, basename

# ImageJ imports
from ij import IJ
from ij.io import OpenDialog
from ij.gui import GenericDialog

# explicitly add our libs to the module search path
from java.lang.System import getProperty
imcfdir = join(getProperty('fiji.dir'), 'plugins', 'IMCF')
imcftpl = join(imcfdir, 'imcf_macros.jar')

import microscopy.fluoview as fv
from microscopy import imagej
from log import log, set_loglevel
from misc import flatten
from ijpy import IJLogHandler
import imcf


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
    failcount = len(mosaics.mosaictrees) - len(mosaics)
    msg = "Parsed %i mosaics from the FluoView project.\n \n " % len(mosaics)
    if failcount > 0:
        msg += ("\n==== WARNING ====== WARNING ====\n \n"
                "Parsing failed on %i mosaic(s). Missing files?\n "
                "\n==== WARNING ====== WARNING ====\n \n \n" % failcount)
    for mos in mosaics:
        msg += "Mosaic %i: " % mos.supplement['index']
        msg += "%i x %i tiles, " % (mos.dim['X'], mos.dim['Y'])
        msg += "%.1f%% overlap.\n" % mos.get_overlap()
    return(msg)


def main_interactive():
    """The main routine for running interactively."""
    log.info('Running in interactive mode.')
    (base, fname) = ui_get_input_file()
    if (base is None):
        return
    log.warn("Parsing project file: %s" % (base + fname))
    IJ.showStatus("Parsing experiment file...")
    mosaics = fv.FluoViewMosaic(join(base, fname), runparser=False)
    IJ.showStatus("Parsing mosaics...")
    progress = 0.0
    count = len(mosaics.mosaictrees)
    step = 1.0 / count
    for subtree in mosaics.mosaictrees:
        IJ.showProgress(progress)
        mosaics.add_mosaic(subtree)
        progress += step
    IJ.showProgress(progress)
    IJ.showStatus("Parsed %i mosaics." % len(mosaics))
    dialog = GenericDialog('FluoView OIF / OIB Stitcher')
    if len(mosaics) == 0:
        msg = ("Couldn't find any (valid) mosaics in the project file.\n"
               " \n"
               "Please make sure to have all files available!\n"
               " \n"
               "Will stop now.\n")
        log.warn(msg)
        dialog.addMessage(msg)
        dialog.showDialog()
        return
    msg = "------------------------ EXPORT OPTIONS ------------------------"
    dialog.addMessage(msg)
    formats = ["OME-TIFF", "ICS/IDS"]
    dialog.addChoice("Export Format", formats, formats[0])
    dialog.addCheckbox("separate files by Z slices (OME-TIFF only)?", False)
    msg = "------------------------ EXPORT OPTIONS ------------------------"
    dialog.addMessage(msg)
    dialog.addMessage("")
    dialog.addMessage("")
    msg = gen_mosaic_details(mosaics)
    log.warn(msg)
    msg += "\n \nPress [OK] to write tile configuration files\n"
    msg += "and continue with running the stitcher."
    dialog.addMessage(msg)
    dialog.showDialog()

    opts = {}
    if dialog.getNextChoice() == 'ICS/IDS':
        opts['export_format'] = '".ids"'
    else:
        opts['export_format'] = '".ome.tif"'
        if dialog.getNextBoolean() == True:
            opts['split_z_slices'] = 'true'
    code = imagej.gen_stitching_macro_code(mosaics, 'templates/stitching',
                                           path=base, tplpath=imcftpl, opts=opts)
    log.warn("============= generated macro code =============")
    log.warn(flatten(code))
    log.warn("============= end of generated  macro code =============")

    if dialog.wasOKed():
        log.warn('Writing stitching macro.')
        imagej.write_stitching_macro(code, fname='stitch_all.ijm', dname=base)
        log.warn('Writing tile configuration files.')
        imagej.write_all_tile_configs(mosaics, fixsep=True)
        log.warn('Launching stitching macro.')
        IJ.runMacro(flatten(code))


def main_noninteractive():
    """The main routine for running non-interactively."""
    global imcftpl
    args = parse_arguments()
    set_loglevel(args.verbose)
    log.info('Running in non-interactive mode.')
    log.debug('Python FluoView package file: %s' % fv.__file__)
    base = dirname(args.mosaiclog)
    fname = basename(args.mosaiclog)
    mosaics = fv.FluoViewMosaic(join(base, fname))
    log.warn(gen_mosaic_details(mosaics))
    if args.templates is not None:
        imcftpl = args.templates
    code = imagej.gen_stitching_macro_code(mosaics, 'templates/stitching',
                                           path=base, tplpath=imcftpl)
    if not args.dryrun:
        log.info('Writing stitching macro.')
        imagej.write_stitching_macro(code, fname='stitch_all.ijm', dname=base)
        log.info('Writing tile configuration files.')
        imagej.write_all_tile_configs(mosaics, fixsep=True)
        log.info('Launching stitching macro.')
        IJ.runMacro(flatten(code))
    else:
        log.info('Dry-run was selected. Printing generated macro:')
        log.warn(flatten(code))


def parse_arguments():
    """Parse commandline arguments."""
    epi = ('NOTE: commandline arguments need to be prefixed by THREE dashes '
           '(e.g. "---dry-run") instead of the default two as Fiji otherwise '
           'parses the arguments and won\'t pass them to the plugin.')
    # preprocess argv for the above described workaround:
    for (i, arg) in enumerate(sys.argv):
        sys.argv[i] = arg.replace('---', '--')
        if (len(sys.argv[i]) == 3):
            sys.argv[i] = arg.replace('--', '-')

    parser = argparse.ArgumentParser(description=__doc__, epilog=epi)
    add = parser.add_argument  # shorthand to improve readability
    add("--mosaiclog", metavar='FILE', required=True,
        help='FluoView "MATL_Mosaic.log" XML file with stage positions')
    add("--templates", required=False,
        help='path containing the "templates/" subdirectory')
    add("--dry-run", action="store_true", dest="dryrun", default=False,
        help="print generated macro but don't run stitcher")
    add("--verbose", action="count", default=0)

    try:
        args = parser.parse_args()
    except IOError as err:
        parser.error(str(err))
    return args

# only run if we're called explicitly from the commandline or as a plugin from
# Fiji's menu, this allows being imported in the Jython console for testing
# and debugging purposes:
if (__name__ == '__main__'):
    ijlogger = IJLogHandler()
    log.addHandler(ijlogger)
    log.warn("FluoView OIF / OIB stitcher (%s)." % imcf.VERSION)
    log.warn("Arguments (sys.argv): %s" % sys.argv)
    if (len(sys.argv) > 0):
        sys.exit(main_noninteractive())
    else:
        main_interactive()
