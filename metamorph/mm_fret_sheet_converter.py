#!/usr/bin/python

from xlrd import open_workbook, colname
import numpy as np
import pprint

ppr = pprint.PrettyPrinter(indent=4)

xlfile = open('../sample_data/fret/2013_08_05T2_-_Linescans_example_2013_10_15.xlsx','rb').read()
wb = open_workbook(file_contents=xlfile)

sheet = wb.sheet_by_index(0)
print("Sheet 0 name: %s" % sheet.name)

sec_size = int(sheet.cell_value(1,8))
sections = int(sheet.nrows / (sec_size + 3))
print("Section size: %s, number of sections: %s" % (sec_size, sections))

for sec in range(sections):
    print sheet.row_values(1,1)


