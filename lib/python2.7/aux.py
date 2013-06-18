#!/usr/bin/python

from log import log

def check_filehandle(filename, mode):
    '''Make sure a variable is either a filehandle or create one from it.
    .
    This function takes a variable and checks whether it is already a
    filehandle with the desired mode or a string that can be turned into
    a filehandle with that mode. This can be used e.g. to make functions
    agnostic against being supplied a file-type parameter that was gathered
    via argparse (then it's already a filehandle) or as a plain string.
    .
    Parameters
    ----------
    filename : str or filehandle
    mode : str
        The desired mode of the filehandle.
    .
    Returns
    -------
    A valid (open) filehandle with the given mode. Raises an IOError
    otherwise.
    '''
    log.debug(type(filename))
    if (type(filename).__name__ == 'str'):
        try:
            return open(filename, mode)
        except IOError as e:
            message = "can't open '%s': %s"
            raise SystemExit(message % (filename, e))
    elif (type(filename).__name__ == 'file'):
        if (filename.mode != mode):
            message = "mode mismatch: %s != %s"
            raise IOError(message % (filename.mode, mode))
        return filename
    else:
        message = "unknown data type (expected string or filehandle): %s"
        raise SystemExit(message % type(filename))
