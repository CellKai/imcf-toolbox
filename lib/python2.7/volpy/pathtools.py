#!/usr/bin/python

"""Helper functions to work with filenames."""

from os import sep
from os.path import basename, dirname


def parse_path(path):
    """Parse a path into its components.

    If the path doesn't end with the pathsep, it is assumed being a file!
    No tests based on existing files are done, as this is supposed to also work
    on path strings that don't exist on the system running this code.

    Example
    -------

    orig : The full path string as given to this function.
    full : Backslashes replaced by the current separator.

    path : 'full' up to the last segment (excluded!), with trailing separator.
    >>> pathtools.parse_path('/tmp/foo/file')['path']
    '/tmp/foo/'
    >>> pathtools.parse_path('/tmp/foo/')['path']
    '/tmp/foo/'

    dname : The last directory of 'full'.
    >>> pathtools.parse_path('/tmp/foo/file')['dname']
    'foo'
    >>> pathtools.parse_path('/tmp/foo/')['dname']
    'foo'

    fname : The filename of 'full', empty in case of a directory.
        '/tmp/foo/file' -> 'file'
        '/tmp/foo/'     -> ''
    >>> pathtools.parse_path('/tmp/foo/file')['fname']
    'file'
    >>> pathtools.parse_path('/tmp/foo/')['fname']
    ''
    """
    parsed = {}
    parsed['orig'] = path
    path = path.replace('\\', sep)
    parsed['full'] = path
    parsed['path'] = dirname(path) + sep
    parsed['fname'] = basename(path)
    parsed['dname'] = basename(dirname(parsed['path']))
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
