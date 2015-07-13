from PyQt4 import QtGui
from tracetab_ui import Ui_Form
import pyqtgraph as pqg
from traceitem import TraceItem
from utils import *


class TraceTab(QtGui.QWidget, Ui_Form):
    """A widget that represents one tab for displaying traces."""

    def __init__(self, Graph):
        """Add SELF to PARENT in GRAPH, which should be a tab page."""
        # Initialize the widget and UI.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

        # Default Fields
        self.graph = Graph
        self.backgroundColor = pqg.mkColor(255, 255, 255, 100)
        self.gridColor = pqg.mkColor(0, 0, 0, 255)
        self.traces = {}
        self.dataStreams = Graph.dataStreams
        self.traceCombos = []
        self.legend = None
        self.name = None

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
        self.checkBox_showGrid.clicked.connect(self.showGrid)
        self.checkBox_showLegend.clicked.connect(self.showLegend)

        # Connecting the color buttons
        self.btnColor_background.sigColorChanging.connect(self.setBackgroundColor)
        self.btnColor_grid.sigColorChanging.connect(self.setGridColor)

        # Initializing the color buttons
        self.btnColor_background.setColor(self.backgroundColor)
        self.btnColor_grid.setColor(self.gridColor)

        # Connecting the Create New Trace button
        self.btn_newTrace.clicked.connect(self.newTrace)

    def deleteTab(self):
        for trace in self.traces.itervalues():
            trace.destroy()

        self.traces = None
        self.Graph = None

        self.destroy()

    def setName(self, newName):
        self.name = str(newName)

    def addDataSource(self, ds):
        for trace in self.traces.itervalues():
            trace.sourceSelector.addItem(ds.name)

    def updateRangeBoxes(self):
        """ Sets the values of the spin boxes to the current viewable range."""
        ((x_min, x_max), (y_min, y_max)) = self.plot.viewRange()
        self.spin_x_min.setValue(float(x_min))
        self.spin_x_max.setValue(float(x_max))
        self.spin_y_min.setValue(float(y_min))
        self.spin_y_max.setValue(float(y_max))

    def setRange(self):
        """ Sets the range of the graph to the values in the spin boxes. """
        x_min = self.spin_x_min.value()
        x_max = self.spin_x_max.value()
        y_min = self.spin_y_min.value()
        y_max = self.spin_y_max.value()
        self.plot.setRange(xRange=(x_min, x_max), yRange=(y_min, y_max), padding = False)
        self.btn_autoScaleX.setChecked(False)
        self.btn_autoScaleY.setChecked(False)
        self.plot.enableAutoRange(enable=False)

    def autoScaleX(self):
        """ Auto scales the x axis such that all item are viewable. """
        enable = self.btn_autoScaleX.isChecked()
        XAxis = pqg.ViewBox.XAxis
        self.plot.enableAutoRange(axis=XAxis, enable=enable)

    def autoScaleY(self):
        """ Auto scales the y axis such that all item are viewable. """
        enable = self.btn_autoScaleY.isChecked()
        YAxis = pqg.ViewBox.YAxis
        self.plot.enableAutoRange(axis=YAxis, enable=enable)

    def showGrid(self):
        """ Toggles the grid on or off. """
        enable = self.checkBox_showGrid.isChecked()
        if enable:
            self.plot.getPlotItem().getAxis('left').setGrid(255)
            self.plot.getPlotItem().getAxis('bottom').setGrid(255)
        else:
            self.plot.getPlotItem().getAxis('left').setGrid(False)
            self.plot.getPlotItem().getAxis('bottom').setGrid(False)

    def showLegend(self):
        if self.checkBox_showLegend.isChecked():
            self.legend = pqg.LegendItem()
            for trace in self.traces.itervalues():
                self.legend.addItem(trace, trace.NAME)
            self.legend.setParentItem(self.plot.getPlotItem())
        elif self.legend != None:
            vb = self.plot.getPlotItem().getViewBox()
            vb.removeItem(self.legend)
            self.legend = None

    def setBackgroundColor(self):
        """ Sets the background color to the value of the value of btnColor_background."""
        self.backgroundColor = self.btnColor_background.color()
        self.plot.getPlotItem().getViewBox().setBackgroundColor(self.backgroundColor)

    def setGridColor(self):
        """Sets the axis color to the value of btnColor_grid. """
        self.axisColor = self.btnColor_grid.color()
        self.plot.getPlotItem().getAxis('left').setPen(self.axisColor)
        self.plot.getPlotItem().getAxis('bottom').setPen(self.axisColor)

    def newTrace(self):
        trace = TraceItem(self)
        trace.setName(uniqueName("Trace {}", 0, self.traces))
        self.traces[trace.NAME] = trace
        trace.addToTree(self)

    def addPlot(self, trace):
        """Add a new trace to the list currenlty plotted plots."""

    def syncButtons(self):
        """Updates the GUI buttons to display the appropriate values when a new
        plot is selected or loaded."""
        self.btn_color2.setColor(self.curPlot.lineColor)
        self.btn_color3.setColor(self.curPlot.pointColor)
        self.slider_lineSize.setValue(self.curPlot.lineSize * 10)
        self.slider_pointSize.setValue(self.curPlot.pointSize * 10)
        self.checkBox_points.setChecked(self.curPlot.showScatter)
        self.checkBox_connect.setChecked(self.curPlot.showCurve)

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

    def setLineColor(self):
        """ Sets the line color to the value of BTN_COLOR2. """
        self.curPlot.lineColor = self.btn_color2.color()
        self.curPlot.setPenCurve(color=self.curPlot.lineColor, width=self.curPlot.lineSize)

    def setPointColor(self):
        """ Sets the point color to the value of BTN_COLOR3. """
        self.curPlot.pointColor = self.btn_color3.color()
        self.curPlot.setBrushScatter(self.curPlot.pointColor)
        self.curPlot.setPenScatter(self.curPlot.pointColor)

    def setPointSize(self):
        """ Sets the point size to one tenth of the SLIDER_POINTSIZE value."""
        self.curPlot.pointSize = float(self.slider_pointSize.value()) / 10
        self.curPlot.setSizeScatter(self.curPlot.pointSize)

    def setLineSize(self):
        """ Sets the line size to one tenth of the SLIDER_LINESIZE value."""
        self.curPlot.lineSize = float(self.slider_lineSize.value()) / 10
        self.curPlot.setPenCurve(color = self.curPlot.lineColor, width = self.curPlot.lineSize)

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
