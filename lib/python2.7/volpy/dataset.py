#!/usr/bin/python

"""Classes to handle various types of datasets."""

from os.path import dirname, basename, isdir
from log import log


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

        Instance Variables
        ------------------
        ds_type : str
        storage : {'type':str, 'full':str, 'fname':str, 'dname':str}
        """
        log.debug("Creating a 'Dataset' object.")
        ds_type_allowed = ('mosaic', 'stack', 'single')
        st_type_allowed = ('single', 'tree', 'sequence')
        if not ds_type in ds_type_allowed:
            raise TypeError("Illegal dataset type: %s." % ds_type)
        if not st_type in st_type_allowed:
            raise TypeError("Illegal storage type: %s." % st_type)
        self.ds_type = ds_type
        self.storage = {'type': st_type, 'full': st_path}
        if st_type == 'single' and isdir(st_path):
            raise TypeError("File name missing for storage type 'single'.")
        if isdir(st_path):
            self.storage['dname'] = st_path
            self.storage['fname'] = None
        else:
            self.storage['dname'] = dirname(st_path)
            self.storage['fname'] = basename(st_path)


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
        dim = {
            'B': int,  # bit depth
            'C': int,  # channels
            'T': int,  # timepoints
            'X': int,
            'Y': int,
            'Z': int
        }
        """
        super(ImageData, self).__init__(ds_type, st_type, st_path)
        log.debug("Creating an 'ImageData' object.")
        log.debug("ds_type: '%s'" % self.ds_type)
        self.dim = {
            'B': 0,  # bit depth
            'C': 0,  # channels
            'T': 0,  # timepoints
            'X': 0,
            'Y': 0,
            'Z': 0
        }


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
        self.dim = {'X': dim[0], 'Y': dim[1], 'Z': dim[2]}
