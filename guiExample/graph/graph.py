import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np
import Tkinter
from tkFileDialog import askopenfilename


from graph_ui import Ui_MainWindow
 

class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.loadFileButton.clicked.connect(self.loadFile)
        self.plotCurve = pqg.PlotCurveItem()
        self.plot.addItem(self.plotCurve)
        self.plot.getPlotItem().showGrid(True, True, 1.0)


    def loadFile(self):
        """ Opens a browser for the user to select a file and then
            attempts to graph the file. """

        # Initialize Tkinter and hide the main GUI window.
        root = Tkinter.Tk()
        root.withdraw()
        
        # opens a new window, and reads the selected file's path into filename.
        filename = askopenfilename()

        x, y, err = openFile(filename)
        if (err != 0):
            return

        xVals = np.array(x)
        yVals = np.array(y)
        self.plotCurve.setData(xVals, yVals)
        self.plot.sigTransformChanged

     
def openFile(path):
    """ Attempts to open the file at path PATH and returns the X, Y data.
        If there was an error also returns TRUE, else FALSE. """
    try:
        data = open(path, 'r')
    except IOError:
        print("The requested file doesn't exist.")
        return [], [], False
    
    err = 0
    x_vals = []
    y_vals = []
    for line in data:
        items = line.split()
        if len(items) != 2:
            print(len(items))
            print("Error in data stream: " + line)
            err = 1
        else:
            x_vals += [float(items[0])]
            y_vals += [float(items[1])]
    
    return x_vals, y_vals, err


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()