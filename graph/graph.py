import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np
from datastream import DataStream, SliceTreeItem
from graph_ui import Ui_MainWindow
from graphexception import GraphException
from traceitem import TraceItem
from imageitem import ImageItem


class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Default Fields
        self.backgroundColor = pqg.mkColor(255, 255, 255, 100)
        self.axisColor = pqg.mkColor(0, 0, 0, 255)
        self.curPlot = TraceItem()
        self.curImage = ImageItem()
        self.dataSources = {}
        self.traces = {}
        self.images = {}
        self.dataStreams = {}
        self.traceCombos = []

        # Connecting the open file menu option
        self.file_open.triggered.connect(self.loadFile)
        self.btn_loadData.clicked.connect(self.loadFile)

        # Add the grid, and get rid of the autoscale button.
        self.plot.getPlotItem().showGrid(True, True, 255)
        self.plot.getPlotItem().hideButtons()

        # Initializing the spin boxes:
        self.updateRangeBoxes()
        self.plot.getPlotItem().sigRangeChanged.connect(self.updateRangeBoxes)

        # Setting background color
        self.plot.getPlotItem().getViewBox().setBackgroundColor(self.backgroundColor)

        # Connecting buttons.
        self.btn_setRange.clicked.connect(self.setRange)
        self.btn_autoScaleX.clicked.connect(self.autoScaleX)
        self.btn_autoScaleY.clicked.connect(self.autoScaleY)

        # Connecting the check boxes.
        self.checkBox_autoScale.clicked.connect(self.setAutoScale)
        self.checkBox_connect.clicked.connect(self.connectPoints)
        self.checkBox_points.clicked.connect(self.showPoints)
        self.checkBox_grid.clicked.connect(self.showGrid)
        self.checkBox_legend.clicked.connect(self.showLegend)

        # Connecting the color buttons
        self.btn_color1.sigColorChanging.connect(self.setBackgroundColor)
        self.btn_color2.sigColorChanging.connect(self.setLineColor)
        self.btn_color3.sigColorChanging.connect(self.setPointColor)
        self.btn_color4.sigColorChanging.connect(self.setAxisColor)

        # Initializing the color buttons
        self.btn_color1.setColor(self.backgroundColor)
        self.btn_color4.setColor(self.axisColor)

        # Connecting and initializing the slider
        self.slider_pointSize.valueChanged.connect(self.setPointSize)
        self.slider_lineSize.valueChanged.connect(self.setLineSize)

        # Connecting the comboboxes
        self.comboBox_selectPlot.activated.connect(self.selectCurPlot)
        self.comboBox_selectImage.activated.connect(self.selectCurImage)
        self.comboBox_symbol.activated.connect(self.selectPointType)
        self.comboBox_symbol.addItems(["Circle", "Square", "Triangle", "Diamond", "Plus"])

        # Connecting the data tree
        self.tree_data.itemClicked.connect(self.treeItemClicked)

        # Connecting the Create New Trace button
        self.btn_newPlot.clicked.connect(self.newSC)
        self.btn_newImage.clicked.connect(self.newImage)

    def addPlot(self, trace):
        """Add a new trace to the list currenlty plotted plots."""
        self.curPlot = trace
        self.curPlot.addTo(self.plot)
        self.comboBox_selectPlot.addItem(trace.NAME)
        curIndex = len(self.traces) - 1
        self.comboBox_selectPlot.setCurrentIndex(curIndex)
        self.syncButtons()

        self.curPlot.onClick(lambda: self.changeToTrace(trace))

    def addImage(self, image):
        """Add a new image to the list of currently selectable images."""
        self.curImage = image
        self.comboBox_selectImage.addItem(image.name)
        curIndex = len(self.images) - 1
        self.comboBox_selectImage.setCurrentIndex(curIndex)
        self.syncButtons()

    def syncButtons(self):
        """Updates the GUI buttons to display the appropriate values when a new
        plot is selected or loaded."""
        self.btn_color2.setColor(self.curPlot.lineColor)
        self.btn_color3.setColor(self.curPlot.pointColor)
        self.slider_lineSize.setValue(self.curPlot.lineSize * 10)
        self.slider_pointSize.setValue(self.curPlot.pointSize * 10)
        self.checkBox_points.setChecked(self.curPlot.showScatter)
        self.checkBox_connect.setChecked(self.curPlot.showCurve)

    def loadFile(self):
        filePaths = getFilePath()
        if filePaths is None:
            return

        for path in filePaths:
            ds = DataStream(str(path))
            ds.addToTree(self)
            self.dataStreams[ds.name] = ds
            self.addDataSources(ds)

    def createNewSlice(self, ds):
        name = uniqueName("Slice {}", len(ds.slices), ds.slices)
        sliceTI = SliceTreeItem(name, ds.sliceParentTW, ds, self.updateSlice)
        index = ds.sliceParentTW.childCount() - 2
        ds.sliceParentTW.insertChild(index, sliceTI)
        ds.slices[name] = sliceTI
        path = ds.name + '.' + name
        self.dataSources[path] = (ds, "SLICE", name)
        self.addSources([path])

    def updateSlice(self, s):
        """Update SELF.SLICE to accurately represent the contents of my LineEdits."""
        tempSlice = [[0 , 0]] * len(s.slice)
        for n in range(s.childCount() - 1):
            child = s.child(n)
            lineEdit = s.treeWidget().itemWidget(child, 1)
            text = str(lineEdit.text())
            text = text.strip()
            if text == ":":
                tempSlice[n] = [0, s.limits[n]]
            else:
                items = text.split(':')
                if len(items) == 1:
                    try:
                        val = int(items[0])
                    except ValueError:
                        raise GraphException(items[0] + "is not a valid integer.")
                    if val >= 0 and val < s.limits[n]:
                        tempSlice[n] = [val]
                    else:
                        raise GraphException("{} is out of bounds.".format(val))
                elif len(items) == 2:
                    try:
                        val1 = int(items[0])
                        val2 = int(items[1])
                    except ValueError:
                        raise GraphException("{} or {} is not a valid integer.".format(items[0], items[1]))
                    if val1 < val2 and val1 >= 0 and val2 < s.limits[n]:
                        tempSlice[n] = [val1, val2]
                    else:
                        raise GraphException("One of either {} or {} is out of bounds.".format(items[0], items[1]))
                else:
                    raise GraphException("Not a valid slice.")

        s.slice = tempSlice
        s.setText(1, s.getSliceStr())
        path = s.ds.name + '.' + s.name
        self.updateSources([path])

    def addDataSources(self, dataStream):
        """Add all the slices """
        sourceNames = []
        for arg in range(dataStream.getNumArgs()):
            string = dataStream.name + '.'
            string += dataStream.argNames[arg]
            self.dataSources[string] = (dataStream, 'ARG', arg)
            sourceNames += [string]

        for val in range(dataStream.getNumVals()):
            string = dataStream.name + '.'
            string += dataStream.valNames[val]
            self.dataSources[string] = (dataStream, 'VAL', val)
            sourceNames += [string]

        for sliceName in dataStream.slices.keys():
            string = dataStream.name + '.'
            string += sliceName
            self.dataSources[string] = (dataStream, 'SLICE', sliceName)
            sourceNames += [string]

        self.addSources(sourceNames)

    def addSources(self, sourcePaths):
        """Add list of SOURCENAMES from DS to the data selecting combo boxes."""
        for path in sourcePaths:
            ds, source, tag = self.dataSources[path]
            if ds.getSourceDim(source, tag) == 1:
                for trace in self.traces.itervalues():
                    for comboBox in trace.comboBoxes:
                        comboBox.addItem(path)

            if ds.getSourceDim(source, tag) in (2, 3, 4):
                for image in self.images.itervalues():
                    for comboBox in image.comboBoxes:
                        comboBox.addItem(path)

    def removeSources(self, sourcePaths):
        """for for each path in SOURCEPATHS remove path from the combo boxes
        and then re-add it to the appropriate ones."""
        for path in sourcePaths:
            for trace in self.traces.itervalues():
                for comboBox in trace.comboBoxes:
                    index = comboBox.findText(path)
                    if index != -1:
                        comboBox.removeItem(index)

            for image in self.images.itervalues():
                for comboBox in image.comboBoxes:
                    index = comboBox.findText(path)
                    if index != -1:
                        comboBox.removeItem(index)

    def updateSources(self, sourcePaths):
        """for for each path in SOURCEPATHS remove path from the combo boxes
        and then re-add it to the appropriate ones."""
        self.removeSources(sourcePaths)
        self.addSources(sourcePaths)

    def sourceNames(self, *dims):
        """Return a list of current data source (args, vals, slices) names
        of dimension DIM."""
        names = []
        for ds, source, tag in self.dataSources.values():
            if ds.getSourceDim(source, tag) in dims:
                name = ds.name + '.'
                name += ds.getSourceName(source, tag)
                names += [name]

        return names

    def treeItemClicked(self, item, column):
        """Handles a click in column COLUMN of item ITEM in SELF.TREE_DATA."""
        return

    def newSC(self):
        trace = TraceItem()
        trace.setName(uniqueName("Trace {}", 0, self.traces))
        self.traces[trace.NAME] = trace
        trace.addToTree(self)

    def newImage(self):
        image = ImageItem()
        image.setName(uniqueName("Image {}", 0, self.images))
        self.images[image.name] = image
        image.addToTree(self)




    #########################################
    #### Methods Dealing with Plot Table ####
    #########################################

    def addToTree(self, dataStream):
        """Add a DataStream DATASTREAM to the TREE_PLOTS."""
        raise NotImplementedError()
        # dimNum = dataStream.dimensions()
        # if dimNum < 2:
        #     raise GraphException("Must have at least 2 dimensions to plot")
        # if dimNum < 5:
        #     data = [dataStream.getDimension(i) for i in range(0, 2)]
        #     trace = TraceItem(data, TraceItem.SC)
        #     dim1 = dataStream.name + '.' + dataStream.dimName(0)
        #     dim2 = dataStream.name + '.' + dataStream.dimName(1)
        #     trace.dimensionNames = [str(dim1), str(dim2)]
        # if dimNum >= 5:
        #     dimNum = min(dimNum, 6)
        #     data = [dataStream.getDimension(i) for i in range(0, dimNum)]
        #     trace = TraceItem(data, TraceItem.IM)

        # trace.setName(uniqueName("Trace {}", 0, self.traces))
        # self.traces[trace.NAME] = trace
        # self.addTraceToTree(trace, self.traces)
    

    def setSCData(self, trace, dim1String, dim2String):
        baseMessage = "The trace won't be updated until the selected dimensions are valid."
        ds1, source1, tag1 = self.dataSources[str(dim1String)]
        ds2, source2, tag2 = self.dataSources[str(dim2String)]

        dim1 = ds1.getSourceDim(source1, tag1)
        dim2 = ds1.getSourceDim(source1, tag1)
        if (dim1 != dim2) or (dim1 != 1):
            message = "Dimension error. "
            message += baseMessage
            raise GraphException(message)

        x = ds1.getData(source1, tag1)
        y = ds2.getData(source2, tag2)

        if len(x) != len(y):
            message = "Sources are not of the same lengths. "
            message += baseMessage
            raise GraphException(message)

        trace.setPoints(x, y)

    def setImageData(self, image, dataPath):
        ds, source, tag = self.dataSources[str(dataPath)]

        if ds.getSourceDim(source, tag) not in (2, 3, 4):
            raise GraphException("Can only create images with 2-4D data.")

        image.setData(ds, source, tag)

    def setTraceName(self, trace, name, lineEdit):
        oldName = trace.NAME
        if name in self.traces.keys():
            lineEdit.setText(oldName)
            raise GraphException("Duplicate names not allowed.")
        else:
            self.traces.pop(oldName)
            trace.setName(name)
            self.traces[trace.NAME] = trace
            index = self.comboBox_selectPlot.findText(oldName)
            self.comboBox_selectPlot.setItemText(index, name)

    def setImageName(self, image, name, lineEdit):
        oldName = image.name
        if name in self.images.keys():
            lineEdit.setText(oldName)
            raise GraphException("Duplicate names not allowed.")
        else:
            self.images.pop(oldName)
            image.setName(name)
            self.images[image.name] = image
            index = self.comboBox_selectImage.findText(oldName)
            self.comboBox_selectImage.setItemText(index, name)

    def toggleUpdate(self, sc):
        raise NotImplementedError()

    def toggleShow(self, trace, checkBox):
        if checkBox.isChecked():
            self.addPlot(trace)
        else:
            trace.removeFrom(self.plot)                  
            index = self.comboBox_selectPlot.findText(trace.NAME)
            self.comboBox_selectPlot.removeItem(index)

    def toggleShowImage(self, image, checkBox):
        if checkBox.isChecked():
            self.addImage(image)
        else:
            image.removeFrom(self.image)                  
            index = self.comboBox_selectPlot.findText(image.name)
            self.comboBox_selectImage.removeItem(index)

    
    ##########################################
    #### Methods dealing with the plot tab ###
    ##########################################

    def setRange(self):
        """ Sets the range of the graph to the values in the spin boxes. """
        x_min = self.spin_x_min.value()
        x_max = self.spin_x_max.value()
        y_min = self.spin_y_min.value()
        y_max = self.spin_y_max.value()
        self.plot.setRange(xRange=(x_min, x_max), yRange=(y_min, y_max), padding = False)
        self.checkBox_autoScale.setChecked(False)
        self.plot.enableAutoRange(enable=False)

    def autoScaleX(self):
        """ Auto scales the x axis such that all item are viewable. """
        x_maxRange, y_maxRange = self.plot.getPlotItem().getViewBox().childrenBounds()
        if x_maxRange is None:
            return
        
        self.plot.setRange(xRange=x_maxRange, padding=False)

    def autoScaleY(self):
        """ Auto scales the y axis such that all item are viewable. """
        x_maxRange, y_maxRange = self.plot.getPlotItem().getViewBox().childrenBounds()
        if y_maxRange == None:
            return

        self.plot.setRange(yRange = y_maxRange, padding = False)

    def updateRangeBoxes(self):
        """ Sets the values of the spin boxes to the current viewable range."""
        ((x_min, x_max), (y_min, y_max)) = self.plot.viewRange()
        self.spin_x_min.setValue(float(x_min))
        self.spin_x_max.setValue(float(x_max))
        self.spin_y_min.setValue(float(y_min))
        self.spin_y_max.setValue(float(y_max))

    def setAutoScale(self):
        """ Toggles auto scale, which constantly updates the viewable range such that all
        items are within view."""
        enable = self.checkBox_autoScale.isChecked()
        self.plot.enableAutoRange(enable = enable)

    def connectPoints(self):
        """Toggles whether the points are connected by lines or not."""
        enable = self.checkBox_connect.isChecked()
        if enable:
            self.curPlot.showCurve = True
            self.curPlot.setPenCurve(color = self.curPlot.lineColor, width = self.curPlot.lineSize)
        else:
            self.curPlot.showCurve = False
            clear = pqg.mkColor(0, 0, 0, 0)
            self.curPlot.setPenCurve(clear)

    def showPoints(self):
        """ Toggles points on or off. """
        enable = self.checkBox_points.isChecked()
        if enable:
            self.curPlot.showScatter = True
            self.curPlot.setSizeScatter(self.curPlot.pointSize)
        else:
            self.curPlot.showScatter = False
            self.curPlot.setSizeScatter(0)

    def showGrid(self):
        """ Toggles the grid on or off. """
        enable = self.checkBox_grid.isChecked()
        if enable:
            self.plot.getPlotItem().getAxis('left').setGrid(255)
            self.plot.getPlotItem().getAxis('bottom').setGrid(255)
        else:
            self.plot.getPlotItem().getAxis('left').setGrid(False)
            self.plot.getPlotItem().getAxis('bottom').setGrid(False)

    def showLegend(self):
        if self.checkBox_legend.isChecked():
            self.legend = pqg.LegendItem()
            for trace in self.traces.itervalues():
                self.legend.addItem(trace, trace.NAME)
            self.legend.setParentItem(self.plot.getPlotItem())
        elif self.legend != None:
            vb = self.plot.getPlotItem().getViewBox()
            vb.removeItem(self.legend)
            self.legend = None

    def setBackgroundColor(self):
        """ Sets the background color to the value of the value of BTN_COLOR1."""
        self.backgroundColor = self.btn_color1.color()
        self.plot.getPlotItem().getViewBox().setBackgroundColor(self.backgroundColor)

    def setLineColor(self):
        """ Sets the line color to the value of BTN_COLOR2. """
        self.curPlot.lineColor = self.btn_color2.color()
        self.curPlot.setPenCurve(color=self.curPlot.lineColor, width=self.curPlot.lineSize)

    def setPointColor(self):
        """ Sets the point color to the value of BTN_COLOR3. """
        self.curPlot.pointColor = self.btn_color3.color()
        self.curPlot.setBrushScatter(self.curPlot.pointColor)
        self.curPlot.setPenScatter(self.curPlot.pointColor)

    def setAxisColor(self):
        """ Sets the axis color to the value of btn_color4. """
        self.axisColor = self.btn_color4.color()
        self.plot.getPlotItem().getAxis('left').setPen(self.axisColor)
        self.plot.getPlotItem().getAxis('bottom').setPen(self.axisColor)

    def setPointSize(self):
        """ Sets the point size to one tenth of the SLIDER_POINTSIZE value."""
        self.curPlot.pointSize = float(self.slider_pointSize.value()) / 10
        self.curPlot.setSizeScatter(self.curPlot.pointSize)

    def setLineSize(self):
        """ Sets the line size to one tenth of the SLIDER_LINESIZE value."""
        self.curPlot.lineSize = float(self.slider_lineSize.value()) / 10
        self.curPlot.setPenCurve(color = self.curPlot.lineColor, width = self.curPlot.lineSize)

    def selectCurPlot(self):
        """Change the current editable plot to that in the COMBOBOX_SELECTPLOT.""" 
        name = self.comboBox_selectPlot.currentText()
        self.changeToIndex(name)

    def selectCurImage(self):
        """Change the current visible Image to that in the COMBOBOX_SELECTPLOT."""
        name = self.comboBox_selectImage.currentText()
        self.changeToImage(name)

    def changeToImage(self, name):
        name = str(name)
        index = self.comboBox_selectImage.findText(name, QtCore.Qt.MatchExactly)
        if name not in self.images.keys():
            raise GraphException("Cannot find trace {}.".format(name))
        if index < 0:
            raise GraphException("Cannot find trace {} in ComboBox.".format(name))
        
        img = self.images[name]
        self.image.setImage(img.getData())
        self.comboBox_selectImage.setCurrentIndex(index)

    def selectPointType(self):
        index = self.comboBox_symbol.currentIndex()
        if index == 0:
            self.curPlot.setSymbolScatter('o')
        elif index == 1:
            self.curPlot.setSymbolScatter('s')
        elif index == 2:
            self.curPlot.setSymbolScatter('t')
        elif index == 3:
            self.curPlot.setSymbolScatter('d')
        elif index == 4:
            self.curPlot.setSymbolScatter('+')
        else:
            raise GraphException("Can't set point type to None. {}".format(index))

    def changeToTrace(self, trace):
        """Change the current plot to TRACE."""
        self.changeToIndex(trace.NAME)

    def changeToIndex(self, name):
        """Change the current plot to the plot NAME."""
        index = self.comboBox_selectPlot.findText(name, QtCore.Qt.MatchExactly)
        if name not in self.traces.keys():
            raise GraphException("Cannot find trace {}.".format(name))
        if index < 0:
            raise GraphException("Cannot find trace {} in ComboBox.".format(name))

        self.curPlot = self.traces[str(name)]
        self.syncButtons()
        self.comboBox_selectPlot.setCurrentIndex(index)


def getFilePath(caption='', dir='', filter=''):
    """Opens a OS native file browser in Windows / OSX.
    Returns a list of paths to the selected files."""
    f = QtGui.QFileDialog.getOpenFileNames
    return f(caption=caption, directory=dir, filter=filter)


def uniqueName(baseName, baseNum, nameList):
    """Return a new name formed from BASENAME.format(BASENUM) that is not
    in nameList."""
    name = baseName.format(baseNum)
    while name in nameList:
        baseNum += 1
        name = baseName.format(baseNum)
    return name


pqg.setConfigOptions(background='w')
# pqg.setConfigOptions(foreground='b')
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()