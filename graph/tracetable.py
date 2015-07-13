from PyQt4 import QtGui
import pyqtgraph as pqg


class TraceTable():

    def __init__(self, table, graph):
        super(TraceTable, self).__init__()
        self.graph = graph

    def addToTable(self, table):
        """Add all of my fields to the TABLE."""
        tableItem = QtGui.QTableWidgetItem
        table.setColumnCount(2)
        table.setRowCount(10)

        table.setItem(0, 0, tableItem('Background Color'))
        table.setItem(1, 0, tableItem('Show Grid'))
        table.setItem(2, 0, tableItem('Grid Color'))
        table.setItem(3, 0, tableItem('Show Legend'))
        table.setItem(4, 0, tableItem('Show Line'))
        table.setItem(5, 0, tableItem('Show Points'))
        table.setItem(6, 0, tableItem('Line Color'))
        table.setItem(7, 0, tableItem('Point Color'))
        table.setItem(8, 0, tableItem('Line Size'))
        table.setItem(9, 0, tableItem('Point Size'))
        table.setItem(10, 0, tableItem('Shadow Color'))
        table.setItem(11, 0, tableItem('Point Outline'))

        # Taking care of color buttons.
        self.backGroundColor = pqg.ColorButton()
        self.backGroundColor.sigColorChanging.connect(self.setBackgroundColor)
        table.setCellWidget(0, 1, self.backGroundColor)

        self.gridColor = pqg.ColorButton()
        self.gridColor.sigColorChanging.connect(self.setGridColor)
        table.setCellWidget(2, 1, self.gridColor)

        self.lineColor = pqg.ColorButton()
        self.lineColor.sigColorChanging.connect(self.setLineColor)
        table.setCellWidget(6, 1, self.lineColor)

        self.pointColor = pqg.ColorButton()
        self.pointColor.sigColorChanging.connect(self.setPointColor)
        table.setCellWidget(7, 1, self.pointColor)

        self.shadowColor = pqg.ColorButton()
        self.shadowColor.sigColorChanging.connect(self.setShadowColor)
        table.setCellWidget(7, 1, self.shadowColor)

        self.outlineColor = pqg.ColorButton()
        self.outlineColor.sigColorChanging.connect(self.setOutlineColor)
        table.setCellWidget(7, 1, self.outlineColor)

        # Taking care of check boxes
        self.showGrid = QtGui.QCheckBox()
        self.showGrid.stateChanged.connect(self.toggleGrid)
        table.setCellWidget(1, 1, self.showGrid)

        self.showLegend = QtGui.QCheckBox()
        self.showLegend.stateChanged.connect(self.toggleLegend)
        table.setCellWidget(3, 1, self.showLegend)

        self.showLine = QtGui.QCheckBox()
        self.showLine.stateChanged.connect(self.toggleLine)
        table.setCellWidget(4, 1, self.showLine)

        self.showPoints = QtGui.QCheckBox()
        self.showPoints.stateChanged.connect(self.togglePoints)
        table.setCellWidget(5, 1, self.showPoints)

        # Taking care of sliders
        self.lineSize = QtGui.QSlider()
        self.lineSize.setMinimum(0)
        self.lineSize.setMaximum(500)
        self.lineSize.setTickInterval(50)
        self.lineSize.setPageStep(50)
        self.lineSize.setSingleStep(1)
        self.lineSize.valueChanged.connect(self.setLineSize)
        table.setCellWidget(8, 1, self.lineSize)

        self.pointSize = QtGui.QSlider()
        self.pointSize.setMinimum(0)
        self.pointSize.setMaximum(500)
        self.pointSize.setTickInterval(50)
        self.pointSize.setPageStep(50)
        self.pointSize.setSingleStep(1)
        self.pointSize.valueChanged.connect(self.setPointSize)
        table.setCellWidget(9, 1, self.pointSize)


    def setBackgroundColor(self):
        """ Sets the background color to the value of the value of backGroundColor."""
        color = self.backGroundColor.color()
        self.graph.plot.getPlotItem().getViewBox().setBackgroundColor(color)

    def setGridColor(self):
        """ Sets the axis color to the value of pointColor. """
        axisColor = self.pointColor.color()
        self.graph.plot.getPlotItem().getAxis('left').setPen(axisColor)
        self.graph.plot.getPlotItem().getAxis('bottom').setPen(axisColor)

    def setLineColor(self):
        """ Sets the line color to the value of lineColor. """
        curPlot = self.graph.curPlot
        curPlot.lineColor = self.lineColor.color()
        curPlot.setPenCurve(color=curPlot.lineColor, width=curPlot.lineSize)

    def setPointColor(self):
        """ Sets the point color to the value of lineColor. """
        curPlot = self.graph.curPlot
        curPlot.pointColor = self.lineColor.color()
        curPlot.setBrushScatter(curPlot.pointColor)
        curPlot.setPenScatter(curPlot.pointColor)

    def setShadowColor(self):
        curPlot = self.graph.curPlot
        curPlot.shadowColor = self.shadowColor.color()
        curPlot.setPenShadow(color=curPlot.shadowColor, width=curPlot.lineSize + 1)

    def setOutlineColor(self):
        curPlot = self.graph.curPlot
        curPlot.outlineColor = self.outlineColor.color()
        curPlot.setPenScatter(curPlot.outlineColor)

    def toggleLine(self):
        """Toggles whether the points are connected by lines or not."""
        curPlot = self.graph.curPlot
        if self.showLine.isChecked():
            curPlot.showCurve = True
            curPlot.setPenCurve(color=curPlot.lineColor, width=curPlot.lineSize)
        else:
            curPlot.showCurve = False
            clear = pqg.mkColor(0, 0, 0, 0)
            curPlot.setPenCurve(clear)

    def togglePoints(self):
        """ Toggles points on or off. """
        curPlot = self.graph.curPlot
        if self.showPoints.isChecked():
            curPlot.showScatter = True
            curPlot.setSizeScatter(self.curPlot.pointSize)
        else:
            curPlot.showScatter = False
            curPlot.setSizeScatter(0)
            
    def setPointSize(self):
        """ Sets the point size to one tenth of the SLIDER_POINTSIZE value."""
        curPlot = self.graph.curPlot
        curPlot.pointSize = float(self.pointSize.value()) / 10
        curPlot.setSizeScatter(self.curPlot.pointSize)

    def setLineSize(self):
        """ Sets the line size to one tenth of the SLIDER_LINESIZE value."""
        curPlot = self.graph.curPlot
        curPlot.lineSize = float(self.lineSize.value()) / 10
        curPlot.setPenCurve(color=self.curPlot.lineColor, width=self.curPlot.lineSize)
