#!/usr/bin/python

"""Helper functions to work with filenames."""

from os import sep
import os.path


def parse_path(path):
    """Parse a path into its components.

    If the path doesn't end with the pathsep, it is assumed being a file!
    No tests based on existing files are done, as this is supposed to also work
    on path strings that don't exist on the system running this code.

    Returns
    -------
    parsed = {
        'orig' : str   # string as passed into this function
        'full' : str   # separators adjusted to current platform
        'path' : str   # like previous, up to (including) the last separator
        'dname' : str  # segment between the last two separators (directory)
        'fname' : str  # segment after the last separator (filename)
    }

    Example
    -------

    >>> path_to_file = pathtools.parse_path('/tmp/foo/file')
    >>> path_to_dir = pathtools.parse_path('/tmp/foo/')

    orig : The full path string as given to this function.
    full : Backslashes replaced by the current separator.

    path : 'full' up to the last separator (included)
    >>> path_to_file['path']
    '/tmp/foo/'
    >>> path_to_dir['path']
    '/tmp/foo/'

    dname : The last directory of the path in 'full'.
    >>> path_to_file['dname']
    'foo'
    >>> path_to_dir['dname']
    'foo'

    fname : The filename of 'full', empty in case of a directory.
    >>> path_to_file['fname']
    'file'
    >>> path_to_dir['fname']
    ''
    """
    parsed = {}
    parsed['orig'] = path
    path = path.replace('\\', sep)
    parsed['full'] = path
    parsed['path'] = os.path.dirname(path) + sep
    parsed['fname'] = os.path.basename(path)
    parsed['dname'] = os.path.basename(os.path.dirname(parsed['path']))
    return parsed


if __name__ == "__main__":
    # pylint: disable-msg=W0611
    # pylint: disable-msg=W0406
    print('Running doctest on file "%s".' % __file__)
    import doctest
    import sys
    from volpy import pathtools
    VERB = '-v' in sys.argv
    doctest.testmod(verbose=VERB)
