import os, sys
import numpy as np
from PyQt4 import QtGui, QtCore
from ImageViewTemplate_ui import *
import pyqtgraph as pqg
from pyqtgraph.graphicsItems.ImageItem import *
from pyqtgraph.graphicsItems.ROI import *
from pyqtgraph.graphicsItems.LinearRegionItem import *
from pyqtgraph.graphicsItems.InfiniteLine import *
from pyqtgraph.graphicsItems.ViewBox import *
from pyqtgraph import ptime
from pyqtgraph import debug
from pyqtgraph.SignalProxy import SignalProxy

try:
    from bottleneck import nanmin, nanmax
except ImportError:
    from numpy import nanmin, nanmax


import numpy as np
from utils import *


class ImageView(pqg.ImageView):
    def __init__(self, parent=None, name='ImageView', imageItem=None, *args):
        """
        By default, this class creates an :class:`ImageItem <pyqtgraph.ImageItem>` to display image data
        and a :class:`ViewBox <pyqtgraph.ViewBox>` to contain the ImageItem. 
        
        ============= =========================================================
        **Arguments** 
        parent        (QWidget) Specifies the parent widget to which
                      this ImageView will belong. If None, then the ImageView
                      is created with no parent.
        name          (str) The name used to register both the internal ViewBox
                      and the PlotItem used to display ROI data. See the *name*
                      argument to :func:`ViewBox.__init__() 
                      <pyqtgraph.ViewBox.__init__>`.
        view          (ViewBox or PlotItem) If specified, this will be used
                      as the display area that contains the displayed image. 
                      Any :class:`ViewBox <pyqtgraph.ViewBox>`, 
                      :class:`PlotItem <pyqtgraph.PlotItem>`, or other 
                      compatible object is acceptable.
        imageItem     (ImageItem) If specified, this object will be used to
                      display the image. Must be an instance of ImageItem
                      or other compatible object.
        ============= =========================================================
        
        Note: to display axis ticks inside the ImageView, instantiate it 
        with a PlotItem instance as its view::
                
            pg.ImageView(view=pg.PlotItem())
        """
        QtGui.QWidget.__init__(self, parent, *args)
        self.levelMax = 4096
        self.levelMin = 0
        self.name = name
        self.image = None
        self.axes = {}
        self.imageDisp = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.scene = self.ui.graphicsView.scene()

        self.ignoreTimeLine = False

        self.plotItem = pqg.PlotItem()
        self.plotItem.showGrid(True, True, 255)
        self.view = self.plotItem

        self.ui.graphicsView.setCentralItem(self.view)
        self.view.setAspectLocked(True)
        self.view.invertY()

        if imageItem is None:
            self.imageItem = pqg.ImageItem()
        else:
            self.imageItem = imageItem
        self.view.addItem(self.imageItem)
        self.currentIndex = 0

        self.ui.histogram.setImageItem(self.imageItem)

        self.menu = None

        self.ui.normGroup.hide()

        self.roi = PlotROI(10)
        self.roi.setZValue(20)
        self.view.addItem(self.roi)
        self.roi.hide()
        self.normRoi = PlotROI(10)
        self.normRoi.setPen(QtGui.QPen(QtGui.QColor(255,255,0)))
        self.normRoi.setZValue(20)
        self.view.addItem(self.normRoi)
        self.normRoi.hide()
        self.roiCurve = self.ui.roiPlot.plot()
        self.timeLine = InfiniteLine(0, movable=True)
        self.timeLine.setPen((0, 0, 0, 255), width=5)
        self.timeLine.setZValue(1)
        self.ui.roiPlot.addItem(self.timeLine)
        self.ui.splitter.setSizes([self.height()-35, 35])
        self.ui.roiPlot.hideAxis('left')

        self.keysPressed = {}
        self.playTimer = QtCore.QTimer()
        self.playRate = 0
        self.lastPlayTime = 0

        self.normRgn = LinearRegionItem()
        self.normRgn.setZValue(0)
        self.ui.roiPlot.addItem(self.normRgn)
        self.normRgn.hide()
  
        # wrap functions from view box
        for fn in ['addItem', 'removeItem']:
            setattr(self, fn, getattr(self.view, fn))

        # wrap functions from histogram
        for fn in ['setHistogramRange', 'autoHistogramRange', 'getLookupTable', 'getLevels']:
            setattr(self, fn, getattr(self.ui.histogram, fn))

        self.timeLine.sigPositionChanged.connect(self.timeLineChanged)
        self.ui.roiBtn.clicked.connect(self.roiClicked)
        self.roi.sigRegionChanged.connect(self.roiChanged)

        self.ui.menuBtn.clicked.connect(self.menuClicked)
        self.ui.normDivideRadio.clicked.connect(self.normRadioChanged)
        self.ui.normSubtractRadio.clicked.connect(self.normRadioChanged)
        self.ui.normOffRadio.clicked.connect(self.normRadioChanged)
        self.ui.normROICheck.clicked.connect(self.updateNorm)
        self.ui.normFrameCheck.clicked.connect(self.updateNorm)
        self.ui.normTimeRangeCheck.clicked.connect(self.updateNorm)
        self.playTimer.timeout.connect(self.timeout)

        self.normProxy = SignalProxy(self.normRgn.sigRegionChanged, slot=self.updateNorm)
        self.normRoi.sigRegionChangeFinished.connect(self.updateNorm)

        self.ui.roiPlot.registerPlot(self.name + '_ROI')
        self.view.register(self.name)

        self.noRepeatKeys = [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]

        self.roiClicked()  ## initialize roi plot to correct shape / visibility

        self.ui.plot_slice_vert.invertX(True)
        self.ui.plot_slice_vert
        self.xSliceCurve = self.ui.plot_slice_horiz.plot()
        self.ySliceCurve = self.ui.plot_slice_vert.plot()

        self.xSliceLine = pqg.InfiniteLine(0, 0, movable=True)
        self.ySliceLine = pqg.InfiniteLine(0, 90, movable=True)
        self.xSliceLine.setPen((200, 200, 100), width=3)
        self.ySliceLine.setPen((200, 200, 100), width=3)
        self.xSliceLine.setHoverPen((255, 0, 0), width=5)
        self.ySliceLine.setHoverPen((255, 0, 0), width=5)
        self.view.addItem(self.xSliceLine)
        self.view.addItem(self.ySliceLine)
        self.xSliceLine.sigPositionChanged.connect(self.set_x_slice)
        self.ySliceLine.sigPositionChanged.connect(self.set_y_slice)
        self.imageItem.sigImageChanged.connect(self.set_x_slice)
        self.imageItem.sigImageChanged.connect(self.set_y_slice)
        self.xSliceLine.hide()
        self.ySliceLine.hide()

        self.showXSlice = False
        self.showYSlice = False

        self.ui.plot_slice_horiz.setXLink(self.getView())
        self.ui.plot_slice_vert.setYLink(self.getView())

        gradient = self.getHistogramWidget().gradient
        gradient.colorDialog.open = gradient.colorDialog.exec_

    def enable_x_slice(self, enable):
        self.showXSlice = enable
        if enable:
            self.xSliceLine.show()
        else:
            self.xSliceLine.hide()

    def enable_y_slice(self, enable):
        self.showYSlice = enable
        if enable:
            self.ySliceLine.show()
        else:
            self.ySliceLine.hide()

    def set_x_slice(self):
        if self.showXSlice is False:
            return

        y_bounds = (0, self.imageItem.image.shape[1]-1)
        self.xSliceLine.setBounds(y_bounds)

        y_index = int(self.xSliceLine.value())

        if self.imageItem.image.ndim == 2:
            data = self.imageItem.image[:, y_index]
            x = [i for i in range(self.imageItem.image.shape[0])]
            x = np.array(x)
            self.xSliceCurve.setData(x=x, y=data)

    def set_y_slice(self):
        if self.showYSlice is False:
            return

        x_bounds = (0, self.imageItem.image.shape[0]-1)
        self.ySliceLine.setBounds(x_bounds)

        x_index = int(self.ySliceLine.value())

        if self.imageItem.image.ndim == 2:
            data = self.imageItem.image[x_index, :]
            y = [i for i in range(self.imageItem.image.shape[1])]
            y = np.array(y)
            self.ySliceCurve.setData(x=data, y=y)

    def getPlotItem(self):
        return self.plotItem

    def getView(self):
        return self.plotItem.getViewBox()

    def exportClicked(self):
        fileName = str(QtGui.QFileDialog.getSaveFileName())
        if fileName == '':
            return
        self.export(fileName)

    def export(self, fileName):
        """
        Export data from the ImageView to a file, or to a stack of files if
        the data is 3D. Saving an image stack will result in index numbers
        being added to the file name. Images are saved as they would appear
        onscreen, with levels and lookup table applied.
        """
        print('exporting')
        img = self.getProcessedImage()
        if self.hasTimeAxis():
            base, ext = os.path.splitext(fileName)
            fmt = "%%s%%0%dd%%s" % int(np.log10(img.shape[0])+1)
            for i in range(img.shape[0]):
                self.imageItem.setImage(img[i], autoLevels=False)
                self.imageItem.save(fmt % (base, i, ext))
            self.updateImage()
        else:
            self.imageItem.save(fileName)

    def get_levels(self):
        """Return the (MIN, MAX) levels used to scale my gradient."""
        return self.getHistogramWidget().getLevels()


class PlotROI(ROI):
    def __init__(self, size):
        ROI.__init__(self, pos=[0, 0], size=size)
        self.addScaleHandle([1, 1], [0, 0])
        self.addRotateHandle([0, 0], [0.5, 0.5])
