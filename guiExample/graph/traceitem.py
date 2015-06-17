import pyqtgraph as pqg
import numpy as np
from scattercurve import ScatterCurve
from pyqtgraph import ImageItem
from graphexception import GraphException

class TraceItem(object):
    count = 0
    IM = 0
    SC = 1


    def __init__(self, data = np.zeros(0), plotType = None):
        self.name = None
        self.id = TraceItem.count
        TraceItem.count += 1
        self.trace = None
        if data != np.zeros(0) and plotType != None:
            self.loadData(data, plotType)

    def setName(self, newName):
        self.name = newName

    def addTo(self, plotItem):
        self.trace.addTo(plotItem)

    def removeFrom(self, plotItem):
        self.trace.removeFrom(plotItem)

    def loadData(self, data, plotType):
        if len(data) < 2:
            raise GraphException("Must select at least 2 dimensions to plot. Cannot create trace.")
        elif plotType == TraceItem.SC:
            self.trace = ScatterCurve()
            self.setData(data)
        elif plotType == TraceItem.IM:
            self.trace = ImagePlot()
            self.setData(data)
        else:
            raise GraphException("Cannont create a trace with {} dimensions.".format(len(data)))

    def setData(self, dimList):
        """dimList is a list of dimension."""
        self.validateData(dimList)
        if self.isSC():
            self.trace.setPoints(dimList[0], dimList[1])
        if self.isImage():
            numDim = len(dimList)
            if numDim not in (2, 5, 6):
                raise GraphException("Can only create 2D Plots with 0, 3, or 4 color dimensions. {}".format(numDim))
            
            # comglomorate dimensions into a single array.
            data = self.createImageArray(dimList)
            self.trace.setImage(image = data)


    def createImageArray(self, dimList):
        """Take a list of x, y, color data and create a numpy array indexed by
        x, y that contains the color at each (x, y) pair."""
        x = dimList[0]
        y = dimList[1]
        if len(dimList) > 2:
            color = dimList[2:]
        

            
    def validateData(self, data):
        if len(data) < 2:
            raise GraphException("Must select at least 2 dimensions to plot. Cannot create trace.")

        length = len(data[0])
        for i in range(len(data)):
            dim = data[i]
            if type(dim) != np.ndarray:
                raise GraphException("Dimension {} is not a numpy ndarray. Cannot create trace".format(dim))
            if len(dim) != length:
                raise GraphException("Dimension {} is not the correct length. Cannot create trace.")

    def isImage(self):
        return isinstance(self.trace, ImageItem)

    def isSC(self):
        return isinstance(self.trace, ScatterCurve)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if self.trace == None:
                raise GraphException("No trace has been instantiated.")
            return object.__getattribute__(self.trace, name)

class ScatterCurve(object):
    count = 0

    def __init__(self, x = None, y = None):
        self.lineColor = pqg.mkColor(0, 0, 0, 255)
        self.pointColor = pqg.mkColor(0, 0, 0, 255)
        self.pointSize = 3
        self.lineSize = 3
        self.showCurve = True
        self.showScatter = True
        self.scatterPlot = pqg.ScatterPlotItem()
        self.curvePlot = pqg.PlotCurveItem()
        self.curvePlot.setClickable(True, 10)
        if x != None and y != None:
            self.xData = x
            self.yData = y
            self.setPoints()
    
    def setPoints(self, x = np.zeros(0), y = np.zeros(0), pxMode = True, antialias = False):
        """Set the data for the ScatterPlotItem and PlotCurveItem.

        pxMode -- if True then the scatter plot points are always the same size in
                  pixels, regardless of scaling.
        antialias = whether to draw the symbols and curve with antialiasing.
        """
        if x == np.zeros(0) and y == np.zeros(0):
            x = self.xData
            y = self.yData

        curvePen = pqg.mkPen(self.lineColor, width=self.lineSize)
        self.curvePlot.setData(x, y, pen=curvePen)
        self.scatterPlot.setData(x, y, pen=self.pointColor, size=self.pointSize)

    def addTo(self, plotItem):
        """Add my ScatterPlotItem and PlotCurveItem to PLOTITEM."""
        plotItem.addItem(self.curvePlot)
        plotItem.addItem(self.scatterPlot)

    def removeFrom(self, plotItem):
        """Remove my ScatterPlotItem and PlotCurveItem from PLOTITEM"""
        plotItem.removeItem(self.scatterPlot)
        plotItem.removeItem(self.curvePlot)

    def clickedConnect(self, f):
        """Connect some function f to be called when SCATTERPLOT or SCATTERCURVE is clicked."""
        self.scatterPlot.sigClicked.connect(f)
        self.curvePlot.sigClicked.connect(f)

    ############################################################
    # The following methods wrap methods from ScatterPlotItem. #
    ############################################################
    def setBrushScatter(self, *args, **kargs):
        """Wraps setBrush from ScatterPlotItem."""
        return self.scatterPlot.setBrush(*args, **kargs)

    def setSizeScatter(self, size, update = True, dataSet = None, mask = None):
        """Wraps setSize from ScatterPlotItem."""
        return self.scatterPlot.setSize(size, update, dataSet, mask)

    def setSymbolScatter(self, symbol, update = True, dataSet = None, mask = None):
        """Wraps setSymbol from ScatterPlotItem."""
        return self.scatterPlot.setSymbol(symbol, update, dataSet, mask)

    def setPenScatter(self, *args, **kargs):
        """Wraps setPen from ScatterPlotItem."""
        return self.scatterPlot.setPen(*args, **kargs)

    ##########################################################
    # The following methods wrap methods from PlotCurveItem. #
    ##########################################################
    def setBrushCurve(self, *args, **kargs):
        """Wraps setBrush from PlotCurveItem."""
        return self.curvePlot.setBrush(*args, **kargs)

    def setPenCurve(self, *args, **kargs):
        """Wraps setPen from PlotCurveItem."""
        return self.curvePlot.setPen(*args, **kargs)

    def mouseShapeCurve(self):
        """Wraps mouseShape from PlotCurveItem."""
        return self.curvePlot.mouseShape()

    def setClickableCurve(self, s, width = None):
        """Wraps setClickable from PlotCurveItem."""
        return self.curvePlot.setClickable(s, width)

    def setFillLevel(self, level):
        """Wraps setFillLevel from PlotCurveItem."""
        return self.curvePlot.setFillLevel(level)

    def setShadowPen(self, *args, **kargs):
        """Wraps setShadowPen from PlotCurveItem."""
        return self.curvePlot.setShadowPen(*args, **kargs)


class ImagePlot(ImageItem):
    
    def __init__(self):
        super(self.__class__, self).__init__()

    def addTo(self, plotItem):
        plotItem.addItem(self)

    def removeFrom(self, plotItem):
        plotItem.removeItem(self)