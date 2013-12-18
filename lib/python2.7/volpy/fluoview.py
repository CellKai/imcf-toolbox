#!/usr/bin/python

"""Tools to process data produced with Olympus FluoView."""

# import numpy as np
# import volpy as vp
import xml.etree.ElementTree as etree
import os
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
        print('# Define the number of dimensions we are working on')
        print('dim = 3')
        print('# Define the image coordinates (in pixels)')
        # TODO: parse tile size from image data instead of hardcoding it!
        size = 1024
        ratio = self.mosaics[idx]['idxratio'] / 100
        for img in self.mosaics[idx]['tiles']:
            xpos = img['xno'] * ratio * size
            ypos = img['yno'] * ratio * size
            # make sure to have OS agnostic directory separators:
            imgf = img['imgf'].replace('\\', os.sep)
            print('%s; ; (%f, %f, %f)' % (imgf, xpos, ypos, 0))
