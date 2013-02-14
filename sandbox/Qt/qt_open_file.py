# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_file.ui'
#
# Created: Wed Feb 13 10:39:58 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 400)
        MainWindow.setWindowTitle(_fromUtf8("MainWindow"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 50, 182, 37))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setText(_fromUtf8("Hello World!"))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 150, 97, 27))
        self.pushButton.setText(_fromUtf8("Load File"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(42, 120, 551, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # QtCore.QObject.connect(self.pushButton,
        #     QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit.update)
        QtCore.QObject.connect(self.pushButton,
            QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectFile)
        # self.pushButton.clicked.connect(self.selectFile))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def selectFile(self):
        self.lineEdit.setText(QtGui.QFileDialog.getOpenFileName())

    def retranslateUi(self, MainWindow):
        pass

