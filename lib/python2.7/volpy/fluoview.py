#!/usr/bin/python

"""Tools to process data produced with Olympus FluoView."""

# import numpy as np
# import volpy as vp
import xml.etree.ElementTree as etree
# import misc
from log import log


class FluoViewMosaic(object):

    """Object representing a tiled project from Olympus FluoView.

    TODO: explain
    """

    def __init__(self, infile):
        """Parse all required values from the XML file.

        Instance Variables
        ------------------
        tree : xml.etree.ElementTree
        experiment : dict
        mosaic : list
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
        """Check XML for expected contents."""
        root = self.tree.getroot()
        if not root.tag == 'XYStage':
            raise TypeError('Unexpected value: %s' % root.tag)
        # the statements below raise an AttributeError if no such element was
        # found as a 'NoneType' is returned then:
        self.experiment['xdir'] = root.find('XAxisDirection').text
        self.experiment['ydir'] = root.find('YAxisDirection').text
        self.experiment['mcount'] = root.find('NumberOfMosaics').text
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
            'tiles': images
        })

    def write_tile_config(self, idx):
        """Generate TileConfiguration.txt for Fiji's stitcher."""
        print('# Define the number of dimensions we are working on')
        print('dim = 3')
        print('# Define the image coordinates')
        for img in self.mosaics[idx]['tiles']:
            print('%s; ; (%f, %f, %f)' %
                  (img['imgf'], img['xpos'], img['ypos'], 0))
