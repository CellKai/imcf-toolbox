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

The `--preset` switch can be used to facilitate testing the GUI from the commandline:

```shell
python  wingj_distances_gui.py --preset TESTDATA/wingj/structure_A-P.txt,TESTDATA/wingj/structure_V-D.txt,TESTDATA/wingj/structure_contour.txt,TESTDATA/wingj/surfaces.xml,TESTDATA/wingj/results-uncalibrated/wt1-to-AP.csv,TESTDATA/wingj/results-uncalibrated/wt1-to-VD.csv,TESTDATA/wingj/results-uncalibrated/wt1-to-contour.csv
```
