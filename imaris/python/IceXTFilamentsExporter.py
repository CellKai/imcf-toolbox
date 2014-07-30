#
#  Filaments Exporter for Imaris 7 by Niko Ehrenfeuchter
#
#  Requirements:
#   - pIceImarisConnector (https://github.com/aarpon/pIceImarisConnector)
#
### Imaris meta information ###
# <CustomTools>
#  <Menu>
#   <Submenu name="Filaments Functions">
#   <Item name="Filaments Exporter (Python)" icon="Python"
#      tooltip="Export points of selected Filaments to CSV.">
#     <Command>PythonXT::IceXTFilamentsExporter(%i)</Command>
#   </Item>
#   </Submenu>
#  </Menu>
#  <SurpassTab>
#   <SurpassComponent name="bpFilaments">
#     <Item name="THIS DOES NOT WORK">
#       <Command>PythonXT::IceXTFilamentsExporter(%i)</Command>
#     </Item>
#   </SurpassComponent>
#  </SurpassTab>
# </CustomTools>

__version__ = 33

import csv
from os.path import split, join

from Tkinter import Tk
from tkFileDialog import asksaveasfilename
from tkMessageBox import askyesno

import ImarisLib
try:
    from pIceImarisConnector import pIceImarisConnector
except:
    Tk().withdraw()
    askyesno('ERROR', "Couldn't find pIceImarisConnector!")



def IceXTFilamentsExporter(ims_app_id=None):

    # set up Tk first so the root window doesn't appear:
    Tk().withdraw()
    
    if ims_app_id is not None:
        connector = pIceImarisConnector(ims_app_id)
    else:
        # start Imaris and set up the connection
        connector = pIceImarisConnector()
        connector.startImaris()

    # if called from Python using an existing connection (useful for
    # debugging), it is better to do some sanity checks first:
    if not connector.isAlive():
        print('Error: no connection to Imaris!')
        return None
    conn = connector.mImarisApplication
    print('connection ID: %s' % conn)
    while not conn.GetFactory().IsFilaments(conn.GetSurpassSelection()):
        msg = 'A "FILAMENTS" object needs to be selected!\n\nTry again?'
        title = 'Selection required!'
        if not askyesno(title, msg):
            return None
    export_filaments(conn)


def export_filaments(conn):
    factory = conn.GetFactory()
    selection = conn.GetSurpassSelection()
    filaments = factory.ToFilaments(selection)
    # scene = conn.GetSurpassScene

    # extract positions of filament points for each and store them
    for i in range(filaments.GetNumberOfFilaments()):
        # gives a list of tuples denoting the edges:
        # filaments.GetEdges(i)
        (fpath, fname) = split(conn.GetCurrentFileName())
        fname = '%s-filaments-%d.csv' % (fname, i)
        opts = {'initialfile': fname,
                'initialdir': fpath,
                'title': 'File name for the filaments export'}
        fname = asksaveasfilename(**opts)
        if fname == '':
            print('aborting due to user request')
            return None
        print('writing filament export to "%s"' % fname)

        # gives a list of 3-tuples with coordinates:
        pos_xyz = filaments.GetPositionsXYZ(i)
        with open(fname, 'wb') as csvout:
            csvwriter = csv.writer(csvout)
            for row in pos_xyz:
                csvwriter.writerow(row)

