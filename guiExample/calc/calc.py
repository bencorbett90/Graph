import sys
from PyQt4 import QtCore, QtGui

from calc_ui import Ui_MainWindow
 

 
class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.calculate.clicked.connect(self.square)
 
    def square(self):
        """ Reads in a line from LINE_X, and writes it's square to
        	LINE_X2. """
        	
        val = float(self.line_x.text())
        self.line_x2.setText(str(val * val))
 
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()