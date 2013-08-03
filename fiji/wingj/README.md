Example using ImageJ measurement export
=======================================

```shell
python wingj_distances.py --directory ../../sample_data/wingj \
    --ijroi ../../sample_data/wingj/surfaces-coords.ij.csv
```

Example using Imaris XML export
===============================

```shell
python wingj_distances.py --directory ../../sample_data/wingj \
    --imsxml ../../sample_data/wingj/surfaces.xml
```

Testing the GUI
===============

The `--preset` switch can be used to facilitate testing the GUI from the
commandline by specifying the names and corresponding values for the desired
GUI elements in the following form:

```shell
PRESETS="le_path_1=../../sample_data/wingj,"\
"le_path_2=../../sample_data/wingj/surfaces-coords.ij.csv"
python wingj_distances_gui.py --preset $PRESETS
```
