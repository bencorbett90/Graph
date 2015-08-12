# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph/graph.ui'
#
# Created: Wed Aug 05 16:08:05 2015
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
        MainWindow.resize(773, 655)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 773, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPlot = QtGui.QMenu(self.menubar)
        self.menuPlot.setObjectName(_fromUtf8("menuPlot"))
        self.menuTab = QtGui.QMenu(self.menubar)
        self.menuTab.setObjectName(_fromUtf8("menuTab"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.file_open = QtGui.QAction(MainWindow)
        self.file_open.setObjectName(_fromUtf8("file_open"))
        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.curPlot_copy = QtGui.QAction(MainWindow)
        self.curPlot_copy.setObjectName(_fromUtf8("curPlot_copy"))
        self.curPlot_paste = QtGui.QAction(MainWindow)
        self.curPlot_paste.setObjectName(_fromUtf8("curPlot_paste"))
        self.tab_new_trace = QtGui.QAction(MainWindow)
        self.tab_new_trace.setObjectName(_fromUtf8("tab_new_trace"))
        self.tab_new_image = QtGui.QAction(MainWindow)
        self.tab_new_image.setObjectName(_fromUtf8("tab_new_image"))
        self.actionClose_tab = QtGui.QAction(MainWindow)
        self.actionClose_tab.setObjectName(_fromUtf8("actionClose_tab"))
        self.curPlot_cut = QtGui.QAction(MainWindow)
        self.curPlot_cut.setObjectName(_fromUtf8("curPlot_cut"))
        self.curPlot_zoom_to = QtGui.QAction(MainWindow)
        self.curPlot_zoom_to.setObjectName(_fromUtf8("curPlot_zoom_to"))
        self.menuFile.addAction(self.file_open)
        self.menuPlot.addAction(self.curPlot_zoom_to)
        self.menuPlot.addSeparator()
        self.menuPlot.addAction(self.curPlot_cut)
        self.menuPlot.addAction(self.curPlot_copy)
        self.menuPlot.addAction(self.curPlot_paste)
        self.menuPlot.addSeparator()
        self.menuPlot.addAction(self.actionDelete)
        self.menuTab.addAction(self.tab_new_trace)
        self.menuTab.addAction(self.tab_new_image)
        self.menuTab.addSeparator()
        self.menuTab.addAction(self.actionClose_tab)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTab.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuPlot.setTitle(_translate("MainWindow", "Current Plot", None))
        self.menuTab.setTitle(_translate("MainWindow", "Tab", None))
        self.file_open.setText(_translate("MainWindow", "Open", None))
        self.file_open.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionDelete.setText(_translate("MainWindow", "Delete", None))
        self.curPlot_copy.setText(_translate("MainWindow", "Copy", None))
        self.curPlot_copy.setShortcut(_translate("MainWindow", "Ctrl+C", None))
        self.curPlot_paste.setText(_translate("MainWindow", "Paste", None))
        self.curPlot_paste.setShortcut(_translate("MainWindow", "Ctrl+V", None))
        self.tab_new_trace.setText(_translate("MainWindow", "New Trace tab", None))
        self.tab_new_trace.setShortcut(_translate("MainWindow", "Ctrl+T", None))
        self.tab_new_image.setText(_translate("MainWindow", "New Image tab", None))
        self.tab_new_image.setShortcut(_translate("MainWindow", "Ctrl+I", None))
        self.actionClose_tab.setText(_translate("MainWindow", "Close tab", None))
        self.curPlot_cut.setText(_translate("MainWindow", "Cut", None))
        self.curPlot_cut.setShortcut(_translate("MainWindow", "Ctrl+X", None))
        self.curPlot_zoom_to.setText(_translate("MainWindow", "Zoom to", None))
        self.curPlot_zoom_to.setShortcut(_translate("MainWindow", "Alt+Z", None))

