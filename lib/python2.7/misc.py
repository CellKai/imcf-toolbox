#!/usr/bin/python

"""Module providing various helper functions."""

# TODO: make this Python2.5 compliant for Jython (*sigh*)

from log import log


# this is taken from numpy's iotools:
def _is_string_like(obj):
    """Check whether obj behaves like a string.

    Using this way of checking for a string-like object is more robust when
    dealing with stuff that can behave like a 'str' but is not strictly an
    instance of it (or a subclass thereof). So it's more generic than using
    isinstance(obj, str).

    Example
    -------
    >>> _is_string_like('foo')
    True
    >>> _is_string_like(123)
    False
    """
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    return True


def filehandle(fname, mode='r'):
    """Make sure a variable is either a filehandle or create one from it.

    This function takes a variable and checks whether it is already a
    filehandle with the desired mode or a string that can be turned into a
    filehandle with that mode. This can be used e.g. to make functions agnostic
    against being supplied a file-type parameter that was gathered via argparse
    (then it's already a filehandle) or as a plain string.

    Parameters
    ----------
    fname : str or filehandle
    mode : str
        The desired mode of the filehandle (default=read).

    Returns
    -------
    A valid (open) filehandle with the given mode. Raises an IOError
    otherwise.

    Example
    -------
    >>> fname = __file__
    >>> type(fname)
    <type 'str'>
    >>> type(filehandle(fname))
    <type 'file'>
    >>> fh = open(__file__, 'r')
    >>> type(fh)
    <type 'file'>
    >>> type(filehandle(fh))
    <type 'file'>
    """
    log.debug(type(fname))
    if (type(fname).__name__ == 'str'):
        try:
            return open(fname, mode)
        except IOError as err:
            message = "can't open '%s': %s"
            raise SystemExit(message % (fname, err))
    elif (type(fname).__name__ == 'file'):
        if (fname.mode != mode):
            message = "mode mismatch: %s != %s"
            raise IOError(message % (fname.mode, mode))
        return fname
    else:
        message = "unknown data type (expected string or filehandle): %s"
        raise SystemExit(message % type(fname))


def filename(name):
    """Get the filename from either a filehandle or a string.

    This is a convenience function to retrieve the filename as a string given
    either an open filehandle or just a plain str containing the name.

    Parameters
    ----------
    name : str or filehandle

    Returns
    -------
    name : str

    Example
    -------
    >>> filename('test_file_name')
    'test_file_name'
    >>> filename(open(__file__, 'r'))
    'misc.py'
    """
    if isinstance(name, file):
        return name.name
    elif _is_string_like(name):
        return name
    else:
        raise TypeError


if __name__ == "__main__":
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
