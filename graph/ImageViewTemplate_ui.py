# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph/ImageViewTemplate.ui'
#
# Created: Fri Jul 31 13:38:07 2015
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
        Form.resize(814, 588)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.splitter_slice_vert = QtGui.QSplitter(self.horizontalLayoutWidget_2)
        self.splitter_slice_vert.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_slice_vert.setObjectName(_fromUtf8("splitter_slice_vert"))
        self.splitter_slice_horiz = QtGui.QSplitter(self.splitter_slice_vert)
        self.splitter_slice_horiz.setOrientation(QtCore.Qt.Vertical)
        self.splitter_slice_horiz.setObjectName(_fromUtf8("splitter_slice_horiz"))
        self.graphicsView = GraphicsView(self.splitter_slice_horiz)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.plot_slice_horiz = PlotWidget(self.splitter_slice_horiz)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_slice_horiz.sizePolicy().hasHeightForWidth())
        self.plot_slice_horiz.setSizePolicy(sizePolicy)
        self.plot_slice_horiz.setMinimumSize(QtCore.QSize(0, 40))
        self.plot_slice_horiz.setObjectName(_fromUtf8("plot_slice_horiz"))
        self.plot_slice_vert = PlotWidget(self.splitter_slice_vert)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_slice_vert.sizePolicy().hasHeightForWidth())
        self.plot_slice_vert.setSizePolicy(sizePolicy)
        self.plot_slice_vert.setMinimumSize(QtCore.QSize(0, 40))
        self.plot_slice_vert.setObjectName(_fromUtf8("plot_slice_vert"))
        self.horizontalLayout_3.addWidget(self.splitter_slice_vert)
        self.roiPlot = PlotWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roiPlot.sizePolicy().hasHeightForWidth())
        self.roiPlot.setSizePolicy(sizePolicy)
        self.roiPlot.setMinimumSize(QtCore.QSize(0, 40))
        self.roiPlot.setObjectName(_fromUtf8("roiPlot"))
        self.horizontalLayout_4.addWidget(self.splitter)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.histogram = HistogramLUTWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram.sizePolicy().hasHeightForWidth())
        self.histogram.setSizePolicy(sizePolicy)
        self.histogram.setMaximumSize(QtCore.QSize(150, 16777215))
        self.histogram.setObjectName(_fromUtf8("histogram"))
        self.verticalLayout.addWidget(self.histogram)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.menuBtn = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.menuBtn.sizePolicy().hasHeightForWidth())
        self.menuBtn.setSizePolicy(sizePolicy)
        self.menuBtn.setMaximumSize(QtCore.QSize(70, 16777215))
        self.menuBtn.setObjectName(_fromUtf8("menuBtn"))
        self.horizontalLayout_2.addWidget(self.menuBtn)
        self.roiBtn = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.roiBtn.sizePolicy().hasHeightForWidth())
        self.roiBtn.setSizePolicy(sizePolicy)
        self.roiBtn.setMaximumSize(QtCore.QSize(70, 16777215))
        self.roiBtn.setCheckable(True)
        self.roiBtn.setObjectName(_fromUtf8("roiBtn"))
        self.horizontalLayout_2.addWidget(self.roiBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.normGroup = QtGui.QGroupBox(Form)
        self.normGroup.setObjectName(_fromUtf8("normGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.normGroup)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.normGroup)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 2, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.normGroup)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.normROICheck = QtGui.QCheckBox(self.normGroup)
        self.normROICheck.setObjectName(_fromUtf8("normROICheck"))
        self.gridLayout_2.addWidget(self.normROICheck, 1, 1, 1, 1)
        self.normDivideRadio = QtGui.QRadioButton(self.normGroup)
        self.normDivideRadio.setChecked(False)
        self.normDivideRadio.setObjectName(_fromUtf8("normDivideRadio"))
        self.gridLayout_2.addWidget(self.normDivideRadio, 0, 1, 1, 1)
        self.normXBlurSpin = QtGui.QDoubleSpinBox(self.normGroup)
        self.normXBlurSpin.setObjectName(_fromUtf8("normXBlurSpin"))
        self.gridLayout_2.addWidget(self.normXBlurSpin, 2, 2, 1, 1)
        self.normOffRadio = QtGui.QRadioButton(self.normGroup)
        self.normOffRadio.setChecked(True)
        self.normOffRadio.setObjectName(_fromUtf8("normOffRadio"))
        self.gridLayout_2.addWidget(self.normOffRadio, 0, 3, 1, 1)
        self.normTimeRangeCheck = QtGui.QCheckBox(self.normGroup)
        self.normTimeRangeCheck.setObjectName(_fromUtf8("normTimeRangeCheck"))
        self.gridLayout_2.addWidget(self.normTimeRangeCheck, 1, 3, 1, 1)
        self.normSubtractRadio = QtGui.QRadioButton(self.normGroup)
        self.normSubtractRadio.setObjectName(_fromUtf8("normSubtractRadio"))
        self.gridLayout_2.addWidget(self.normSubtractRadio, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.normFrameCheck = QtGui.QCheckBox(self.normGroup)
        self.normFrameCheck.setObjectName(_fromUtf8("normFrameCheck"))
        self.gridLayout_2.addWidget(self.normFrameCheck, 1, 2, 1, 1)
        self.normTBlurSpin = QtGui.QDoubleSpinBox(self.normGroup)
        self.normTBlurSpin.setObjectName(_fromUtf8("normTBlurSpin"))
        self.gridLayout_2.addWidget(self.normTBlurSpin, 2, 6, 1, 1)
        self.label_10 = QtGui.QLabel(self.normGroup)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 2, 5, 1, 1)
        self.normYBlurSpin = QtGui.QDoubleSpinBox(self.normGroup)
        self.normYBlurSpin.setObjectName(_fromUtf8("normYBlurSpin"))
        self.gridLayout_2.addWidget(self.normYBlurSpin, 2, 4, 1, 1)
        self.verticalLayout_2.addWidget(self.normGroup)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.menuBtn.setText(_translate("Form", "Menu", None))
        self.roiBtn.setText(_translate("Form", "ROI", None))
        self.normGroup.setTitle(_translate("Form", "Normalization", None))
        self.label_4.setText(_translate("Form", "Blur:", None))
        self.label_9.setText(_translate("Form", "Y", None))
        self.label_8.setText(_translate("Form", "X", None))
        self.label_5.setText(_translate("Form", "Operation:", None))
        self.normROICheck.setText(_translate("Form", "ROI", None))
        self.normDivideRadio.setText(_translate("Form", "Divide", None))
        self.normOffRadio.setText(_translate("Form", "Off", None))
        self.normTimeRangeCheck.setText(_translate("Form", "Time range", None))
        self.normSubtractRadio.setText(_translate("Form", "Subtract", None))
        self.label_3.setText(_translate("Form", "Mean:", None))
        self.normFrameCheck.setText(_translate("Form", "Frame", None))
        self.label_10.setText(_translate("Form", "T", None))

from pyqtgraph import HistogramLUTWidget, GraphicsView, PlotWidget
