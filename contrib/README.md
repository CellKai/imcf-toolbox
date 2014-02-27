About "contrib"
===============

This subtree contains standalone tools that for example pre- or postprocess
data that was created by another software but are not running within the scope
of this software directly.

That's for example scripts that take results from an ImageJ plugin (MTrack2,
WingJ, ...) or Imaris statistics export. All generic functionality is to be
avoided within these tools, everything that is reusable should of course live
in the corresponding library packages.
