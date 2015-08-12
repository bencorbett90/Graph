import pyqtgraph as pqg
from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotDataItem
from imageitem import ImageItem
from utils import *


class TraceItem(PlotDataItem):
    count = 0

    def __init__(self,  traceTab, *args, **kargs):
        super(self.__class__, self).__init__(*args, **kargs)
        self.traceTab = traceTab
        self.NAME = None
        self.curveColor = pqg.mkColor(0, 0, 0, 255)
        self.curveSize = 3
        self.pointColor = pqg.mkColor(0, 0, 0, 255)
        self.pointSize = 3
        self.shadowColor = pqg.mkColor(0, 0, 0, 255)
        self.shadowSize = 0
        self.outlineColor = pqg.mkColor(0, 0, 0, 255)
        self.outlineSize = 0
        self.fillColor = pqg.mkColor(0, 0, 0, 255)
        self.symbol = 'o'
        self.fillLevel = None
        self.pxMode = True
        
        self.x = None
        self.y = None
        self.spin_sliceMin = None
        self.spin_sliceMax = None
        self.spin_sliceParams = []
        self.sliceTable = None
        self.updateSlice = True

        self.ds = None
        self.valName = None
        self.argName = None
        self.sliceParams = {}

        self.update = False
        self.showOnPlot = True
        self.showCurve = True
        self.showPoints = True
        self.showFill = False
        self.id = TraceItem.count
        TraceItem.count += 1
        self.curve.setClickable(30)

    def copy_data(self, other):
        """Set myself to a copy of OTHER which is also a TraceItem."""
        if isinstance(other, TraceItem):
            self.showCurve = other.showCurve
            self.showPoints = other.showPoints
            self.showFill = other.showFill
            self.showOnPlot = other.showOnPlot
            self.update = other.update
    
            self.ds = other.ds
            self.valName = other.valName
            self.argName = other.argName
            self.sliceParams = other.sliceParams
    
            self.setPointPen(other.pointColor, other.pointSize)
            self.setPointOutline(other.outlineColor, other.outlineSize)
            self.symbol = other.symbol
            self.setSymbolScatter(self.symbol)
            self.pxMode = other.pxMode
    
            self.setFill(other.fillColor, other.fillLevel)
            self.setCurvePen(other.curveColor, other.curveSize)
            self.setCurveShadow(other.shadowColor, other.shadowSize)

        if isinstance(other, ImageItem):
            self.ds = other.ds
            self.valName = other.valName
            self.argName = other.axisNames['x']
            
            for k, v in other.sliceParams.iteritems():
                self.sliceParams[k] = v

            for arg in other.axisNames.itervalues():
                if arg == self.argName or arg == 'None':
                    continue
                else:
                    self.sliceParams[arg] = 0

        self.get_data()
        self.checkBoxShow.setChecked(self.showOnPlot)
        self.toggleShow(self.checkBoxShow)
        self.checkBoxUpdate.setChecked(self.update)
        self.toggleUpdate()

    def delete(self):
        self.removeFrom(self.traceTab.plot)
        self.traceTab.delete_trace(self)
        del self.x
        del self.y
        del self.traceTab

    def set_data_source(self, ds, valName, argName):
        """Set the data that I display to value VALNAME vs argumnent ARGNAME
        of dataSet DSNAME."""
        self.ds = ds
        self.valName = valName
        self.argName = argName
        self.sliceParams.clear()
        for axis in ds.get_args_to_val(valName):
            self.sliceParams[axis] = 0

        self.sliceParams[argName] = (0, ds.get_arg_shape(argName))
        self.update_slice_table(self.traceTab.table_slice)
        self.get_data()
        self.toggleShow(self.checkBoxShow)

    def get_data(self):
        """Get the actual data from SELF.VALNAME and SELF.ARGNAME of SELF.DS
        specified by SELF.SLICEPARAMS."""
        argSlice = slice(*self.sliceParams[self.argName])
        x = self.ds.load_arg(self.argName, argSlice)

        s = self.ds.gen_slice(self.valName, self.sliceParams)
        y = self.ds.load_val(self.valName, s)

        self.setPoints(x, y)

    def update_slice_table(self, sliceTable):
        if self.argName is None:
            sliceTable.clear()
            sliceTable.setHorizontalHeaderLabels(['axis', 'indices', 'values'])
            return

        self.sliceTable = sliceTable
        sliceTable.clear()
        sliceTable.setHorizontalHeaderLabels(['axis', 'indices', 'values'])
        sliceTable.setRowCount(len(self.sliceParams))

        argItem = QtGui.QTableWidgetItem(self.argName)
        sliceTable.setItem(0, 0, argItem)
        minBounds = (0, self.ds.get_arg_shape(self.argName) - 2)
        maxBounds = (1, self.ds.get_arg_shape(self.argName) - 1)
        self.spin_sliceMin = pqg.SpinBox(bounds=minBounds, step=1.0, int=True)
        self.spin_sliceMin.setValue(self.sliceParams[self.argName][0])
        self.spin_sliceMax = pqg.SpinBox(bounds=maxBounds, step=1.0, int=True)
        self.spin_sliceMax.setValue(self.sliceParams[self.argName][1])

        self.spin_sliceMin.sigValueChanging.connect(self.update_slice)
        self.spin_sliceMax.sigValueChanging.connect(self.update_slice)
        spinLayout = QtGui.QHBoxLayout()
        spinLayout.addWidget(self.spin_sliceMin)
        spinLayout.addWidget(self.spin_sliceMax)
        cellWidget = QtGui.QWidget()
        cellWidget.setLayout(spinLayout)
        sliceTable.setCellWidget(0, 1, cellWidget)
        sliceTable.setCellWidget(0, 2, QtGui.QLabel())

        self.spin_sliceParams = []
        row = 1
        for argName, s in self.sliceParams.iteritems():
            if argName == self.argName:
                continue
            argItem = QtGui.QTableWidgetItem(argName)
            sliceTable.setItem(row, 0, argItem)

            bounds = (0, self.ds.get_arg_shape(argName) - 1)
            spin = pqg.SpinBox(bounds=bounds, step=1.0, int=True)
            spin.setValue(self.sliceParams[argName])
            spin.sigValueChanging.connect(self.update_slice)

            self.spin_sliceParams += [spin]
            sliceTable.setCellWidget(row, 1, spin)
            sliceTable.setCellWidget(row, 2, QtGui.QLabel())
            row += 1

        self.update_slice_labels()
        sliceTable.resizeColumnsToContents()
        sliceTable.resizeRowsToContents()
        sliceTable.horizontalHeader().setStretchLastSection(True)

    def update_slice(self):
        if self.updateSlice == False:
            return

        self.updateSlice = False
        sliceMin = self.spin_sliceMin.value()
        sliceMax = self.spin_sliceMax.value()

        self.spin_sliceMin.setMaximum(sliceMax - 1)
        self.spin_sliceMax.setMinimum(sliceMin + 1)
        self.spin_sliceMin.setValue()
        self.spin_sliceMax.setValue()

        sliceMin = self.spin_sliceMin.value()
        sliceMax = self.spin_sliceMax.value()

        self.sliceParams[self.argName] = (sliceMin, sliceMax + 1)

        for row in range(1, self.sliceTable.rowCount()):
            argName = str(self.sliceTable.item(row, 0).text())
            spin = self.sliceTable.cellWidget(row, 1)
            self.sliceParams[argName] = spin.value()

        self.update_slice_labels()
        self.get_data()
        self.updateSlice = True

    def update_slice_labels(self):
        for row in range(self.sliceTable.rowCount()):
            argName = str(self.sliceTable.item(row, 0).text())

            s = self.sliceParams[argName]
            if isinstance(s, tuple):
                valString = '[' + str(self.ds.load_arg(argName, s[0])) + ',  '
                valString += str(self.ds.load_arg(argName, s[1] - 1)) + ']'
            else:
                valString = str(self.ds.load_arg(argName, s))

            label = self.sliceTable.cellWidget(row, 2)
            label.setText(valString)

    def name(self):
        return self.NAME

    def toggleUpdate(self):
        """Turn on/off automatic updating when the trace is refreshed."""
        if self.checkBoxUpdate.isChecked():
            self.update = True
        else:
            self.update = False

    def toggleShowPoints(self, checkBox):
        if checkBox.isChecked():
            self.showPoints = True
            self.setSizeScatter(self.pointSize)
            self.setBrushScatter(self.pointColor)
            self.setPointOutline(self.outlineColor, self.outlineSize)
        else:
            self.showPoints = False
            self.setSizeScatter(0)

    def toggleShowCurve(self, checkBox):
        if checkBox.isChecked():
            self.showCurve = True
            self.setPenCurve(color=self.curveColor, width=self.curveSize)
            self.setShadowPen(color=self.shadowColor, width=self.shadowSize)
        else:
            self.showCurve = False
            pen = pqg.mkPen((0, 0, 0, 0), width=0)
            self.setPenCurve(pen)
            self.setShadowPen(pen)

    def toggleShowFill(self, checkBox):
        if checkBox.isChecked():
            self.showFill = True
            if self.fillLevel == None:
                self.fillLevel = 0
            self.setFillLevel(self.fillLevel)
            self.setFillBrush(self.fillColor)
        else:
            self.showFill = False
            self.setFillLevel(None)

    def selectDataSource(self, comboBox, index):
        """Change the dataStream from which I pull my data."""
        dsName = str(comboBox.itemText(index))
        self.ds = self.traceTab.dataStreams[dsName]
        i = self.xDataSelector.count()
        while i > 0:
            i -= 1
            self.xDataSelector.removeItem(i)

        i = self.yDataSelector.count()
        while i > 0:
            i -= 1
            self.yDataSelector.removeItem(i)

        self.xDataSelector.addItems(self.ds.argNames)
        self.xDataSelector.addItems(self.ds.valNames)
        self.yDataSelector.addItems(self.ds.argNames)
        self.yDataSelector.addItems(self.ds.valNames)

    def setPointPen(self, color, size):
        """Set pen drawing my points, size ranges from 0-100."""
        if color != self.pointColor:
            self.pointColor = color
            if self.showPoints:
                self.setBrushScatter(color)
        if size != self.pointSize:
            self.pointSize = size
            self.setPointOutline(self.outlineColor, self.outlineSize)
            if self.showPoints:
                self.setSizeScatter(size)

    def setPointOutline(self, color, size):
        """Set the pen from drawing the point outlines. Size ranges from 
        0-1 and specifies percent of the point pen size."""
        self.outlineColor = color
        self.outlineSize = size
        size = self.pointSize * self.outlineSize
        self.setPenScatter(color=color, width=size)

    def setCurvePen(self, color, size):
        """Set pen drawing my curve."""
        if color != self.curveColor or size != self.curveSize:
            self.curveColor = color
            self.curveSize = size
            self.setCurveShadow(self.shadowColor, self.shadowSize)
            if self.showCurve == True:
                self.setPenCurve(color, width=size)

    def setCurveShadow(self, color, size):
        """Set pen drawing my curve shadow, size ranges from 0-1
        and specifies percent of curve pen size."""
        self.shadowColor = color
        self.shadowSize = size
        size = self.curveSize * (1 + self.shadowSize)
        if self.showCurve == True:
            self.setShadowPen(color, width=size)

    def setFill(self, color, level):
        """Set the color and level to fill my curve."""
        if color != self.fillColor:
            self.fillColor = color
            if self.showFill is True:
                self.setFillBrush(color)
        if level != self.fillLevel:
            self.fillLevel = level
            if self.showFill is True:
                self.setFillLvl(level)

    def setPointShape(self, comboBox):
        text = str(comboBox.currentText()).strip()
        pointDict = {'Circle': 'o', 'Square': 's',
                     'Triangle': 't', 'Diamond': 'd', 'Plus': '+'}
        if text not in pointDict.keys():
            raise GraphException(
                "{} is not a recognized point type".format(text))
        else:
            self.symbol = pointDict[text]
            self.setSymbolScatter(self.symbol)

    def toggleShow(self, checkBox):
        if checkBox.isChecked():
            self.showOnPlot = True
            self.addTo(self.traceTab.plot)
            self.onClick(lambda: self.traceTab.change_to_trace(self))
        else:
            self.showOnPlot = False
            self.removeFrom(self.traceTab.plot)

    def togglePxMode(self, checkBox):
        if checkBox.isChecked():
            self.pxMode = True
        else:
            self.pxMode = False

        self.setPoints(self.x, self.y)

    def getDataFromName(self, Name):
        Name = str(Name)
        name = Name.split('[')
        dataName = name[0].strip()

        if len(name) not in (1, 2):
            raise GraphException("{} is not a valid slice".format(Name))
        elif dataName not in self.ds.argNames:
            if dataName not in self.ds.valNames:
                message = "{} does not contain {}".format(
                    self.ds.name, dataName)
                raise GraphException(message)
        if len(name) == 1:
            return self.ds.getDataFromName(dataName)
        if len(name) == 2:
            sliceStr = name[1].split(']')
            if len(sliceStr) < 2:
                raise GraphException("{} is not a valid slice".format(Name))
            sliceStr = sliceStr[0].strip()
            return self.ds.getDataFromName(name[0], sliceStr)

    def setName(self, newName):
        """Set SELF's name to NEWNAME."""
        newName = str(newName)
        if newName == self.name():
            return
        validName = self.traceTab.rename(self, newName)
        self.NAME = validName
        self.item_name.setText(validName)

    def addTo(self, plotItem):
        """ADD SELF to PLOTITEM."""
        plotItem.addItem(self)

    def removeFrom(self, plotItem):
        """Remove SELF from PLOTITEM."""
        plotItem.removeItem(self)

    def setPoints(self, x, y):
        """dimList is a list of dimension."""
        self.x = x
        self.y = y
        pointSize = self.pointSize
        LinePen = pqg.mkPen(self.curveColor, width=self.curveSize)
        if not self.showPoints:
            pointSize = 0
        if not self.showCurve:
            LinePen = pqg.mkPen((0, 0, 0, 0), width=0)

        self.setData(x=x, y=y, symbol=self.symbol, symbolBrush=self.pointColor,
                     symbolSize=pointSize, pen=LinePen, pxMode=self.pxMode)

    def onClick(self, f):
        """Call F whenever SELF is clicked."""
        self.sigClicked.connect(f)

    def setBrushScatter(self, *args, **kargs):
        """Set my color of my points"""
        return self.setSymbolBrush(*args, **kargs)

    def setSizeScatter(self, size):
        """Set the size of my points."""
        return self.setSymbolSize(size)

    def setSymbolScatter(self, symbol):
        """Set the symbol used for my scatter plot points."""
        return self.setSymbol(symbol)

    def setPenScatter(self, *args, **kargs):
        """Set the pen outlining my points."""
        return self.setSymbolPen(*args, **kargs)

    def setPenCurve(self, *args, **kargs):
        """Set the color of my curve."""
        return self.setPen(*args, **kargs)

    def setBrushFill(self, *args, **kargs):
        """Set the brush used to fill in below my curve."""
        return self.setBrush(*args, **kargs)

    def setFillLvl(self, level):
        """Set the level to fill in below my curve."""
        return self.setFillLevel(level)

    def add_to_trace_table(self, traceTable):
        table = traceTable
        row = table.rowCount()
        table.setRowCount(row + 1)
        self.item_name = QtGui.QTableWidgetItem(self.NAME)
        self.item_name.trace = self
        table.setItem(row, 0, self.item_name)

        self.checkBoxShow = QtGui.QCheckBox()
        self.checkBoxShow.setChecked(True)
        show = lambda: self.toggleShow(self.checkBoxShow)
        self.checkBoxShow.stateChanged.connect(show)
        table.setCellWidget(row, 1, self.checkBoxShow)

        self.checkBoxUpdate = QtGui.QCheckBox()
        self.checkBoxUpdate.setChecked(False)
        self.checkBoxUpdate.stateChanged.connect(self.toggleUpdate)
        table.setCellWidget(row, 2, self.checkBoxUpdate)

        btn_delete = QtGui.QPushButton('Delete')
        btn_delete.clicked.connect(self.delete)
        table.setCellWidget(row, 4, btn_delete)

        # Add icon here if so desire.
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
