"""A convenience module to set up logging with some default values across
multiple modules.

To use it, just add this line to your python code:
---
from log import log
---
From there on a logger is available for usage with e.g. log.warn(), even if the
import statement from above happens in multiple places across modules, it will
always use the same logger instance (that functionality is built into the
logging module, we just do the setup here). This can easily be check by looking at the log handlers in the different modules.
"""

import logging

log = logging.getLogger('imcf_logger')

# we always log to stdout, so add a console handler to the logger
log.addHandler(logging.StreamHandler())

# from http://stackoverflow.com/questions/4722745
#
# formatter = logging.Formatter(
#     "%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")
# # Alternative formatting available on python 3.2+:
# # formatter = logging.Formatter(
# #     "{asctime} {threadName:>11} {levelname} {message}", style='{')
#
# # Log to file
# filehandler = logging.FileHandler("debug.txt", "w")
# filehandler.setLevel(logging.DEBUG)
# filehandler.setFormatter(formatter)
# log.addHandler(filehandler)
#
# # Log to stdout too
# streamhandler = logging.StreamHandler()
# streamhandler.setLevel(logging.INFO)
# streamhandler.setFormatter(formatter)
# log.addHandler(streamhandler)
