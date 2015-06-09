import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np
import Tkinter
import thread
import time
from tkFileDialog import askopenfilename


from graph_ui import Ui_MainWindow
 

class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Default Fields
        self.updateFilePath = None
        self.filePath = None
        self.lineColor = pqg.mkColor(0, 0, 0, 255)
        self.pointColor = pqg.mkColor(0, 0, 0, 255)
        self.backgroundColor = pqg.mkColor(255, 255, 255, 100)
        self.axisColor = pqg.mkColor(0, 0, 0, 255)
        self.xVals = np.empty((0, 0))
        self.yVals = np.empty((0, 0))
        self.pointSize = 3
        self.lineSize = 3

        # Connecting the open file menu option
        self.file_open.triggered.connect(self.loadPlot)
        
        # Connecting the update menu option. Starts the polling on a new thread.
        u = lambda: thread.start_new_thread(self.updatePlot, ())
        self.file_update.triggered.connect(u)
        
        # Add the curve to the PlotItem.
        self.plotCurve = pqg.PlotCurveItem()
        self.plot.addItem(self.plotCurve)

        # Add the scatter plot to the PlotItem.
        self.plotScatter = pqg.ScatterPlotItem()
        self.plot.addItem(self.plotScatter)
        
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
        self.btn_color2.setColor(self.lineColor)
        self.btn_color3.setColor(self.pointColor)
        self.btn_color4.setColor(self.axisColor)

        # Connecting the drop down menu
        self.list_pointShapes.clicked.connect(self.popup_menu)

        # Connecting and initializing the slider
        self.slider_pointSize.valueChanged.connect(self.setPointSize)
        self.slider_lineSize.valueChanged.connect(self.setLineSize)
        self.slider_lineSize.setValue(self.lineSize * 10)
        self.slider_pointSize.setValue(self.pointSize * 10)


    def updatePlot(self):
        """ Allows the user to select an update file, which will tell the program to track
            a file and display any changes. The file must be in the format of a number signifing
            a time stamp of when the file was last formatted, and then a line with the file path.
            The program will only display the updated data when the timestamp is greater than the
            previous stamp. """

        filePath = getFilePath()
        dataPath = None
        prevTime = 0.0

        while True:
            try:
                data = open(filePath, 'r')
            except IOError:
                print("The requested file doesn't exist: " + filePath)
                return
            
            lineCount = sum(1 for line in open(filePath))
            
            if lineCount == 2:
                curTime = float(data.next())
                if curTime > prevTime:
                    prevTime = curTime
                    dataPath = data.next().strip()
                    self.plotFile(dataPath)

            data.close()
            time.sleep(1)


    def plotFile(self, filePath, connect = True):
        """Plot the file at FILEPATH."""
        
        # open the file, read, in the data and check for error
        x, y, err = openFile(filePath)
        if (err != 0):
            return

        self.filePath = filePath
    
        # convert to numpy arrays
        self.xVals = np.array(x)
        self.yVals = np.array(y)
    
        # plot
        curvePen = pqg.mkPen(self.lineColor, width = self.lineSize)
        self.plotCurve.setData(x = self.xVals, y = self.yVals, pen = curvePen)
        self.plotScatter.setData(self.xVals, self.yVals, pen = self.pointColor, size = self.pointSize)


    def loadPlot(self):
        """ Opens a browser for the user to select a file and then
            attempts to graph the file. """

        filePath = getFilePath()
        self.plotFile(filePath)

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
            show = self.lineColor
            self.plotCurve.setPen(color = self.lineColor, width = self.lineSize)
            #self.plotCurve.setData(self.xVals, self.yVals, pen = show)
            # self.plotCurve.sigPlotChanged
            # print("show")
        else:
            clear = pqg.mkColor(0, 0, 0, 0)
            self.plotCurve.setPen(clear)
            #self.plotCurve.setData(self.xVals, self.yVals, pen = clear)
            # self.plotCurve.sigPlotChanged
            # print("hide")

    def showPoints(self):
        """ Toggles points on or off. """
        enable = self.checkBox_points.isChecked()
        if not enable:
            self.plotScatter.setSize(0)
        else:
            self.plotScatter.setSize(self.pointSize)

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
        self.lineColor = self.btn_color2.color()
        self.plotCurve.setPen(color = self.lineColor, width = self.lineSize)


    def setPointColor(self):
        """ Sets the point color to the value of BTN_COLOR3. """
        self.pointColor = self.btn_color3.color()
        self.plotScatter.setPen(self.pointColor)


    def setAxisColor(self):
        """ Sets the axis color to the value of btn_color4. """
        self.axisColor = self.btn_color4.color()
        self.plot.getPlotItem().getAxis('left').setPen(self.axisColor)
        self.plot.getPlotItem().getAxis('bottom').setPen(self.axisColor)


    def popup_menu(self):
        """Creates a drop down menu for the selection of shapes."""
        popup = QtGui.QMenu()
    
        popup.addAction("Circle").triggered.connect(self.setPointsCircle)
        popup.addAction("Square").triggered.connect(self.setPointsSquare)
        popup.addAction("Triangle").triggered.connect(self.setPointsTriangle)
        popup.addAction("Diamond").triggered.connect(self.setPointsDiamond)
        popup.addAction("Plus").triggered.connect(self.setPointsPlus)                                                         
        popup.exec_(self.list_pointShapes.get_last_pos())

    def setPointsCircle(self):
        """ Sets the points to circles."""
        self.plotScatter.setSymbol(symbol = 'o')
    
    def setPointsSquare(self):
        """ Sets the points to squares."""
        self.plotScatter.setSymbol(symbol = 's')
    
    def setPointsTriangle(self):
        """ Sets the points to triangles."""
        self.plotScatter.setSymbol(symbol = 't')
    
    def setPointsDiamond(self):
        """ Sets the points to diamonds."""
        self.plotScatter.setSymbol(symbol = 'd')
    
    def setPointsPlus(self):
        """ Sets the points to plus signs."""
        self.plotScatter.setSymbol(symbol = '+')

    def setPointSize(self):
        """ Sets the point size to one tenth of the SLIDER_POINTSIZE value."""
        self.pointSize = float(self.slider_pointSize.value()) / 10
        self.plotScatter.setSize(self.pointSize)

    def setLineSize(self):
        """ Sets the line size to one tenth of the SLIDER_LINESIZE value."""
        self.lineSize = float(self.slider_lineSize.value()) / 10
        self.plotCurve.setPen(color = self.lineColor, width = self.lineSize)





                

