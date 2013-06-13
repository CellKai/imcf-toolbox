import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#signal handler
def myCellChanged(row, col):
    print row, col

#just a helper function to setup the table
def createCheckItem(table, row, col):
    check = QTableWidgetItem("Test")
    check.setCheckState(Qt.Checked)
    table.setItem(row,col,check)

app = QApplication(sys.argv)

#create the 5x5 table...
table = QTableWidget(5,5)
map(lambda (row,col): createCheckItem(table, row, col),
   [(row, col) for row in range(0, 5) for col in range(0, 5)])
table.show()

#...and connect our signal handler to the cellChanged(int, int) signal
QObject.connect(table, SIGNAL("cellChanged(int, int)"), myCellChanged)
app.exec_()
