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
        self.enableSetRange = True
        self.enableUpdateBoxes = True

        # Add the grid, and get rid of the autoscale button.
        self.plot.getPlotItem().showGrid(True, True, 255)
        self.plot.getPlotItem().hideButtons()

        # Initializing the spin boxes:
        self.spin_x_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_x_max.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_y_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_y_max.setOpts(step=.1, dec=True, minStep=.1)
        self.plot.getPlotItem().sigRangeChanged.connect(self.updateRangeBoxes)
        self.spin_x_min.valueChanged.connect(self.setRange)
        self.spin_x_max.valueChanged.connect(self.setRange)
        self.spin_y_min.valueChanged.connect(self.setRange)
        self.spin_y_max.valueChanged.connect(self.setRange)
        self.updateRangeBoxes()

        # Setting background color
        self.plot.getPlotItem().getViewBox().setBackgroundColor(self.backgroundColor)

        # Connecting buttons.
        self.btn_autoScaleX.clicked.connect(self.autoScaleX)
        self.btn_autoScaleY.clicked.connect(self.autoScaleY)

        # Connecting the check boxes.
        self.checkBox_showGrid.setChecked(True)
        self.checkBox_showGrid.clicked.connect(self.showGrid)
        self.checkBox_showLegend.clicked.connect(self.showLegend)
        self.checkBox_logX.clicked.connect(self.toggleLogX)
        self.checkBox_logY.clicked.connect(self.toggleLogY)

        # Connecting the color buttons
        self.btnColor_background.sigColorChanging.connect(self.setBackgroundColor)
        self.btnColor_grid.sigColorChanging.connect(self.setGridColor)

        # Initializing the color buttons
        self.btnColor_background.setColor(self.backgroundColor)
        self.btnColor_grid.setColor(self.gridColor)

        # Connecting the Create New Trace button
        self.btn_newTrace.clicked.connect(self.newTrace)

    def toggleLogX(self):
        if self.checkBox_logX.isChecked():
            self.plot.getPlotItem().setLogMode(x=True)
        else:
            self.plot.getPlotItem().setLogMode(x=False)

    def toggleLogY(self):
        if self.checkBox_logY.isChecked():
            self.plot.getPlotItem().setLogMode(y=True)
        else:
            self.plot.getPlotItem().setLogMode(y=False)

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
        if self.enableUpdateBoxes:
            self.enableSetRange = False
            ((x_min, x_max), (y_min, y_max)) = self.plot.getPlotItem().viewRange()
            self.spin_x_min.setValue(float(x_min))
            self.spin_x_max.setValue(float(x_max))
            self.spin_y_min.setValue(float(y_min))
            self.spin_y_max.setValue(float(y_max))
            self.enableSetRange = True
            autoRange = self.plot.getPlotItem().getViewBox().autoRangeEnabled()
            self.btn_autoScaleX.setChecked(autoRange[0])
            self.btn_autoScaleY.setChecked(autoRange[1])
    
    def setRange(self):
        if self.enableSetRange:
            self.enableUpdateBoxes = False
            x_min = self.spin_x_min.value()
            x_max = self.spin_x_max.value()
            y_min = self.spin_y_min.value()
            y_max = self.spin_y_max.value()
            self.plot.getPlotItem().setRange(xRange=(x_min, x_max), yRange=(y_min, y_max), padding=False)
            self.enableUpdateBoxes = True
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

    
