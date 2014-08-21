#!/usr/bin/python

"""Classes to handle various types of datasets."""

import codecs
import ConfigParser
from os.path import exists

from log import log
from microscopy.pathtools import parse_path


class DataSet(object):

    """The most generic dataset object, to be subclassed and specialized."""

    def __init__(self, ds_type, st_type, st_path):
        """Prepare the dataset object.

        Parameters
        ----------
        ds_type : str
            One of ('mosaic', 'stack', 'single')
        st_type : str
            'single' : a single file container with the full dataset
            'tree' : a directory hierarchy
            'sequence' : a sequence of files
        st_path : str
            The full path to either a file or directory, depending on the
            storage type of this dataset.
        supplement : dict
            An auxiliary dict to keep supplementary information.

        Instance Variables
        ------------------
        ds_type : str
        storage : pathtools.parse_path
        """
        log.debug("Creating a 'Dataset' object.")
        ds_type_allowed = ('mosaic', 'stack', 'single')
        st_type_allowed = ('single', 'tree', 'sequence')
        if not ds_type in ds_type_allowed:
            raise TypeError("Illegal dataset type: %s." % ds_type)
        if not st_type in st_type_allowed:
            raise TypeError("Illegal storage type: %s." % st_type)
        self.ds_type = ds_type
        self.storage = parse_path(st_path)
        self.storage['type'] = st_type
        if st_type == 'single' and self.storage['fname'] == '':
            raise TypeError("File name missing for storage type 'single'.")
        self.supplement = {}


class ImageData(DataSet):

    """Specific DataSet class for images, 2D to 5D."""

    def __init__(self, ds_type, st_type, st_path):
        """Set up the image dataset object.

        Parameters
        ----------
        ds_type : str
            One of ('mosaic', 'stack', 'single')
        st_type : str
            'single' : a single file container with the full dataset
            'tree' : a directory hierarchy
            'sequence' : a sequence of files
        st_path : str
            The full path to either a file or directory, depending on the
            storage type of this dataset.

        Instance Variables
        ------------------
        _dim = {
            'B': int,  # bit depth
            'C': int,  # channels
            'T': int,  # timepoints
            'X': int,
            'Y': int,
            'Z': int
        }
        position : dict
            Spatial information for multi-image datasets:
            {
                'stage' : (float, float),    # raw stage coords
                'relative' : (float, float)  # relative coords in pixels
            }
        """
        super(ImageData, self).__init__(ds_type, st_type, st_path)
        log.debug("Creating an 'ImageData' object.")
        log.debug("ds_type: '%s'" % self.ds_type)
        self._dim = {
            'B': 0,  # bit depth
            'C': 0,  # channels
            'T': 0,  # timepoints
            'X': 0,
            'Y': 0,
            'Z': 0
        }
        self.position = {      # spatial information for multi-image datasets
            'stage': None,    # raw stage coordinates
            'relative': None  # relative coordinates in pixel values (float)
        }

    def set_stagecoords(self, coords):
        """Set the stageinfo coordinates for this object."""
        log.info("Setting stage coordinates: %s." % str(coords))
        self.position['stage'] = coords

    def set_relpos(self, coords):
        """Set the relative coordinates in pixels for this object."""
        log.info("Setting relative coordinates: %s." % str(coords))
        self.position['relative'] = coords

    def set_tilenumbers(self, tileno_x, tileno_y, tileno_z=None):
        """Set the tile number in the supplementary informations."""
        log.info("Tile numbers: %s,%s,%s." % (tileno_x, tileno_y, tileno_z))
        self.supplement['tileno'] = (tileno_x, tileno_y, tileno_z)

    def get_dimensions(self):
        """Lazy parsing of the image dimensions."""
        raise NotImplementedError('get_dimensions() not implemented!')


