import pyqtgraph as pqg
from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotDataItem
from graphexception import GraphException


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
        self.fillLevel = None
        self.pxMode = True
        self.x = None
        self.y = None
        
        self.symbol = 'o'
        self.showCurve = True
        self.showPoints = True
        self.showFill = False
        self.sourceSelector = None
        self.xDataSelector = None
        self.yDataSelector = None
        self.ds = None
        self.id = TraceItem.count
        TraceItem.count += 1
        self.curve.setClickable(30)


    def name(self):
        return self.NAME

    def toggleUpdate(self):
        """Turn on/off automatic updating when the trace is refreshed."""
        return

    def toggleShowPoints(self, checkBox):
        if checkBox.isChecked():
            self.showPoints = True
            self.setSizeScatter(self.pointSize)
            self.setBrushScatter(self.pointColor)
            self.setPointOutline(self.outlineColor, self.outlineSize * 100)
        else:
            self.showPoints = False
            self.setSizeScatter(0)

    def toggleShowCurve(self, checkBox):
        if checkBox.isChecked():
            self.showCurve = True
            self.setPenCurve(color=self.curveColor, width=self.curveSize)
            self.setShadowPen(color=self.shadowColor, width=self.shadowSize*100)
        else:
            self.showCurve = False
            pen = pqg.mkPen((0, 0, 0, 0), width = 0)
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
        size = size / 5.0

        if color != self.pointColor:
            self.pointColor = color
            if self.showPoints:
                self.setBrushScatter(color)
        if size != self.pointSize:     
            self.pointSize = size
            self.setPointOutline(self.outlineColor, self.outlineSize * 100)
            if self.showPoints:
                self.setSizeScatter(size)

    def setPointOutline(self, color, size):
        """Set the pen from drawing the point outlines. Size ranges from 
        0-100 and specifies percent of the point pen size."""
        self.outlineColor = color
        self.outlineSize = size / 100.0
        size = self.pointSize * self.outlineSize
        self.setPenScatter(color=color, width=size)

    def setCurvePen(self, color, size):
        """Set pen drawing my curve, size ranges from 0-100."""
        size = size / 5
        if color != self.curveColor or size != self.curveSize:
            self.curveColor = color
            self.curveSize = size
            self.setPenShadow(self.shadowColor, self.shadowSize * 100)
            if self.showCurve == True:
                self.setPenCurve(color, width=size)
                
    def setPenShadow(self, color, size):
        """Set pen drawing my curve shadow, size ranges from 0-100
        and specifies percent of curve pen size."""
        self.shadowColor = color
        self.shadowSize = size / 100.0
        size = self.curveSize * (1 + self.shadowSize)
        if self.showCurve == True:
            self.setShadowPen(color, width=size)

    def setFill(self, color, level):
        """Set the color and level to fill my curve."""
        if color != self.fillColor:
            self.fillColor = color
            if self.showFill == True:
                self.setFillBrush(color)
        if level != self.fillLevel:
            self.fillLevel = level
            if self.showFill == True:
                self.setFillLvl(level)

    def setPointShape(self, comboBox):
        text = str(comboBox.currentText()).strip()
        pointDict = {'Circle' : 'o', 'Square': 's', 'Triangle': 't', 'Diamond': 'd', 'Plus': '+'}
        if text not in pointDict.keys():
            raise GraphException("{} is not a recognized point type".format(text))
        else:
            self.setSymbolScatter(pointDict[text])            

    def toggleShow(self, checkBox):
        if checkBox.isChecked():
            self.addTo(self.traceTab.plot)
            self.onClick(lambda: self.traceTab.changeToTrace(self))
        else:
            self.removeFrom(self.traceTab.plot)

    def togglePxMode(self, checkBox):
        if checkBox.isChecked():
            self.pxMode = True
        else:
            self.pxMode = False

        self.setPoints(self.x, self.y)

    def setTraceName(self, name, lineEdit):
        oldName = self.NAME
        if name in self.traceTab.traces.keys():
            lineEdit.setText(oldName)
            raise GraphException("Duplicate names not allowed.")
        else:
            self.traceTab.traces.pop(oldName)
            self.setName(name)
            self.traceTab.traces[self.NAME] = self

    def setTraceData(self, index):
        xString = str(self.xDataSelector.currentText())
        xData = self.getDataFromName(xString)

        yString = str(self.yDataSelector.currentText())
        yData = self.getDataFromName(yString)

        self.setPoints(xData, yData)

    def getDataFromName(self, Name):
        Name = str(Name)
        name = Name.split('[')
        dataName = name[0].strip()

        if len(name) not in (1, 2):
            raise GraphException("{} is not a valid slice".format(Name))
        elif dataName not in self.ds.argNames:
            if dataName not in self.ds.valNames:
                message = "{} does not contain {}".format(self.ds.name, dataName)
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
        self.NAME = str(newName)

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
        LinePen = pqg.mkPen(self.curveColor, width=self.curveSize)
        self.setData(x=x, y=y, symbol=self.symbol, symbolBrush=self.pointColor,
                     symbolSize=self.pointSize, pen=LinePen, pxMode=self.pxMode)

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


    def addToTree(self, traceTab):
        """Add my TraceItem to traceTab.TREE_TRACE."""

        tree = traceTab.tree_trace
        updateData = traceTab.setSCData
        dataStreamNames = traceTab.dataStreams.keys()

        parentTWI = QtGui.QTreeWidgetItem()
        tree.addTopLevelItem(parentTWI)

        # Adding the lineedit for the trace name
        nameBox = QtGui.QLineEdit(self.NAME)
        f = lambda name: self.setTraceName(name, nameBox)
        nameBox.textEdited.connect(f)
        tree.setItemWidget(parentTWI, 0, nameBox)

        # Adding the checkbox for showing the trace
        checkBoxShow = QtGui.QCheckBox("Show")
        show = lambda: self.toggleShow(checkBoxShow)
        checkBoxShow.stateChanged.connect(show)
        checkBoxShow.setChecked(True)
        tree.setItemWidget(parentTWI, 1, checkBoxShow)

        # Adding the data parent item and update check box
        dataParent = QtGui.QTreeWidgetItem(['Data'])
        parentTWI.addChild(dataParent)
        checkBoxUpdate = QtGui.QCheckBox("Update")
        checkBoxUpdate.stateChanged.connect(self.toggleUpdate)
        checkBoxUpdate.setChecked(False)
        tree.setItemWidget(dataParent, 1, checkBoxUpdate)

        # Adding the sourceSelector
        childSource = QtGui.QTreeWidgetItem(['Source'])
        dataParent.addChild(childSource)
        comboSource = QtGui.QComboBox()
        comboSource.addItems(dataStreamNames)
        comboSource.setEditable(True)
        selectSource = lambda index: self.selectDataSource(comboSource, index)
        comboSource.activated.connect(selectSource)
        tree.setItemWidget(childSource, 1, comboSource)
        self.sourceSelector = comboSource

        # Adding xData selector
        childX = QtGui.QTreeWidgetItem(['x'])
        dataParent.addChild(childX)
        comboX = QtGui.QComboBox()
        comboX.setEditable(True)
        comboX.activated.connect(self.setTraceData)
        tree.setItemWidget(childX, 1, comboX)
        self.xDataSelector = comboX

        # Adding yData selector
        childY = QtGui.QTreeWidgetItem(['y'])
        dataParent.addChild(childY)
        comboY = QtGui.QComboBox()
        comboY.setEditable(True)
        comboY.activated.connect(self.setTraceData)
        tree.setItemWidget(childY, 1, comboY)
        self.yDataSelector = comboY

        # Adding the point parent item and show check box
        pointParent = QtGui.QTreeWidgetItem(['Points'])
        parentTWI.addChild(pointParent)
        checkBoxShowPoints = QtGui.QCheckBox("Show")
        showPoints = lambda : self.toggleShowPoints(checkBoxShowPoints)
        checkBoxShowPoints.stateChanged.connect(showPoints)
        checkBoxShowPoints.setChecked(True)
        tree.setItemWidget(pointParent, 1, checkBoxShowPoints)

        # Adding the pen selector
        childPen = QtGui.QTreeWidgetItem(['Pen'])
        pointParent.addChild(childPen)
        colorBtnPen = pqg.ColorButton(color=self.pointColor)
        sliderPen = QtGui.QSlider(QtCore.Qt.Horizontal)
        sliderPen.setRange(0, 100)
        sliderPen.setSingleStep(1)
        sliderPen.setPageStep(10)
        tree.setItemWidget(childPen, 1, colorBtnPen)
        tree.setItemWidget(childPen, 2, sliderPen)

        colorFunc1 = colorBtnPen.color
        sizeFunc1 = sliderPen.value
        setPointPen = lambda : self.setPointPen(colorFunc1(), sizeFunc1())
        colorBtnPen.sigColorChanging.connect(setPointPen)
        sliderPen.valueChanged.connect(setPointPen)

        # Adding the outline pen selector
        childOutline = QtGui.QTreeWidgetItem(['Outline Pen'])
        pointParent.addChild(childOutline)
        colorBtnOutline = pqg.ColorButton(color=self.outlineColor)
        sliderOutline = QtGui.QSlider(QtCore.Qt.Horizontal)
        sliderOutline.setRange(0, 100)
        sliderOutline.setSingleStep(1)
        sliderOutline.setPageStep(10)
        tree.setItemWidget(childOutline, 1, colorBtnOutline)
        tree.setItemWidget(childOutline, 2, sliderOutline)

        colorFunc2 = colorBtnOutline.color
        sizeFunc2 = sliderOutline.value
        setPointOutline = lambda : self.setPointOutline(colorFunc2(), sizeFunc2())
        colorBtnOutline.sigColorChanging.connect(setPointOutline)
        sliderOutline.valueChanged.connect(setPointOutline)

        # Adding the point shape selector
        childPointShape = QtGui.QTreeWidgetItem(['Shape'])
        pointParent.addChild(childPointShape)
        comboPoints = QtGui.QComboBox()
        comboPoints.addItems(["Circle", "Square", "Triangle", "Diamond", 'Plus'])
        tree.setItemWidget(childPointShape, 1, comboPoints)
        setPointShape = lambda index: self.setPointShape(comboPoints)
        comboPoints.activated.connect(setPointShape)
        checkBoxPxMode = QtGui.QCheckBox("pxMode")
        checkBoxPxMode.setChecked(True)
        togglePxMode = lambda : self.togglePxMode(checkBoxPxMode)
        checkBoxPxMode.stateChanged.connect(togglePxMode)
        tree.setItemWidget(childPointShape, 2, checkBoxPxMode)


        # Adding the curve parent item and show check box
        curveParent = QtGui.QTreeWidgetItem(['Curve'])
        parentTWI.addChild(curveParent)
        checkBoxShowCurve = QtGui.QCheckBox("Show")
        showCurve = lambda : self.toggleShowCurve(checkBoxShowCurve)
        checkBoxShowCurve.stateChanged.connect(showCurve)
        checkBoxShowCurve.setChecked(True)
        tree.setItemWidget(curveParent, 1, checkBoxShowCurve)
        checkBoxShowFill = QtGui.QCheckBox("Show Fill")
        checkBoxShowFill.setChecked(False)
        showFill = lambda : self.toggleShowFill(checkBoxShowFill)
        checkBoxShowFill.stateChanged.connect(showFill)
        tree.setItemWidget(curveParent, 2, checkBoxShowFill)

        # Adding the curve pen selector
        childCurvePen = QtGui.QTreeWidgetItem(['Pen'])
        curveParent.addChild(childCurvePen)
        colorBtnCurve = pqg.ColorButton(color=self.curveColor)
        sliderCurve = QtGui.QSlider(QtCore.Qt.Horizontal)
        sliderCurve.setRange(0, 100)
        sliderCurve.setSingleStep(1)
        sliderCurve.setPageStep(10)
        tree.setItemWidget(childCurvePen, 1, colorBtnCurve)
        tree.setItemWidget(childCurvePen, 2, sliderCurve)

        colorFunc3 = colorBtnCurve.color
        sizeFunc3 = sliderCurve.value
        setCurvePen = lambda : self.setCurvePen(colorFunc3(), sizeFunc3())
        colorBtnCurve.sigColorChanging.connect(setCurvePen)
        sliderCurve.valueChanged.connect(setCurvePen)

        # Adding the curve shadow pen selector
        childShadowPen = QtGui.QTreeWidgetItem(['Shadow Pen'])
        curveParent.addChild(childShadowPen)
        colorBtnShadow = pqg.ColorButton(color=self.shadowColor)
        sliderShadow = QtGui.QSlider(QtCore.Qt.Horizontal)
        sliderShadow.setRange(0, 100)
        sliderShadow.setSingleStep(1)
        sliderShadow.setPageStep(10)
        tree.setItemWidget(childShadowPen, 1, colorBtnShadow)
        tree.setItemWidget(childShadowPen, 2, sliderShadow)

        colorFunc4 = colorBtnShadow.color
        sizeFunc4 = sliderShadow.value
        setShadowPen = lambda : self.setPenShadow(colorFunc4(), sizeFunc4())
        colorBtnShadow.sigColorChanging.connect(setShadowPen)
        sliderShadow.valueChanged.connect(setShadowPen)

        # Adding the fill selector
        childFill = QtGui.QTreeWidgetItem(['Fill'])
        curveParent.addChild(childFill)
        colorBtnFill = pqg.ColorButton(color=self.fillColor)
        spinFill = pqg.SpinBox()
        spinFill.setOpts(step=1)
        tree.setItemWidget(childFill, 1, colorBtnFill)
        tree.setItemWidget(childFill, 2, spinFill)

        colorFunc5 = colorBtnFill.color
        sizeFunc5 = spinFill.value
        setFill = lambda : self.setFill(colorFunc5(), sizeFunc5())
        colorBtnFill.sigColorChanging.connect(setFill)
        spinFill.sigValueChanging.connect(setFill)

        self.spinFill = spinFill
