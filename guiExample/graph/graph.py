import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np
import Tkinter
from tkFileDialog import askopenfilename

from datastream import DataTxtFile, DataStream
from graph_ui import Ui_MainWindow
from graphexception import GraphException
from traceitem import TraceItem
 

class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Default Fields
        self.backgroundColor = pqg.mkColor(255, 255, 255, 100)
        self.axisColor = pqg.mkColor(0, 0, 0, 255)
        self.plots = []
        self.curPlot = TraceItem()
        self.selectedDimensions = []
        self.tabs = ['None', 'Tab1']
        self.dimDict = {}
        self.traces = {}
        self.dimensionSelectors = []
        
        # Connecting the open file menu option
        self.file_open.triggered.connect(self.loadTxtFile)
        self.btn_loadData.clicked.connect(self.loadTxtFile)
        
        # Add the curve to the PlotItem.
        self.plots = []
        
        # Add the grid, and get rid of the autoscale button.
        self.plot.getPlotItem().showGrid(True, True, 1)
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
        self.comboBox_symbol.activated.connect(self.selectPointType)
        self.comboBox_symbol.addItems(["Circle", "Square", "Triangle", "Diamond", "Plus"])

        # Connecting the data tree
        self.tree_data.itemClicked.connect(self.treeItemClicked)

        # Connecting the Create New Trace button
        self.btn_newTrace.clicked.connect(self.newTrace)


    def addPlot(self, sc):
        """Add a new plot consisting of x, y data to the plots."""
        self.curPlot = sc
        self.curPlot.addTo(self.plot)
        self.plots += [self.curPlot]
        self.comboBox_selectPlot.addItem(sc.name)
        curIndex = len(self.plots) - 1
        self.comboBox_selectPlot.setCurrentIndex(curIndex)
        self.syncButtons()

        self.curPlot.clickedConnect(lambda: self.changeToSC(sc))

    def syncButtons(self):
        """Updates the GUI buttons to display the appropriate values when a new
        plot is selected or loaded."""
        self.btn_color2.setColor(self.curPlot.lineColor)
        self.btn_color3.setColor(self.curPlot.pointColor)
        self.slider_lineSize.setValue(self.curPlot.lineSize * 10)
        self.slider_pointSize.setValue(self.curPlot.pointSize * 10)
        self.checkBox_points.setChecked(self.curPlot.showScatter)
        self.checkBox_connect.setChecked(self.curPlot.showCurve)

    def loadTxtFile(self):
        """ Opens a browser for the user to select a file and then
            attempts to graph the file. """

        filePath = getFilePath()
        txtFile = DataTxtFile(filePath)
        self.addDataToTree(txtFile)

    def addDataToTree(self, dataStream):
        """Add a DataStream DATASTREAM to the TREE_DATA."""
        tree = self.tree_data
        
        # create a new QTreeWidgetItem that will be the parent TreeWidget.
        parentTW = QtGui.QTreeWidgetItem([dataStream.getName()])
        
        # Since the parent TreeWidgetItem represents the DataStream and not
        # one of it's dimensions, set its DIMDATA field to NONE.
        parentTW.dimData = np.zeros(0)
        parentTW.parent = True

        # add the default view of this stream to the Table and graph it 
        self.addToTree(dataStream)

        # populate the TreeWidget with children that comprise it's dimensions.
        for dim in range(dataStream.dimensions()):
            
            # create a new child TreeWidget and set it to be checkable
            childTW = QtGui.QTreeWidgetItem([dataStream.dimName(dim)])
            childTW.setFlags(QtCore.Qt.ItemIsUserCheckable)
            childTW.setCheckState(1, QtCore.Qt.Unchecked)
            
            # attatch the dimension data to the child
            childTW.dimData = dataStream.getDimension(dim)
            childTW.parent = False

            # Set the text color
            childTW.setTextColor(0, QtGui.QColor(0, 0, 0))
            childTW.setTextColor(1, QtGui.QColor(0, 0, 0))
            
            # add the child to the parent TreeWidget 
            parentTW.addChild(childTW)

        self.addDimensions(dataStream) 

        # finally add the parent TreeWidgetItem to the tree
        tree.addTopLevelItem(parentTW)

    def addDimensions(self, dataStream):
        newDimNames = []
        for dim in range(dataStream.dimensions()):
            string = dataStream.name + '.'
            string += dataStream.dimName(dim)
            self.dimDict[string] = (dataStream, dim)
            newDimNames += [string]
        self.updateComboDim(newDimNames)

    def updateComboDim(self, newDimNames):
        for comboBox in self.dimensionSelectors:
            comboBox.addItems(newDimNames)

    def treeItemClicked(self, item, column):
        """Handles a click in column COLUMN of item ITEM."""
        
        # if it's the parent item do nothing.
        if item.parent == True:
            return
        # if ITEM is unchecked: check it, and add the associated data  
        elif item.checkState(1) == QtCore.Qt.Unchecked:
            item.setCheckState(1, QtCore.Qt.Checked)
            self.selectedDimensions += [item.dimData]
        # else it's checkd, so uncheck it and remove it's dimension from the list.
        else:
            item.setCheckState(1, QtCore.Qt.Unchecked)
            self.selectedDimensions.remove(item.dimData)

    #########################################
    #### Methods Dealing with Plot Table ####
    #########################################

    def newTrace(self):
        """Create a new trace/plot from the selected dimensions"""
        dimList = self.selectedDimensions
        dimNum = len(dimList)
        
        # uncheck all of the DataStream dimension check boxes
        self.deselectDataStreams()
        
        # currently don't support displaying more than 2D data.
        if dimNum not in (2, 5, 6):
            self.selectedDimensions = []
            raise GraphException("Improper number of dimensions selected: {}".format(dimNum))
        
        if dimNum == 2:
        	trace = TraceItem(dimList, TraceItem.SC)
        	self.addTraceToTree(trace)

        if dimNum in (5, 6):
        	trace = TraceItem(dimList, TraceItem.IM)
        	self.addTraceToTree(trace)

        # clear the list of selected dimensions.
        self.selectedDimensions = []

    def deselectDataStreams(self):
        """Uncheck all of the data streams. Used after creating a new plot."""
        # raise NotImplementedError()
        print ("deselectDataStreams not implimented")
        return

    def addToTree(self, dataStream):
        """Add a DataStream DATASTREAM to the TREE_PLOTS."""
        dimNum = dataStream.dimensions()
        if dimNum < 2:
        	raise GraphException("Must have at least 2 dimensions to plot")
        if dimNum < 5:
        	data = [dataStream.getDimension(i) for i in range(0, 2)]
        	trace = TraceItem(data, TraceItem.SC)
        if dimNum >= 5:
        	dimNum = min(dimNum, 6)
        	data = [dataStream.getDimension(i) for i in range(0, dimNum)]
        	trace = TraceItem(data, TraceItem.IM)

        self.addTraceToTree(trace)
    

    def addTraceToTree(self, trace, traceType = TraceItem.SC):
        tree = self.tree_trace
        parentTWI = QtGui.QTreeWidgetItem()
        tree.addTopLevelItem(parentTWI)

        nameBox = QtGui.QLineEdit(trace.name)
        updateName = lambda name: self.setTraceName(trace, name, nameBox)
        nameBox.textEdited.connect(updateName)
        tree.setItemWidget(parentTWI, 0, nameBox)

        checkBoxShow = QtGui.QCheckBox("Show")
        # show = lambda: self.toggleShow(trace, checkBoxShow)
        # checkBoxShow.setChecked(True)
        # checkBoxShow.stateChanged.connect(show)
        tree.setItemWidget(parentTWI, 1, checkBoxShow)
        
        checkBoxUpdate = QtGui.QCheckBox("Update")
        update = lambda: self.toggleUpdate(trace, checkBoxUpdate)
        checkBoxShow.setChecked(False)
        checkBoxShow.stateChanged.connect(update)
        tree.setItemWidget(parentTWI, 2, checkBoxUpdate) 

        if traceType == TraceItem.SC:
            childX = QtGui.QTreeWidgetItem(['x values'])
            parentTWI.addChild(childX)
            comboBoxX = QtGui.QComboBox()
            comboBoxX.addItems(self.dimDict.keys())
            tree.setItemWidget(childX, 1, comboBoxX)

            childY = QtGui.QTreeWidgetItem(['y values'])
            parentTWI.addChild(childY)
            comboBoxY = QtGui.QComboBox()
            comboBoxY.addItems(self.dimDict.keys())
            tree.setItemWidget(childY, 1, comboBoxY)

            curText1 = comboBoxX.currentText
            curText2 = comboBoxY.currentText
            loadData = lambda name: self.setTraceData(trace, curText1(), curText2())
            comboBoxX.activated.connect(loadData)
            comboBoxY.activated.connect(loadData)
            self.dimensionSelectors += [comboBoxX, comboBoxY]

    def setTraceData(self, trace, dim1String, dim2String):
        print(dim1String, dim2String)

    def setTraceName(self, trace, name, lineEdit):
        print(name)

    def updateName(self, textBox, trace, row):
        newName = textBox.text()
        if newName == trace.name:
            return
        elif not self.uniquePlotName(newName, row):
            textBox.setText(newName + '*')
        else:
            oldName = trace.name
            trace.setName(newName)
            index = self.comboBox_selectPlot.findText(oldName)
            self.comboBox_selectPlot.setItemText(index, newName)

    def uniquePlotName(self, name, exceptRow):
        """Search the plot table for names, and return True if name is not one of them."""
        names = []
        for row in range(self.table_plots.rowCount()):
            textBox = self.table_plots.cellWidget(row, 0)
            if row == exceptRow:
                continue
            if textBox != None:
                names += [textBox.text()]
        return name not in names

    def toggleUpdate(self, sc):
        raise NotImplementedError()

    def toggleShow(self, trace, checkBox):
        if checkBox.isChecked():
            self.addPlot(trace)
        else:
            trace.removeFrom(self.plot)
            
            index = None
            for i in range(len(self.plots)):
                if self.plots[i].id == trace.id:
                    index = i
            self.plots.pop(index)                   
            index = self.comboBox_selectPlot.findText(trace.name)
            self.comboBox_selectPlot.removeItem(index)

    
    ##########################################
    #### Methods dealing with the plot tab ###
    ##########################################

    def setRange(self):
        """ Sets the range of the graph to the values in the spin boxes. """
        x_min = self.spin_x_min.value()
        x_max = self.spin_x_max.value()
        y_min = self.spin_y_min.value()
        y_max = self.spin_y_max.value()
        self.plot.setRange(xRange = (x_min, x_max), yRange = (y_min, y_max), padding = False)
        self.checkBox_autoScale.setChecked(False)
        self.plot.enableAutoRange(enable = False)

    def autoScaleX(self):
        """ Auto scales the x axis such that all item are viewable. """
        x_maxRange, y_maxRange = self.plot.getPlotItem().getViewBox().childrenBounds()
        if x_maxRange == None:
            return
            
        self.plot.setRange(xRange = x_maxRange, padding = False)

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

    def setBackgroundColor(self):
        """ Sets the background color to the value of the value of BTN_COLOR1."""
        self.backgroundColor = self.btn_color1.color()
        self.plot.getPlotItem().getViewBox().setBackgroundColor(self.backgroundColor)

    def setLineColor(self):
        """ Sets the line color to the value of BTN_COLOR2. """
        self.curPlot.lineColor = self.btn_color2.color()
        self.curPlot.setPenCurve(color = self.curPlot.lineColor, width = self.curPlot.lineSize)

    def setPointColor(self):
        """ Sets the point color to the value of BTN_COLOR3. """
        self.curPlot.pointColor = self.btn_color3.color()
        self.curPlot.setBrushScatter(self.curPlot.pointColor)

    def setAxisColor(self):
        """ Sets the axis color to the value of btn_color4. """
        self.axisColor = self.btn_color4.color()
        self.plot.getPlotItem().getAxis('left').setPen(self.axisColor)
        self.plot.getPlotItem().getAxis('bottom').setPen(self.axisColor)

    def setPointsCircle(self):
        """ Sets the points to circles."""
        self.curPlot.setSymbolScatter('o')
    
    def setPointsSquare(self):
        """ Sets the points to squares."""
        self.curPlot.setSymbolScatter('s')
    
    def setPointsTriangle(self):
        """ Sets the points to triangles."""
        self.curPlot.setSymbolScatter('t')
    
    def setPointsDiamond(self):
        """ Sets the points to diamonds."""
        self.curPlot.setSymbolScatter('d')
    
    def setPointsPlus(self):
        """ Sets the points to plus signs."""
        self.curPlot.setSymbolScatter('+')

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
        index = self.comboBox_selectPlot.currentIndex()
        self.changeToIndex(index)

    def selectPointType(self):
        index = self.comboBox_symbol.currentIndex()
        if index == 0:
            self.setPointsCircle()
        if index == 1:
            self.setPointsSquare()
        if index == 2:
            self.setPointsTriangle()
        if index == 3:
            self.setPointsDiamond()
        if index == 4:
            self.setPointsPlus()
        else:
            raise GraphException("Can't set point type to None. {}".format(index))

    def changeToSC(self, sc):
        """Change the current plot to SC."""
        index = self.comboBox_selectPlot.findText(sc.name, QtCore.Qt.MatchExactly)
        self.changeToIndex(index)

    def changeToIndex(self, index):
        """Change the current plot to SELF.PLOTS[INDEX]."""
        if index < len(self.plots):
            self.curPlot = self.plots[index]
            self.syncButtons()
            self.comboBox_selectPlot.setCurrentIndex(index)


def getFilePath():
    """ Opens a Tkinter GUI to select a file. Returns the path of that file. """
    # Initialize Tkinter and hide the main GUI window.
    root = Tkinter.Tk()
    root.withdraw()
    
    # opens a new window, and returns the selected file's path.
    return askopenfilename()


pqg.setConfigOptions(background='w')
# pqg.setConfigOptions(foreground='b')
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
sys.exit(app.exec_())