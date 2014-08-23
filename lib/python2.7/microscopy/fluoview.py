#!/usr/bin/python

"""Tools to process data produced with Olympus FluoView."""

import xml.etree.ElementTree as etree
from log import log

from microscopy.experiment import MosaicExperiment
from microscopy.dataset import MosaicDataCuboid, ImageDataOIF


class FluoViewOIFMosaic(MosaicExperiment):

    """Object representing a tiled ("mosaic") project from Olympus FluoView.

    Olympus FluoView creates a "MATL_Mosaic.log" file for each tiled project.
    The file contains XML (no specifications given), describing some generic
    settings like axis directions, number of mosaics, and some more.
    After the generic section, every mosaic (a set of tiles belonging together)
    is described in detail (number of tiles in x and y direction, overlap,
    stage positions, file names and positions of each of the mosaic's tiles).

    Please note that multiple mosaics are contained in these project files and
    each of the mosaics can have different properties.

    Example
    -------
    >>> import volpy.fluoview as fv
    >>> from log import set_loglevel
    >>> set_loglevel(3)
    >>> mosaic = fv.FluoViewMosaic('TESTDATA/mosaic/MATL_Mosaic.log')
    >>> mosaic.experiment['mcount']
    1
    >>> mosaic.experiment['xdir']
    'LeftToRight'
    >>> mosaic.mosaics[0]['tiles'][0]['imgf']
    'Slide1sec001\\\\Slide1sec001.oif'
    >>> mosaic.write_all_tile_configs()
    >>> code = mosaic.gen_stitching_macro_code('stitching')
    >>> mosaic.write_stitching_macro(code)
    """

    def __init__(self, infile):
        """Parse all required values from the XML file.

        Instance Variables
        ------------------
        tree : xml.etree.ElementTree
        supplement : {'mcount': int, # highest index reported by FluoView
                      'xdir': str,   # X axis direction
                      'ydir': str    # Y axis direction
                     }
        """
        super(FluoViewOIFMosaic, self).__init__(infile)
        self.tree = self.validate_xml()
        self.add_mosaics()

    def validate_xml(self):
        """Parse and check XML for being a valid FluoView mosaic experiment.

        Evaluate the XML tree for known elements like the root tag (expected to
        be "XYStage", and some of the direct children to make sure the parsed
        file is in fact a FluoView mosaic XML file. Raises exceptions in case
        something expected can't be found in the tree.

        Returns
        -------
        tree : xml.etree.ElementTree
        """
        log.info('Validating FluoView Mosaic XML...')
        tree = etree.parse(self.infile['full'])
        root = tree.getroot()
        if not root.tag == 'XYStage':
            raise TypeError('Unexpected value: %s' % root.tag)
        # find() raises an AttributeError if no such element is found:
        xdir = root.find('XAxisDirection').text
        ydir = root.find('YAxisDirection').text
        # WARNING: 'mcount' is the HIGHEST INDEX number, not the total count!
        mcount = int(root.find('NumberOfMosaics').text)
        # currently we only support LTR and TTB experiments:
        if xdir != 'LeftToRight' or ydir != 'TopToBottom':
            raise TypeError('Unsupported Axis configuration')
        self.supplement = {
            'xdir': xdir,
            'ydir': ydir,
            'mcount': mcount
        }
        log.info('Finished validating XML.')
        return tree

    def add_mosaics(self):
        """Parse a list of XML subtrees and create MosaicDatasets from them.

        Old datastructure
        -----------------
        This is the previously used datastructure, for documentation purposes.

        mosaic : {'id': int,
                  'ratio': float,  # non-overlapping tile percentage
                  'xcount': int,   # number of tiles in X
                  'ycount': int,   # number of tiles in Y
                  'tiles': [{
                             'imgf': str,    # tile filename
                             'imgid': int,   # tile ID
                             'xno': int,     # tile index in X direction
                             'yno': int,     # tile index in Y direction
                             'xpos': float,  # tile position in X direction
                             'ypos': float   # tile position in Y direction
                           }]
                 }
        """
        for tree in self.tree.getroot().findall('Mosaic'):
            # lambda functions for tree.find().text and int/float conversions:
            tft = lambda p: tree.find(p).text
            tfi = lambda p: int(tft(p))
            tff = lambda p: float(tft(p))
            idx = int(tree.attrib['No'])
            assert tft('XScanDirection') == 'LeftToRight'
            assert tft('YScanDirection') == 'TopToBottom'

            # assemble the dataset (MosaicDataCuboid):
            # use the infile for the mosaic_ds infile as well as individual
            # mosaics don't have separate project files in our case
            mosaic_ds = MosaicDataCuboid('tree', self.infile['orig'],
                                         (tfi('XImages'), tfi('YImages'), 1))
            mosaic_ds.set_overlap(100.0 - tff('IndexRatio'), 'pct')
            mosaic_ds.supplement['index'] = idx

            # Parsing and assembling the ImageData section should be considered
            # to be moved into a separate method.
            # ImageData section:
            for img in tree.findall('ImageInfo'):
                tft = lambda p: img.find(p).text
                tfi = lambda p: int(img.find(p).text)
                tff = lambda p: float(img.find(p).text)
                try:
                    oif_ds = ImageDataOIF(self.infile['path']
                                          + tft('Filename'))
                    oif_ds.set_stagecoords((tff('XPos'), tff('YPos')))
                    oif_ds.set_tilenumbers(tfi('Xno'), tfi('Yno'))
                    oif_ds.set_relpos(mosaic_ds.get_overlap('pct'))
                    oif_ds.supplement['index'] = tfi('No')
                    mosaic_ds.add_subvol(oif_ds)
                except IOError as err:
                    log.info('Broken/missing image data: %s' % err)
                    mosaic_ds = None
            if mosaic_ds is not None:
                self.add_dataset(mosaic_ds)
            else:
                log.warn('Mosaic %s: incomplete subvolumes, SKIPPING!' % idx)


if __name__ == "__main__":
    print('Running doctest on file "%s".' % __file__)
    import doctest
    import sys
    VERB = '-v' in sys.argv
    doctest.testmod(verbose=VERB)
