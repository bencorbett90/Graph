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
        self.file_open.triggered.connect(self.loadPlot)
            
        u = lambda: thread.start_new_thread(self.updatePlot, ())
        self.file_update.triggered.connect(u)
        
        self.plotCurve = pqg.PlotCurveItem()
        self.plot.addItem(self.plotCurve)
        self.plot.getPlotItem().showGrid(True, True, 1.0)

        self.updateFilePath = None



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



    def plotFile(self, filePath):
        """Plot the file at FILEPATH."""
        
        # open the file, read, in the data and check for error
        x, y, err = openFile(filePath)
        if (err != 0):
            return
    
        # convert to numpy arrays
        xVals = np.array(x)
        yVals = np.array(y)
    
        # plot and signal an update
        self.plotCurve.setData(xVals, yVals)
        self.plot.sigTransformChanged



    def loadPlot(self):
        """ Opens a browser for the user to select a file and then
            attempts to graph the file. """

        filePath = getFilePath()
        self.plotFile(filePath)

        

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
    try:
        data = open(path, 'r')
    except IOError:
        print("The requested file doesn't exist: " + path)
        return [], [], False
    
    err = 0
    x_vals = []
    y_vals = []

    # Read the file into x_vals, y_vals. If there is an error, set err to 1.
    lineNum = 1
    for line in data:
        items = line.split()
        if len(items) != 2:
            print("Length error at line: " + str(lineNum))
            return x_vals, y_vals, err
        else:
            x_vals += [float(items[0])]
            y_vals += [float(items[1])]
        
        lineNum += 1
    return x_vals, y_vals, err


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()