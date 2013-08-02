
Testing the GUI
===============
The `--preset` switch can be used to facilitate testing the GUI from the
commandline by specifying the names and corresponding values for the desired
GUI elements in the following form:

```shell
PRESETS="le_infile=TESTDATA/filaments/testdata-filaments-manual.csv,"\
"le_outfile=TESTDATA/filaments/result_filaments-manual.csv"
python junction_statistics_gui.py --preset $PRESETS
```