class ImageDataOIF(ImageData):

    """Specific DataSet class for images in Olympus OIF format."""

    def __init__(self, st_path):
        """Set up the image dataset object.

        Parameters
        ----------
        st_path : str
            The full path to the .OIF file.

        Instance Variables
        ------------------
        For inherited variables, see ImageData.
        """
        log.debug("ImageDataOIF(%s)" % st_path)
        super(ImageDataOIF, self).__init__('stack', 'tree', st_path)
        self.storage = self.validate_oifpath()
        self.parser = self.setup_parser()
        self._dim = None  # override _dim to mark it as not yet known

    def validate_oifpath(self):
        """Fix the broken .oif paths in FluoView experiment files.

        The FluoView software usually stores corrupted filenames in its
        experiment description files, that have a missing suffix, e.g.

            Slide1sec001\\Slide1sec001.oif

        whereas the correct filename would be

            Slide1sec001\\Slide1sec001_01.oif

        This function attempts to fix this by checking if the supplied path is
        actually existing and trying the default suffix if not. Raises an
        IOError exception if no corresponding file can be found.

        Returns
        -------
        storage : pathtools.parse_path
        """
        oif = self.storage
        log.debug("Validating oif path: %s" % oif)
        if not exists(oif['full']):
            oif = parse_path(oif['orig'].replace('.oif', '_01.oif'))
            log.debug("Trying next path: %s" % oif['full'])
        if not exists(oif['full']):
            raise IOError("Can't find OIF file: %s" % oif)
        return oif

    def setup_parser(self):
        """Set up the ConfigParser object for this .oif file.

        Use the 'codecs' package to set up a ConfigParser object that can
        properly handle the UTF-16 encoded .oif files.
        """
        # TODO: investigate usage of 'io' package instead of 'codecs'
        oif = self.storage['full']
        log.info('Parsing OIF file: %s' % oif)
        try:
            conv = codecs.open(oif, "r", "utf16")
        except IOError:
            raise IOError("Error parsing OIF file (does it exist?): %s" % oif)
        parser = ConfigParser.RawConfigParser()
        parser.readfp(conv)
        conv.close()
        log.debug('Finished parsing OIF file.')
        return parser

    def parse_dimensions(self):
        """Read image dimensions from a ConfigParser object.

        Returns
        -------
        dim : (int, int)
            Pixel dimensions in X and Y direction as tuple.
        """
        get = self.parser.get
        try:
            dim_b = get(u'Reference Image Parameter', u'ValidBitCounts')
            dim_x = get(u'Reference Image Parameter', u'ImageHeight')
            dim_y = get(u'Reference Image Parameter', u'ImageWidth')
            dim_z = get(u'Axis 3 Parameters Common', u'MaxSize')
            axis_z = get(u'Axis 3 Parameters Common', u'AxisName')
            dim_c = get(u'Axis 2 Parameters Common', u'MaxSize')
            axis_c = get(u'Axis 2 Parameters Common', u'AxisName')
            dim_t = get(u'Axis 4 Parameters Common', u'MaxSize')
            axis_t = get(u'Axis 4 Parameters Common', u'AxisName')
        except ConfigParser.NoOptionError as err:
            raise ValueError("Error parsing dimensions from %s: %s" %
                             (self.storage['full'], err))
        # check if we got the right axis for Z/Ch/T, set to 0 otherwise:
        if not axis_z == u'"Z"':
            log.warn("WARNING: couldn't find Z axis in metadata!")
            dim_z = 0
        if not axis_c == u'"Ch"':
            log.warn("WARNING: couldn't find channels in metadata!")
            dim_c = 0
        if not axis_t == u'"T"':
            log.warn("WARNING: couldn't find timepoints in metadata!")
            dim_t = 0
        dim = {
            'B': int(dim_b),  # bit depth
            'C': int(dim_c),  # channels
            'T': int(dim_t),  # timepoints
            'X': int(dim_x),
            'Y': int(dim_y),
            'Z': int(dim_z)
        }
        log.info('Parsed image dimensions: %s' % dim)
        return dim

    def get_dimensions(self):
        """Lazy parsing of the image dimensions."""
        if self._dim is None:
            self._dim = self.parse_dimensions()
        return self._dim

    def set_relpos(self, overlap):
        """Set the relative coordinates in pixels for this object.

        Parameters
        ----------
        overlap : float
            The overlap between tiles in percent.
        """
        ratio = (100.0 - overlap) / 100
        size_x = self.get_dimensions()['X']
        size_y = self.get_dimensions()['Y']
        tileno_x = self.supplement['tileno'][0]
        tileno_y = self.supplement['tileno'][1]
        pos_x = size_x * ratio * tileno_x
        pos_y = size_y * ratio * tileno_y
        log.info("Setting relative coordinates: %s, %s." % (pos_x, pos_y))
        self.position['relative'] = (pos_x, pos_y)


class MosaicData(DataSet):

    """Special DataSet class for mosaic / tiling datasets."""

    def __init__(self, st_type, st_path):
        """Set up the mosaic dataset object.

        Parameters
        ----------
        st_type, st_path : see superclass

        Instance Variables
        ------------------
        subvol : list(ImageData)
        """
        super(MosaicData, self).__init__('mosaic', st_type, st_path)
        self.subvol = list()

    def add_subvol(self, img_ds):
        """Add a subvolume to this dataset."""
        log.debug('Dataset type: %s' % type(img_ds))
        self.subvol.append(img_ds)


class MosaicDataCuboid(MosaicData):

    """Special case of a full cuboid mosaic volume."""

    def __init__(self, st_type, st_path, dim):
        """Set up the mosaic dataset object.

        Parameters
        ----------
        st_type, st_path : see superclass
        dim : list(int, int, int)
            Number of sub-volumes (stacks) in all spatial dimensions.

        Instance Variables
        ------------------
        subvol : list(ImageData)
        dim = {
            'X': int,  # number of sub-volumes in X-direction
            'Y': int,  # number of sub-volumes in Y-direction
            'Z': int   # number of sub-volumes in Z-direction
        }
        """
        super(MosaicDataCuboid, self).__init__(st_type, st_path)
        log.info('Mosaic: %ix%ix%i' % (dim[0], dim[1], dim[2]))
        self.dim = {'X': dim[0], 'Y': dim[1], 'Z': dim[2]}
        self.overlap = 0
        self.overlap_units = 'px'

    def set_overlap(self, value, units='px'):
        """Set the overlap amount and unit."""
        units_allowed = ['px', 'pct', 'um', 'nm', 'mm']
        if units not in units_allowed:
            raise TypeError('Unknown overlap unit given: %s' % units)
        # TODO: this warning should be displayed for other units as well
        if units == 'pct' and value <= 5.0:
            log.warn('Low overlap %.1f%%!' % value)
        self.overlap = value
        self.overlap_units = units

    def get_overlap(self, units='pct'):
        """Get the overlap amount in a specific unit."""
        # TODO: implement conversion for other units:
        # units_allowed = ['px', 'pct', 'um', 'nm', 'mm']
        units_allowed = ['pct']
        if units not in units_allowed:
            raise TypeError('Unknown overlap unit requested: %s' % units)
        if units != self.overlap_units:
            raise NotImplementedError('Unit conversion not implemented!')
        return self.overlap
