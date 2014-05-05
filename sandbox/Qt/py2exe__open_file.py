# to run py2exe this script needs to be called like this:
# >>> C:\Python27\python.exe py2exe__open_file.py py2exe

from distutils.core import setup

import py2exe
setup(
    options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"],  # requires vcredist 2008
            "includes": ["sip", "PyQt4.QtGui"]
        }
    },
    windows=['open_file.py']
)
