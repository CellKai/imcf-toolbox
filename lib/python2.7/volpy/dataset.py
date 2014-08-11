#!/usr/bin/python

"""Classes to handle various types of datasets."""

from os.path import dirname, basename, isdir


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
