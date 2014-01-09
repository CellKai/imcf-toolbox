#!/usr/bin/python

"""Tools to process data produced with Olympus FluoView."""

# import numpy as np
# import volpy as vp
import xml.etree.ElementTree as etree
import os
# import misc
from log import log


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

    TODO: explain what the class provides, add examples?
    """

    def __init__(self, infile):
        """Parse all required values from the XML file.

        Instance Variables
        ------------------
        tree : xml.etree.ElementTree
        experiment : dict({'mcount': int, # number of mosaics
                           'xdir': str,   # X axis direction
                           'ydir': str    # Y axis direction
                         })
        mosaics : list
        """
        log.info('Reading FluoView Mosaic XML...')
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
        """Parse a mosaic section and assemble a dict from it."""
        idx = int(mosaic.attrib['No'])
        assert mosaic.find('XScanDirection').text == 'LeftToRight'
        assert mosaic.find('YScanDirection').text == 'TopToBottom'
        xcount = int(mosaic.find('XImages').text)
        ycount = int(mosaic.find('YImages').text)
        xidx = float(mosaic.find('XIndex').text)
        yidx = float(mosaic.find('YIndex').text)
        idxratio = float(mosaic.find('IndexRatio').text)
        print('Mosaic %i: %ix%i' % (idx, xcount, ycount))
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
        out = open('mosaic_%02i.txt' % idx, 'w')
        out.write('# Define the number of dimensions we are working on\n')
        out.write('dim = 3\n')
        out.write('# Define the image coordinates (in pixels)\n')
        # TODO: parse tile size from image data instead of hardcoding it!
        size = 800
        ratio = self.mosaics[idx]['idxratio'] / 100
        for img in self.mosaics[idx]['tiles']:
            xpos = img['xno'] * ratio * size
            ypos = img['yno'] * ratio * size
            # uncomment this to have OS agnostic directory separators:
            # imgf = img['imgf'].replace('\\', os.sep)
            # fix wrong filenames from stupid Olympus software:
            imgf = img['imgf'].replace('.oif', '_01.oif')
            out.write('%s; ; (%f, %f, %f)\n' % (imgf, xpos, ypos, 0))
        out.close()
