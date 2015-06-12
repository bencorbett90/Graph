import pyqtgraph as pqg
import numpy as np

class ScatterCurve():
    def __init__(self, x = np.zeros(0), y = np.zeros(0)):
        self.xData = np.zeros(0)
        self.yData = np.zeros(0)
        self.lineColor = pqg.mkColor(0, 0, 0, 255)
        self.pointColor = pqg.mkColor(0, 0, 0, 255)
        self.pointSize = 3
        self.lineSize = 3
        self.suppliedDim = 0
        self.scatterPlot = pqg.ScatterPlotItem()
        self.curvePlot = pqg.PlotCurveItem()
        self.curvePlot.setClickable(True, 10)
        self.validateData(x, y)
        self.graph()

    def validateData(self, x, y):
        if type(x) != np.ndarray or type(y) != np.ndarray:
            raise Exception("Data is not a numpy ndarray.")
        if len(x) == len(y) == 0:
            self.suppliedDim = 0
        elif len(x) == 0 and len(y) > 0:
            self.suppliedDim = 1
            self.yData = y
            self.setXRange()
        elif len(x) > 0 and len(y) == 0:
            self.suppliedDim = 1
            self.yData = x
            self.setXRange()
        elif len(x) != len(y):
            raise Exception("Dimensions of x, y data don't match.")
        elif len(x) == len(y):
            self.suppliedDim = 2
            self.xData = x
            self.yData = y

    def setXRange(self, xMin = 0, xMax = 10):
        """When no x data supplied, must interpolate a range. Evenly distributes the y
        values over [XMIN, XMAX]."""
        if self.suppliedDim != 1:
            raise Exception("Can only set X range with 1D data")
        numPoints = len(self.yData)
        step = float((xMin - xMax)) / float(numPoints)
        self.xData = np.zeros(numPoints)
        
        for i in range(numPoints):
            self.xData[i] = xMin + (step * i)

    def graph(self, pxMode = True, antialias = False):
        """Set the data for the ScatterPlotItem and PlotCurveItem.

        pxMode -- if True then the scatter plot points are always the same size in
                  pixels, regardless of scaling.
        antialias = whether to draw the symbols and curve with antialiasing.
        """
        curvePen = pqg.mkPen(self.lineColor, width = self.lineSize)
        self.curvePlot.setData(self.xData, self.yData, pen = curvePen)
        self.scatterPlot.setData(self.xData, self.yData, pen = self.pointColor, size = self.pointSize)

    def setPoints(self, x = np.zeros(0), y = np.zeros(0)):
        self.validateData(x, y)
        self.graph()

    def addTo(self, plotItem):
        """Add my ScatterPlotItem and PlotCurveItem to PLOTITEM."""
        plotItem.addItem(self.scatterPlot)
        plotItem.addItem(self.curvePlot)


    #
    # The following methods wrap methods from ScatterPlotItem.
    #
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

    #
    # The following methods wrap methods from PlotCurveItem.
    #
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