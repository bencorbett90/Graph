# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph/tracetab.ui'
#
# Created: Mon Jul 13 18:14:16 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1081, 761)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_4 = QtGui.QSplitter(Form)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName(_fromUtf8("splitter_4"))
        self.tree_data = QtGui.QTreeWidget(self.splitter_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_data.sizePolicy().hasHeightForWidth())
        self.tree_data.setSizePolicy(sizePolicy)
        self.tree_data.setColumnCount(2)
        self.tree_data.setObjectName(_fromUtf8("tree_data"))
        self.tree_trace = QtGui.QTreeWidget(self.splitter_4)
        self.tree_trace.setColumnCount(3)
        self.tree_trace.setObjectName(_fromUtf8("tree_trace"))
        self.btn_newTrace = QtGui.QPushButton(self.splitter_4)
        self.btn_newTrace.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btn_newTrace.setObjectName(_fromUtf8("btn_newTrace"))
        self.verticalLayout.addWidget(self.splitter_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.plot = PlotWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setSizeIncrement(QtCore.QSize(0, 0))
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spin_x_min = SpinBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_x_min.sizePolicy().hasHeightForWidth())
        self.spin_x_min.setSizePolicy(sizePolicy)
        self.spin_x_min.setMinimumSize(QtCore.QSize(0, 0))
        self.spin_x_min.setMaximumSize(QtCore.QSize(80, 15))
        self.spin_x_min.setBaseSize(QtCore.QSize(30, 15))
        self.spin_x_min.setObjectName(_fromUtf8("spin_x_min"))
        self.horizontalLayout.addWidget(self.spin_x_min)
        self.spin_x_max = SpinBox(Form)
        self.spin_x_max.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_x_max.sizePolicy().hasHeightForWidth())
        self.spin_x_max.setSizePolicy(sizePolicy)
        self.spin_x_max.setMinimumSize(QtCore.QSize(0, 0))
        self.spin_x_max.setMaximumSize(QtCore.QSize(80, 15))
        self.spin_x_max.setBaseSize(QtCore.QSize(30, 15))
        self.spin_x_max.setObjectName(_fromUtf8("spin_x_max"))
        self.horizontalLayout.addWidget(self.spin_x_max)
        self.spin_y_min = SpinBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_y_min.sizePolicy().hasHeightForWidth())
        self.spin_y_min.setSizePolicy(sizePolicy)
        self.spin_y_min.setMinimumSize(QtCore.QSize(0, 0))
        self.spin_y_min.setMaximumSize(QtCore.QSize(80, 15))
        self.spin_y_min.setBaseSize(QtCore.QSize(30, 15))
        self.spin_y_min.setObjectName(_fromUtf8("spin_y_min"))
        self.horizontalLayout.addWidget(self.spin_y_min)
        self.spin_y_max = SpinBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_y_max.sizePolicy().hasHeightForWidth())
        self.spin_y_max.setSizePolicy(sizePolicy)
        self.spin_y_max.setMinimumSize(QtCore.QSize(0, 0))
        self.spin_y_max.setMaximumSize(QtCore.QSize(80, 15))
        self.spin_y_max.setBaseSize(QtCore.QSize(30, 15))
        self.spin_y_max.setObjectName(_fromUtf8("spin_y_max"))
        self.horizontalLayout.addWidget(self.spin_y_max)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(5, 10))
        self.label_3.setMaximumSize(QtCore.QSize(40, 15))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(5, 10))
        self.label_4.setMaximumSize(QtCore.QSize(40, 15))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(5, 10))
        self.label.setMaximumSize(QtCore.QSize(40, 15))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(5, 10))
        self.label_2.setMaximumSize(QtCore.QSize(40, 15))
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.btn_autoScaleX = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_autoScaleX.sizePolicy().hasHeightForWidth())
        self.btn_autoScaleX.setSizePolicy(sizePolicy)
        self.btn_autoScaleX.setMaximumSize(QtCore.QSize(75, 25))
        self.btn_autoScaleX.setCheckable(True)
        self.btn_autoScaleX.setChecked(True)
        self.btn_autoScaleX.setObjectName(_fromUtf8("btn_autoScaleX"))
        self.verticalLayout_3.addWidget(self.btn_autoScaleX)
        self.btn_autoScaleY = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_autoScaleY.sizePolicy().hasHeightForWidth())
        self.btn_autoScaleY.setSizePolicy(sizePolicy)
        self.btn_autoScaleY.setMaximumSize(QtCore.QSize(75, 25))
        self.btn_autoScaleY.setCheckable(True)
        self.btn_autoScaleY.setChecked(True)
        self.btn_autoScaleY.setObjectName(_fromUtf8("btn_autoScaleY"))
        self.verticalLayout_3.addWidget(self.btn_autoScaleY)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.btnColor_background = ColorButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnColor_background.sizePolicy().hasHeightForWidth())
        self.btnColor_background.setSizePolicy(sizePolicy)
        self.btnColor_background.setMaximumSize(QtCore.QSize(75, 20))
        self.btnColor_background.setObjectName(_fromUtf8("btnColor_background"))
        self.verticalLayout_4.addWidget(self.btnColor_background)
        self.label_6 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMaximumSize(QtCore.QSize(100, 15))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btnColor_grid = ColorButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnColor_grid.sizePolicy().hasHeightForWidth())
        self.btnColor_grid.setSizePolicy(sizePolicy)
        self.btnColor_grid.setMaximumSize(QtCore.QSize(75, 20))
        self.btnColor_grid.setObjectName(_fromUtf8("btnColor_grid"))
        self.verticalLayout_2.addWidget(self.btnColor_grid)
        self.label_5 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMaximumSize(QtCore.QSize(75, 15))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.label_5)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.checkBox_logX = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_logX.sizePolicy().hasHeightForWidth())
        self.checkBox_logX.setSizePolicy(sizePolicy)
        self.checkBox_logX.setMaximumSize(QtCore.QSize(16777215, 15))
        self.checkBox_logX.setObjectName(_fromUtf8("checkBox_logX"))
        self.verticalLayout_8.addWidget(self.checkBox_logX)
        self.checkBox_logY = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_logY.sizePolicy().hasHeightForWidth())
        self.checkBox_logY.setSizePolicy(sizePolicy)
        self.checkBox_logY.setMaximumSize(QtCore.QSize(16777215, 15))
        self.checkBox_logY.setObjectName(_fromUtf8("checkBox_logY"))
        self.verticalLayout_8.addWidget(self.checkBox_logY)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.checkBox_showGrid = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_showGrid.sizePolicy().hasHeightForWidth())
        self.checkBox_showGrid.setSizePolicy(sizePolicy)
        self.checkBox_showGrid.setMaximumSize(QtCore.QSize(16777215, 15))
        self.checkBox_showGrid.setObjectName(_fromUtf8("checkBox_showGrid"))
        self.verticalLayout_6.addWidget(self.checkBox_showGrid)
        self.checkBox_showLegend = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_showLegend.sizePolicy().hasHeightForWidth())
        self.checkBox_showLegend.setSizePolicy(sizePolicy)
        self.checkBox_showLegend.setMaximumSize(QtCore.QSize(16777215, 15))
        self.checkBox_showLegend.setObjectName(_fromUtf8("checkBox_showLegend"))
        self.verticalLayout_6.addWidget(self.checkBox_showLegend)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.tree_data.headerItem().setText(0, _translate("Form", "DataStreams", None))
        self.tree_trace.headerItem().setText(0, _translate("Form", "Traces", None))
        self.btn_newTrace.setText(_translate("Form", "Create New Trace", None))
        self.label_3.setText(_translate("Form", "x min", None))
        self.label_4.setText(_translate("Form", "x max", None))
        self.label.setText(_translate("Form", "y min", None))
        self.label_2.setText(_translate("Form", "y max", None))
        self.btn_autoScaleX.setText(_translate("Form", "Auto Scale X", None))
        self.btn_autoScaleY.setText(_translate("Form", "Auto Scale Y", None))
        self.label_6.setText(_translate("Form", "Background Color", None))
        self.label_5.setText(_translate("Form", "Grid Color", None))
        self.checkBox_logX.setText(_translate("Form", "Log X", None))
        self.checkBox_logY.setText(_translate("Form", "Log Y", None))
        self.checkBox_showGrid.setText(_translate("Form", "Show Grid", None))
        self.checkBox_showLegend.setText(_translate("Form", "Show Legend", None))

from pyqtgraph import SpinBox, ColorButton, PlotWidget
