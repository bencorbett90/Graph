import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np

from graph_ui import Ui_MainWindow
 

class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.calculate.clicked.connect(self.updateGraph)
        self.plotCurve = pqg.PlotCurveItem()
        self.plot.addItem(self.plotCurve)
        self.numPoints = 1
 
    def updateGraph(self):
    	xVals = []
    	yVals = []
    	for i in range(self.numPoints):
    		xVals += [i]
    		yVals += [i*i]

    	xVals = np.array(xVals)
    	yVals = np.array(yVals)
    	self.plotCurve.setData(xVals, yVals)
    	self.plot.sigTransformChanged
    	self.numPoints += 1


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()