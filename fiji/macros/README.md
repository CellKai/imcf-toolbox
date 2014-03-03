About
=====

This directory serves two related purposes:
* The topmost level contains "plain" macros in the ImageJ Macro language that
  are "ready to use" via the _Plugins_ menu within ImageJ.
* The "templates" subdirectories is for building-blocks of ImageJ macros to be
  used with the macro generating engine. They are not meant to show up in the
  ImageJ menu. See e.g. the FluoView Stitcher plugin for more an example how to
  use this.

Adding a macro
==============

* Make sure the file name contains an underscore and the file suffix is ".ijm".
* Edit "plugins.config" to have the macro show up in ImageJ's _Plugins_ menu
  structure with the desired name.

Adding a template
=================

* Templates consist of two parts, head and body. Choose a name for the template
  and put the two files into the "templates" directory, adding "\_head.ijm" and
  "\_body.ijm" as a suffix to the name.