def getFilePath():
    """ Opens a Tkinter GUI to select a file. Returns the path of that file. """
    # Initialize Tkinter and hide the main GUI window.
    root = Tkinter.Tk()
    root.withdraw()
    
    # opens a new window, and returns the selected file's path.
    return askopenfilename()

     
def openFile(path):
    """ Attempts to open the file at path PATH and returns the tripple of two lists of
        x, y data and a bool signifying error. The file must be a a .txt file with two columns
        of floating point numbers x,y separated by whitespace. If there was an error the bool
        is TRUE else FALSE. """

    #Attempt to open the file and handle the error.
    if path == None:
        return [], [], 1

    try:
        data = open(path, 'r')
    except IOError:
        print("The requested file doesn't exist: " + path)
        return [], [], False
    

    x_vals = []
    y_vals = []

    # Read the file into x_vals, y_vals. If there is an error, set err to 1.
    lineNum = 1
    for line in data:
        items = line.split()
        if len(items) != 2:
            print("Length error at line: " + str(lineNum))
            return x_vals, y_vals, 1
        else:
            x_vals += [float(items[0])]
            y_vals += [float(items[1])]
        
        lineNum += 1
    return x_vals, y_vals, 0



pqg.setConfigOptions(background=None)
pqg.setConfigOptions(foreground='k')
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()