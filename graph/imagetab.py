from PyQt4 import QtGui
from imagetab_ui import Ui_Form
import pyqtgraph as pqg
from imageitem import ImageItem
from utils import *


class ImageTab(QtGui.QWidget, Ui_Form):
    """A widget that represents one tab for displaying images."""

    def __init__(self, Graph):
        """Init self in the GRAPH."""
        # Initialize the widget and UI.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

        # Default Fields
        self.graph = Graph
        self.backgroundColor = pqg.mkColor(255, 255, 255, 100)
        self.gridColor = pqg.mkColor(0, 0, 0, 255)
        self.images = {}
        self.dataStreams = Graph.dataStreams
        self.traceCombos = []
        self.legend = None
        self.name = None
        self.xRange = [0,1]
        self.yRange = [0,1]
        self.enableSetRange = True
        self.enableUpdateBoxes = True

        self.plot.getView().setAspectLocked(False)
        self.plot.getView().invertY(False)

        # Add the grid, and get rid of the autoscale button.
        self.plot.getPlotItem().showGrid(True, True, 255)
        self.plot.getPlotItem().hideButtons()

        # Initializing the spin boxes:
        self.spin_x_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_x_max.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_y_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_y_max.setOpts(step=.1, dec=True, minStep=.1)
        self.plot.getView().sigRangeChanged.connect(self.updateRangeBoxes)
        self.spin_x_min.sigValueChanged.connect(self.setRange)
        self.spin_x_max.sigValueChanged.connect(self.setRange)
        self.spin_y_min.sigValueChanged.connect(self.setRange)
        self.spin_y_max.sigValueChanged.connect(self.setRange)
        self.updateRangeBoxes()

        # Setting background color
        self.plot.getView().setBackgroundColor(self.backgroundColor)

        # Connecting the check boxes.
        self.checkBox_showGrid.setChecked(True)
        self.checkBox_showGrid.clicked.connect(self.showGrid)

        # Connecting the color buttons
        self.btnColor_background.sigColorChanging.connect(self.setBackgroundColor)
        self.btnColor_grid.sigColorChanging.connect(self.setGridColor)

        # Initializing the color buttons
        self.btnColor_background.setColor(self.backgroundColor)
        self.btnColor_grid.setColor(self.gridColor)

        # Connecting the Create New Trace button
        self.btn_newImage.clicked.connect(self.newImage)

    def addDataSource(self, ds):
        for image in self.images.itervalues():
            image.sourceSelector.addItem(ds.name)

    def setName(self, newName):
        self.name = str(newName)

    def updateRangeBoxes(self):
        """ Sets the values of the spin boxes to the current viewable range."""
        if self.enableUpdateBoxes:
            self.enableSetRange = False
            ((x_min, x_max), (y_min, y_max)) = self.plot.getView().viewRange()
            self.spin_x_min.setValue(float(x_min))
            self.spin_x_max.setValue(float(x_max))
            self.spin_y_min.setValue(float(y_min))
            self.spin_y_max.setValue(float(y_max))
            self.enableSetRange = True

    def setRange(self):
        if self.enableSetRange:
            self.enableUpdateBoxes = False
            x_min = self.spin_x_min.value()
            x_max = self.spin_x_max.value()
            y_min = self.spin_y_min.value()
            y_max = self.spin_y_max.value()
            self.plot.getView().setRange(xRange=(x_min, x_max), yRange=(y_min, y_max), padding=False)
            self.enableUpdateBoxes = True
    
    def showGrid(self):
        """ Toggles the grid on or off. """
        if self.checkBox_showGrid.isChecked():
            self.plot.getPlotItem().getAxis('left').setGrid(255)
            self.plot.getPlotItem().getAxis('bottom').setGrid(255)
        else:
            self.plot.getPlotItem().getAxis('left').setGrid(False)
            self.plot.getPlotItem().getAxis('bottom').setGrid(False)

    def setBackgroundColor(self):
        """ Sets the background color to the value of the value of btnColor_background."""
        self.backgroundColor = self.btnColor_background.color()
        self.plot.getView().setBackgroundColor(self.backgroundColor)

    def setGridColor(self):
        """Sets the axis color to the value of btnColor_grid. """
        self.axisColor = self.btnColor_grid.color()
        self.plot.getPlotItem().getAxis('left').setPen(self.axisColor)
        self.plot.getPlotItem().getAxis('bottom').setPen(self.axisColor)

    def newImage(self):
        image = ImageItem(self)
        image.setName(uniqueName("Image {}", 0, self.images))
        self.images[image.name] = image
        image.addToTree(self)
