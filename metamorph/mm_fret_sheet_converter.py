from mmap import mmap,ACCESS_READ
from xlrd import open_workbook, colname
import numpy as np
import pprint

ppr = pprint.PrettyPrinter(indent=4)

xlfile = open('2013_08_05T2_-_Linescans_example_workingcopy.xlsx','rb').read()
wb = open_workbook(file_contents=xlfile)

sheet = wb.sheet_by_index(0)
print("Sheet 0 name: %s" % sheet.name)

# sec_size = 83
sec_size = int(sheet.cell_value(1,8))
sections = int(sheet.nrows / (sec_size + 3))
print("Section size: %s, number of sections: %s" % (sec_size, sections))

print colname(3)

for sec in range(sections):
    print sheet.row_values(1,1)

# for sec in range(sections):
#     line_0 = ''
#     line_1 = ''
#     for col in range(14):
#         line_0 += str(sheet.cell_value(sec * 86, col)) + ' | '
#         line_1 += str(sheet.cell_value(sec * 86 + 1, col)) + ' | '
#     # print(
#     #     str(sheet.cell_value(sec * 86, 0)) + ' | ' +
#     #     str(sheet.cell_value(sec * 86, 1)) + ' | ' +
#     #     str(sheet.cell_value(sec * 86, 2)) + '\n' +
#     #     str(sheet.cell_value(sec * 86 + 1, 0)) + ' | ' +
#     #     str(sheet.cell_value(sec * 86 + 1, 1)) + ' | ' +
#     #     str(sheet.cell_value(sec * 86 + 1, 2)) + ' | ' +
#     #     str(sheet.cell_value(sec * 86 + 2, 0)) + '\n' +
#     #     str(sheet.cell_value(sec * 86 + 2, 1)) + ' | ' +
#     #     str(sheet.cell_value(sec * 86 + 2, 2)))
#     print line_0
#     # print line_1

