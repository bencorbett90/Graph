import pyqtgraph as pqg
import numpy as np
from pyqtgraph import PlotDataItem
from pyqtgraph import ImageItem
from graphexception import GraphException

class TraceItem(PlotDataItem, object):
    count = 0

    def __init__(self,  *args, **kargs):
        super(self.__class__, self).__init__(*args, **kargs)
        self.name = None
        self.lineColor = pqg.mkColor(0, 0, 0, 255)
        self.pointColor = pqg.mkColor(0, 0, 0, 255)
        self.pointSize = 3
        self.lineSize = 3
        self.symbol = 'o'
        self.showCurve = True
        self.showScatter = True
        self.comboBoxes = ()
        
        self.id = TraceItem.count
        TraceItem.count += 1

    def addToTree(self, Graph):
        """Add my TraceItem to GRAPH.TREE_TRACE."""

        tree = Graph.tree_trace
        updateName = Graph.setTraceName
        toggleShow = Graph.toggleShow
        updateData = Graph.setSCData
        comboNames = Graph.sourceNames(1)

        parentTWI = QtGui.QTreeWidgetItem()
        tree.addTopLevelItem(parentTWI)

        nameBox = QtGui.QLineEdit(self.name)
        f = lambda name: updateName(self, name, nameBox)
        nameBox.textEdited.connect(f)
        tree.setItemWidget(parentTWI, 0, nameBox)

        checkBoxShow = QtGui.QCheckBox("Show")
        show = lambda: toggleShow(trace, checkBoxShow)
        checkBoxShow.stateChanged.connect(show)
        checkBoxShow.setChecked(True)
        tree.setItemWidget(parentTWI, 1, checkBoxShow)
  
        childX = QtGui.QTreeWidgetItem(['x values'])
        parentTWI.addChild(childX)
        combo1 = QtGui.QComboBox()
        
        combo1.addItems(comboNames)
        tree.setItemWidget(childX, 1, combo1)

        childY = QtGui.QTreeWidgetItem(['y values'])
        parentTWI.addChild(childY)
        combo2 = QtGui.QComboBox()
        
        combo2.addItems(comboNames)
        tree.setItemWidget(childY, 1, combo2)

        curText1 = combo1.currentText
        curText2 = combo2.currentText
        loadData = lambda name: updateData(trace, curText1(), curText2())
        combo1.activated.connect(loadData)
        combo2.activated.connect(loadData)
        self.comboBoxes = (combo1, combo2)

    def setSCData(self, trace, dim1String, dim2String):
        dsX, dimX = self.dimDict[str(dim1String)]
        x = dsX.getDimension(dimX)

        dsY, dimY = self.dimDict[str(dim2String)]
        y = dsY.getDimension(dimY)

        if len(x) != len(y):
            message = "Dimensions are of unequal lengths. The trace won't be updated until the selected dimensions are valid."
            raise GraphException(message)
        trace.setData((x, y))


    def setName(self, newName):
        """Set SELF's name to NEWNAME."""
        self.name = str(newName)

    def addTo(self, plotItem):
        """ADD SELF to PLOTITEM."""
        plotItem.addItem(self)

    def removeFrom(self, plotItem):
        """Remove SELF from PLOTITEM."""
        plotItem.removeItem(self)

    def setPoints(self, x, y):
        """dimList is a list of dimension."""
        LinePen = pqg.mkPen(self.lineColor, width = self.lineSize)
        self.setData(x, y, symbol = self.symbol, symbolBrush = self.pointColor,
                    symbolSize = self.pointSize, pen = LinePen)
    
    def onClick(self, f):
        """Call F whenever SELF is clicked."""
        self.sigClicked.connect(f)

    def setBrushScatter(self, *args, **kargs):
        """Set my color of my points"""
        return self.setSymbolBrush(args, kargs)

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

    def setPenShadow(self, *args, **kargs):
        """Set the pen that draws the shadow of my curve."""
        return self.setShadowPen(*args, **kargs)

class ImagePlot(ImageItem):
    def __init__(self):
        super(self.__class__, self).__init__()

    def addTo(self, plotItem):
        plotItem.addItem(self)

    def removeFrom(self, plotItem):
        plotItem.removeItem(self)