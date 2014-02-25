# TODO: present either a GUI to ask the user about the individual steps
# or allow passing all parameters as arguments for this plugin

# explicitly add our libs to the module search path
from java.lang.System import getProperty
from os.path import join
import sys.path
imcfpath = join(getProperty('fiji.dir'), 'plugins', 'IMCF', 'libs')
sys.path.append(imcfpath)


import fluoview as fv
from log import log, set_loglevel
from ij import IJ
from ij.io import DirectoryChooser, OpenDialog
import sys


def ui_get_input_file():
    """Ask user for input file and process results."""
    od = OpenDialog("Choose a 'MATL_Mosaic.log' file")
    fname = od.getFileName()
    if (fname is None):
        log.warn('No input file selected!')
        return((None, None))
    base = od.getDirectory()
    return((base, fname))


def main():
    (base, fname) = ui_get_input_file()
    if (base is None):
        return
    mf = base + fname
    log.warn(mf)
    mosaic = fv.FluoViewMosaic(mf)
    # FIXME: ask user where to put the tile configs
    mosaic.write_all_tile_configs(fixpath=True)
    code = mosaic.gen_stitching_macro_code('stitching', base)
    flat = ""
    for line in code:
        flat += line
    # TODO: ask user how to proceed (show macro, run it, ...)
    print flat
    #IJ.runMacro(flat)

log.debug(fv.__file__)
# set_loglevel(1)
main()
