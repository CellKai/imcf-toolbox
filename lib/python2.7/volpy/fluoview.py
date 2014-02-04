#!/usr/bin/python

"""Tools to process data produced with Olympus FluoView."""

# import numpy as np
# import volpy as vp
import xml.etree.ElementTree as etree
from os import sep
from os.path import basename, dirname
# import misc
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
    FIXME: example is not conftest-proof!
    >>> import volpy.fluoview as fv
    >>> mosaicfile = '/path/to/some/FluoView/experiment/MATL_Mosaic.log'
    >>> mosaic = fv.FluoViewMosaic(mosaicfile)
    >>> mosaic.write_all_tile_configs()
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

    def write_tile_config(self, idx):
        """Generate TileConfiguration.txt for Fiji's stitcher."""
        # TODO: this method should go into a superclass for generic mosaic type
        # experiments as it will also be required for other input formats
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
        except IOError as err:
            # if reading the OIF fails, we just issue a warning and continue
            # with the next mosaic:
            log.warn('\n*** WARNING *** WARNING *** WARNING ***\n%s' % err)
            log.warn('=====> SKIPPING MOSAIC %i <=====\n' % idx)
            return
        ratio = self.mosaics[idx]['idxratio'] / 100
        for img in self.mosaics[idx]['tiles']:
            xpos = img['xno'] * ratio * size[0]
            ypos = img['yno'] * ratio * size[1]
            # uncomment this to have OS agnostic directory separators:
            # imgf = img['imgf'].replace('\\', sep)
            # fix wrong filenames from stupid Olympus software:
            imgf = img['imgf'].replace('.oif', '_01.oif')
            out.write('%s; ; (%f, %f, %f)\n' % (imgf, xpos, ypos, 0))
        out.close()
        log.warn('Wrote tile config to %s' % out.name)

    def write_all_tile_configs(self):
        """Wrapper to generate all TileConfiguration.txt files."""
        for i in xrange(self.experiment['mcount']):
            self.write_tile_config(i)

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

    def write_stitching_macro(self):
        """Generate a stitching macro template."""
        fname = self.infile['dname'] + '_stitch_all.ijm'
        # for now we're writing to the directory containing the input XML:
        fname = self.infile['path'] + fname
        out = open(fname, 'w')
        out.write('input_dir="FILL_IN";\n')
        out.write('output_dir=input_dir;\n\n')
        out.write('for (id=0; id<%i; id++) {\n' %
                  (self.experiment['mcount'] - 1))
        out.write('    print("===========================================");\n')
        # TODO: padding needs to be done according to the overall number of
        # mosaics, see write_tile_config() above
        out.write('    pad="";\n')
        out.write('    if (id < 10) {\n')
        out.write('        pad="0";\n')
        out.write('    }\n')
        out.write('    print("processing mosaic " + id);\n')
        params  = 'type=[Positions from file] '
        params += 'order=[Defined by TileConfiguration] '
        params += 'directory=" + input_dir + " '
        params += 'layout_file=mosaic_" + pad + id + ".txt '
        params += 'fusion_method=[Linear Blending] '
        params += 'regression_threshold=0.30 '
        params += 'max/avg_displacement_threshold=2.50 '
        params += 'absolute_displacement_threshold=3.50 '
        # TODO: if overlap is below a certain level, we should disable
        # computing the overlap and probably also subpixel accuracy
        params += 'compute_overlap '
        params += 'subpixel_accuracy '
        params += 'computation_parameters='
        params += '[Save computation time (but use more RAM)] '
        params += 'image_output=[Fuse and display]'
        out.write('    run("Grid/Collection stitching", "%s");\n' % params)
        params  = 'save=" + output_dir + "\\\\mosaic_" + pad + id + ".ome.tif '
        params += 'compression=Uncompressed'
        out.write('    run("Bio-Formats Exporter", "%s");\n' % params)
        out.write('    close();\n')
        out.write('}\n')
        out.close()
        log.warn('Wrote macro template to %s' % out.name)
