
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

```shell
IN="TESTDATA/spots_distances/spots_nocorners_ws-all.xml"
OUT="TESTDATA/spots_distances/spots_nocorners_bitmap-uncropped.csv"
PRESETS="le_infile=${IN},le_outfile=${OUT},"\
"dsb_1=268.463,dsb_2=265.676,sb_1=256,sb_2=256"
rm -v "${OUT}"
python spots_to_bitmap_gui.py --preset $PRESETS
```

```shell
IN="TESTDATA/spots_distances/spots_allcorners_ws-all.xml"
OUT="TESTDATA/spots_distances/spots_allcorners_bitmap-uncropped.csv"
PRESETS="le_infile=${IN},le_outfile=${OUT},"\
"dsb_1=383.475,dsb_2=382.940,sb_1=256,sb_2=256"
rm -v "${OUT}"
python spots_to_bitmap_gui.py --preset $PRESETS
```
