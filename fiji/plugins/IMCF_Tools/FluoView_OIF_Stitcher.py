"""Fiji plugin for stitching FluoView mosaics in OIF format."""

# TODO: allow passing all parameters as arguments for this plugin

# explicitly add our libs to the module search path
from java.lang.System import getProperty
from os.path import join
import sys
sys.path.append(join(getProperty('fiji.dir'), 'plugins', 'IMCF', 'libs'))


from ij import IJ
from ij.io import OpenDialog
from ij.gui import GenericDialog

import fluoview as fv
from log import log, set_loglevel


def ui_get_input_file():
    """Ask user for input file and process results."""
    dialog = OpenDialog("Choose a 'MATL_Mosaic.log' file")
    fname = dialog.getFileName()
    if (fname is None):
        log.warn('No input file selected!')
        return((None, None))
    base = dialog.getDirectory()
    return((base, fname))


def flatten(lst):
    """Make a single string from a list of strings."""
    # TODO: move to misc package
    flat = ""
    for line in lst:
        flat += line
    return(flat)


def gen_mosaic_details(mosaics):
    """Generate human readable string of details about the parsed mosaics."""
    # TODO: could go into fluoview package
    msg = ""
    mcount = mosaics.experiment['mcount']
    msg += "Parsed a total of %i mosaics from the logfile.\n \n" % mcount
    for mos in mosaics.mosaics:
        msg += "Mosaic %i: " % mos['id']
        msg += "%i x %i tiles, " % (mos['xcount'], mos['ycount'])
        msg += "%i%% overlap.\n" % int(100 - mos['ratio'])
    return(msg)


def main():
    """The main program workflow."""
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

# set_loglevel(1)
log.debug(fv.__file__)
sys.exit(main())
