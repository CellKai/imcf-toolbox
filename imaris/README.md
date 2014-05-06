Imaris
======

The tools in this subtree work in the scope of Imaris XT.

Shellscripts
------------

`pythonXT.cmd` is used to set up the correct environment to run an interactive
Python shell that can import the required `ImarisLib` module and use it to
communicate with a running Imaris instance.

`ipythonXT.cmd` does the same job but is using the IPython console (either via
the standard Windows `cmd` console or using the Qt console of IPython. This
script expects the [Anaconda](http://continuum.io/) distribution of Python
being installed.

Both cmd scripts require the desired Imaris version as a parameter, using the
following syntax:
```
pythonXT.cmd "7.6.5"
pythonXT.cmd "x64 7.7.1"
ipythonXT.cmd "x64 7.7.1" qtconsole
```

Python
------
Extensions written in Python can be found in the `python/` subdirectory.

Matlab
------
Extensions written in Matlab can be found in the `matlab/` subdirectory.
