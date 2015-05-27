# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calc.ui'
#
# Created: Wed May 27 15:59:58 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(638, 447)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.line_x = QtGui.QLineEdit(self.centralwidget)
        self.line_x.setGeometry(QtCore.QRect(140, 160, 113, 20))
        self.line_x.setText(_fromUtf8(""))
        self.line_x.setReadOnly(False)
        self.line_x.setObjectName(_fromUtf8("line_x"))
        self.line_x2 = QtGui.QLineEdit(self.centralwidget)
        self.line_x2.setGeometry(QtCore.QRect(380, 160, 113, 20))
        self.line_x2.setReadOnly(True)
        self.line_x2.setObjectName(_fromUtf8("line_x2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 190, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 190, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.calculate = QtGui.QPushButton(self.centralwidget)
        self.calculate.setGeometry(QtCore.QRect(280, 160, 75, 23))
        self.calculate.setCheckable(False)
        self.calculate.setObjectName(_fromUtf8("calculate"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 638, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.line_x.setPlaceholderText(_translate("MainWindow", "x", None))
        self.line_x2.setPlaceholderText(_translate("MainWindow", "x^2", None))
        self.label.setText(_translate("MainWindow", "x", None))
        self.label_2.setText(_translate("MainWindow", "x^2", None))
        self.calculate.setText(_translate("MainWindow", "Calculate", None))

