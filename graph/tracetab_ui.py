# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph/tracetab.ui'
#
# Created: Sun Jul 12 20:21:49 2015
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
        Form.resize(944, 761)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_4 = QtGui.QSplitter(self.verticalLayoutWidget)
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
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.plot = PlotWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setSizeIncrement(QtCore.QSize(0, 0))
        self.plot.setObjectName(_fromUtf8("plot"))
        self.verticalLayout_7.addWidget(self.plot)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.spin_x_min = SpinBox(self.layoutWidget)
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
        self.spin_x_max = SpinBox(self.layoutWidget)
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
        self.spin_y_min = SpinBox(self.layoutWidget)
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
        self.spin_y_max = SpinBox(self.layoutWidget)
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
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
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
        self.label_4 = QtGui.QLabel(self.layoutWidget)
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
        self.label = QtGui.QLabel(self.layoutWidget)
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
        self.label_2 = QtGui.QLabel(self.layoutWidget)
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
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.btn_setRange = QtGui.QPushButton(self.layoutWidget)
        self.btn_setRange.setMaximumSize(QtCore.QSize(75, 25))
        self.btn_setRange.setObjectName(_fromUtf8("btn_setRange"))
        self.horizontalLayout_5.addWidget(self.btn_setRange)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.btn_autoScaleX = QtGui.QPushButton(self.layoutWidget)
        self.btn_autoScaleX.setMaximumSize(QtCore.QSize(75, 25))
        self.btn_autoScaleX.setCheckable(True)
        self.btn_autoScaleX.setChecked(True)
        self.btn_autoScaleX.setObjectName(_fromUtf8("btn_autoScaleX"))
        self.verticalLayout_3.addWidget(self.btn_autoScaleX)
        self.btn_autoScaleY = QtGui.QPushButton(self.layoutWidget)
        self.btn_autoScaleY.setMaximumSize(QtCore.QSize(75, 25))
        self.btn_autoScaleY.setCheckable(True)
        self.btn_autoScaleY.setChecked(True)
        self.btn_autoScaleY.setObjectName(_fromUtf8("btn_autoScaleY"))
        self.verticalLayout_3.addWidget(self.btn_autoScaleY)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.btnColor_background = ColorButton(self.layoutWidget)
        self.btnColor_background.setMaximumSize(QtCore.QSize(75, 25))
        self.btnColor_background.setObjectName(_fromUtf8("btnColor_background"))
        self.verticalLayout_4.addWidget(self.btnColor_background)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setMaximumSize(QtCore.QSize(100, 15))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btnColor_grid = ColorButton(self.layoutWidget)
        self.btnColor_grid.setMaximumSize(QtCore.QSize(75, 25))
        self.btnColor_grid.setObjectName(_fromUtf8("btnColor_grid"))
        self.verticalLayout_2.addWidget(self.btnColor_grid)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setMaximumSize(QtCore.QSize(75, 15))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.label_5)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.checkBox_showGrid = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_showGrid.setObjectName(_fromUtf8("checkBox_showGrid"))
        self.verticalLayout_6.addWidget(self.checkBox_showGrid)
        self.checkBox_showLegend = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_showLegend.setObjectName(_fromUtf8("checkBox_showLegend"))
        self.verticalLayout_6.addWidget(self.checkBox_showLegend)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_8.addWidget(self.splitter)

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
        self.btn_setRange.setText(_translate("Form", "Set Range", None))
        self.btn_autoScaleX.setText(_translate("Form", "Auto Scale X", None))
        self.btn_autoScaleY.setText(_translate("Form", "Auto Scale Y", None))
        self.label_6.setText(_translate("Form", "Background Color", None))
        self.label_5.setText(_translate("Form", "Grid Color", None))
        self.checkBox_showGrid.setText(_translate("Form", "Show Grid", None))
        self.checkBox_showLegend.setText(_translate("Form", "Show Legend", None))

from pyqtgraph import SpinBox, ColorButton, PlotWidget