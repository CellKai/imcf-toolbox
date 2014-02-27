
Testing the GUI
===============

The `--preset` switch can be used to facilitate testing the GUI from the
commandline by specifying the names and corresponding values for the desired
GUI elements in the following form:

```shell
PRESETS="le_infile=../../sample_data/mtrack2/1170_4001_5000.txt,"\
"le_outfile=../../sample_data/mtrack2/results__1170_4001_5000.csv"
python mtrack2_stats_gui.py --preset $PRESETS
```
