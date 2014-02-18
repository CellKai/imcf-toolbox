#!/usr/bin/python

"""Tools to process data produced with Olympus FluoView."""

import xml.etree.ElementTree as etree
from os import sep
from os.path import basename, dirname
from log import log
import ConfigParser
import codecs


class FluoViewMosaic(object):

    """Object representing a tiled ("mosaic") project from Olympus FluoView.

    Olympus FluoView creates a "MATL_Mosaic.log" file for each tiled project.
    The file contains XML (no specifications given), describing some generic
    settings like axis directions, number of mosaics, and some more.
    After the generic section, every mosaic (a set of tiles belonging together)
    is described in detail (number of tiles in x and y direction, overlap,
    stage positions, file names and positions of each of the mosaic's tiles).

    Please note that multiple mosaics are contained in these project files and
    each of the mosaics can have different properties.

    TODO: explain what the class provides

    Example
    -------
    >>> import volpy.fluoview as fv
    >>> from log import set_loglevel
    >>> set_loglevel(3)
    >>> mosaicfile = 'TESTDATA/mosaic/MATL_Mosaic.log'
    >>> mosaic = fv.FluoViewMosaic(mosaicfile)
    >>> mosaic.experiment['mcount']
    1
    >>> mosaic.experiment['xdir']
    'LeftToRight'
    >>> mosaic.mosaics[0]['tiles'][0]['imgf']
    'Slide1sec001\\\\Slide1sec001.oif'
    >>> mosaic.write_all_tile_configs()
    >>> code = mosaic.gen_stitching_macro_code('ijm_templates/stitching')
    >>> mosaic.write_stitching_macro(code)
    """

    def __init__(self, infile):
        """Parse all required values from the XML file.

        Instance Variables
        ------------------
        infile : {'path': str,    # path to input XML file
                  'dname': str,   # the directory name (last part of 'path')
                  'fname': str,   # the input XML filename
                 }
        tree : xml.etree.ElementTree
        experiment : dict({'mcount': int, # number of mosaics
                           'xdir': str,   # X axis direction
                           'ydir': str    # Y axis direction
                         })
        mosaics : list of mosaics (dicts, see parse_mosaic)
        """
        log.info('Reading FluoView Mosaic XML...')
        self.infile = {}
        self.infile['path'] = dirname(infile).replace('\\', sep) + sep
        self.infile['dname'] = basename(dirname(self.infile['path']))
        self.infile['fname'] = basename(infile)
        # a dictionary of experiment-wide settings
        self.experiment = {}
        # a list of dicts with mosaic specific settings
        self.mosaics = []
        self.tree = etree.parse(infile)
        self.check_fvxml()
        self.parse_all_mosaics()
        log.info('Done.')

    def check_fvxml(self):
        """Check XML for being a valid FluoView mosaic experiment file.

        Evaluate the XML tree for known elements like the root tag (expected to
        be "XYStage", and some of the direct children to make sure the parsed
        file is in fact a FluoView mosaic XML file.
        """
        root = self.tree.getroot()
        if not root.tag == 'XYStage':
            raise TypeError('Unexpected value: %s' % root.tag)
        # the statements below raise an AttributeError if no such element was
        # found as a 'NoneType' is returned then:
        self.experiment['xdir'] = root.find('XAxisDirection').text
        self.experiment['ydir'] = root.find('YAxisDirection').text
        # FIXME: mcount is WRONG, it gives the index number of the last mosaic
        # in the project, but a project might e.g. only contain mosaics number
        # 5 and 6 (so "2" would be correct but mcount is "6"):
        self.experiment['mcount'] = int(root.find('NumberOfMosaics').text)
        # currently we only support LTR and TTB experiments:
        if not self.experiment['xdir'] == 'LeftToRight':
            raise TypeError('Unsupported XAxis configuration')
        if not self.experiment['ydir'] == 'TopToBottom':
            raise TypeError('Unsupported YAxis configuration')

    def parse_all_mosaics(self):
        """Wrapper to parse all mosaic parts."""
        for mosaic in self.tree.getroot().findall('Mosaic'):
            self.parse_mosaic(mosaic)

    def parse_mosaic(self, mosaic):
        """Parse a mosaic section and assemble a dict from it.

        Generate a dict from a mosaic and append it to the object's mosaics
        list. The dict has the following format:

        mosaic : dict({'id': int,
                       'idxratio': float,
                       'tiles': tiles
                     })

        tiles : list(dict({'imgf': str,    # tile filename
                           'imgid': int,   # tile ID
                           'xno': int,     # tile index in X direction
                           'xpos': float,  # tile position in X direction
                           'yno': int,     # tile index in Y direction
                           'ypos': float   # tile position in Y direction
                         }))
        """
        idx = int(mosaic.attrib['No'])
        assert mosaic.find('XScanDirection').text == 'LeftToRight'
        assert mosaic.find('YScanDirection').text == 'TopToBottom'
        xcount = int(mosaic.find('XImages').text)
        ycount = int(mosaic.find('YImages').text)
        xidx = float(mosaic.find('XIndex').text)
        yidx = float(mosaic.find('YIndex').text)
        idxratio = float(mosaic.find('IndexRatio').text)
        log.info('Mosaic %i: %ix%i' % (idx, xcount, ycount))
        # warn if overlap is below 5 percent:
        if (idxratio > 95.0):
            log.warn('WARNING: overlap of mosaic %i is only %.1f%%!' %
                     (idx, (100.0 - idxratio)))
        images = []
        for img in mosaic.findall('ImageInfo'):
            info = {
                'imgid': int(img.find('No').text),
                'xpos': float(img.find('XPos').text),
                'ypos': float(img.find('YPos').text),
                'xno': int(img.find('Xno').text),
                'yno': int(img.find('Yno').text),
                'imgf': img.find('Filename').text
            }
            images.append(info)
        self.mosaics.append({
            'id': idx,
            'xcount': xcount,
            'ycount': ycount,
            'xidx': xidx,
            'yidx': yidx,
            'idxratio': idxratio,
            'tiles': images
        })

    def write_tile_config(self, idx, fixpath=False):
        """Generate TileConfiguration.txt for Fiji's stitcher.

        Generate a layout configuration file for a ceartain mosaic in the
        format readable by Fiji's "Grid/Collection stitching" plugin. The
        configuration is stored in a file in the input directory carrying the
        mosaic's index number as a suffix.

        Parameters
        ----------
        idx : int  --  The index of the mosaic to create the tile config for.
        fixpath : bool  --  Whether to adjust the path separators.
        """
        # TODO: this method should go into a superclass for generic mosaic type
        # experiments as it will also be required for other input formats
        # TODO: split into two functions: generating and writing
        # filename is zero-padded to the total number of mosaics:
        fname = 'mosaic_%0*i.txt' % (len(str(len(self.mosaics))), idx)
        # for now we're writing to the directory containing the input XML:
        fname = self.infile['path'] + fname
        out = open(fname, 'w')
        out.write('# Define the number of dimensions we are working on\n')
        out.write('dim = 3\n')
        out.write('# Define the image coordinates (in pixels)\n')
        try:
            size = self.dim_from_oif(self.mosaics[idx]['tiles'][0]['imgf'])
        except IOError, err:
            # if reading the OIF fails, we just issue a warning and continue
            # with the next mosaic:
            log.warn('\n*** WARNING *** WARNING *** WARNING ***\n%s' % err)
            log.warn('=====> SKIPPING MOSAIC %i <=====\n' % idx)
            return
        ratio = self.mosaics[idx]['idxratio'] / 100
        for img in self.mosaics[idx]['tiles']:
            xpos = img['xno'] * ratio * size[0]
            ypos = img['yno'] * ratio * size[1]
            # fix wrong filenames from stupid Olympus software:
            imgf = img['imgf'].replace('.oif', '_01.oif')
            if(fixpath):
                imgf = imgf.replace('\\', sep)
            out.write('%s; ; (%f, %f, %f)\n' % (imgf, xpos, ypos, 0))
        out.close()
        log.warn('Wrote tile config to %s' % out.name)

    def write_all_tile_configs(self, fixpath=False):
        """Wrapper to generate all TileConfiguration.txt files."""
        for i in xrange(self.experiment['mcount']):
            self.write_tile_config(i, fixpath)

    def dim_from_oif(self, oif):
        """Read image dimensions from a .oif file.

        Parameters
        ----------
        oif : str
            The .oif file to read the dimensions from.

        Returns
        -------
        dim : (int, int)
            Pixel dimensions in X and Y direction as tuple.
        """
        oif = oif.replace('\\', sep)
        oif = oif.replace('.oif', '_01.oif')
        oif = self.infile['path'] + oif
        log.debug('Parsing OIF file for dimensions: %s' % oif)
        # we're using ConfigParser which can't handle UTF-16 (and UTF-8) files
        # properly, so we need the help of "codecs" to parse the file
        try:
            conv = codecs.open(oif, "r", "utf16")
        except IOError:
            raise IOError("Can't find required OIF file for parsing image" +
                          " dimensions: %s" % oif)
        parser = ConfigParser.RawConfigParser()
        parser.readfp(conv)
        try:
            dim_h = parser.get(u'Reference Image Parameter', u'ImageHeight')
            dim_w = parser.get(u'Reference Image Parameter', u'ImageWidth')
        except ConfigParser.NoOptionError:
            raise ValueError("Can't read image dimensions from %s." % oif)
        dim = (int(dim_w), int(dim_h))
        log.warn('Dimensions: %s %s' % dim)
        return dim

    def gen_stitching_macro_code(self, pfx):
        """Generate code in ImageJ's macro language to stitch the mosaics.

        Take two template files ("head" and "body") and generate an ImageJ
        macro to stitch the mosaics. Using the splitted templates allows for
        setting default values in the body that can be overridden in this
        generator method (the ImageJ macro language doesn't have a command to
        check if a variable is set or not, it just exits with an error).

        Parameters
        ----------
        pfx : str
            The prefix for the two template files, will be completed with the
            corresponding suffixes "_head.ijm" and "_body.ijm".

        Returns
        -------
        ijm : list(str)
            The generated macro code as a list of str (one str per line).
        """
        # TODO: this method is a candidate for a mosaic superclass
        mcount = self.experiment['mcount']
        tpl = open(pfx + '_head.ijm', 'r')
        ijm = tpl.readlines()
        tpl.close()
        ijm.append('\n')

        ijm.append('name="%s";\n' % self.infile['dname'])
        ijm.append('padlen=%i;\n' % len(str(mcount)))
        ijm.append('mcount=%i;\n' % mcount)
        ijm.append('input_dir="";\n')
        ijm.append('use_batch_mode=true;\n')

        # If the overlap is below a certain level (5 percent), we disable
        # computing the actual positions and subpixel accuracy:
        if (self.mosaics[0]['idxratio'] > 95.0):
            ijm.append('compute = false;\n')

        ijm.append('\n')
        tpl = open(pfx + '_body.ijm', 'r')
        ijm += tpl.readlines()
        tpl.close()
        log.debug('--- ijm ---\n%s\n--- ijm ---' % ijm)
        return(ijm)

    def write_stitching_macro(self, code, fname=None, dname=None):
        """Write generated macro code into a file."""
        if fname is None:
            fname = self.infile['dname'] + '_stitch_all.ijm'
        if dname is None:
            # if not requested other, write to input directory:
            fname = self.infile['path'] + sep + fname
        else:
            fname = dname + fname
        out = open(fname, 'w')
        out.writelines(code)
        out.close()
        log.warn('Wrote macro template to %s' % out.name)


if __name__ == "__main__":
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
