import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np
from datastream import DataStream
from graph_ui import Ui_MainWindow
from tracetab import TraceTab
from imagetab import ImageTab
from traceitem import TraceItem
from imageitem import ImageItem
import h5py
from utils import *


class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.traceTabs = {}
        self.imageTabs = {}
        self.dataStreams = {}
        self.dataSources = {}
        self.plotToPaste = None
        self.plotWasCut = False

        # Connecting the menu bar
        self.file_open.triggered.connect(self.loadFile)
        self.curPlot_copy.triggered.connect(self.copy_plot)
        self.curPlot_cut.triggered.connect(self.cut_plot)
        self.curPlot_paste.triggered.connect(self.paste_plot)
        self.curPlot_zoom_to.triggered.connect(self.zoom_to)
        self.tab_new_image.triggered.connect(self.addImageTab)
        self.tab_new_trace.triggered.connect(self.addTraceTab)

        self.comboNewTab = QtGui.QComboBox()
        self.comboNewTab.addItems(["Trace Tab", "Image Tab"])
        self.comboNewTab.activated.connect(self.newTab)
        self.tabWidget.setCornerWidget(self.comboNewTab)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        self.addTraceTab()
        self.addImageTab()

        self.first = True
        self.loadFile()

        self.tabWidget.setCurrentIndex(0)

    def copy_plot(self):
        self.plotWasCut = False
        tab = self.tabWidget.currentWidget()
        if isinstance(tab, TraceTab):
            self.plotToPaste = tab.curTrace
        if isinstance(tab, ImageTab):
            tab.curImage.gradient = tab.plot.getHistogramWidget().gradient.saveState()
            tab.curImage.levels = tab.plot.getHistogramWidget().getLevels()
            tab.curImage.savedGradient = tab.gradient_isocurve.saveState()
            if tab.plot.axes.get('t', None) is not None:
                tab.curImage.time = tab.plot.timeLine.value()

            self.plotToPaste = tab.curImage

    def paste_plot(self):
        if self.plotToPaste is None:
            return
        tab = self.tabWidget.currentWidget()
        tab.paste_plot(self.plotToPaste)

        if self.plotWasCut:
            self.plotWasCut = False
            self.plotToPaste.delete()

    def cut_plot(self):
        self.copy_plot()
        self.plotWasCut = True

    def zoom_to(self):
        tab = self.tabWidget.currentWidget()
        tab.zoom_to_current()


    def closeTab(self, index):
        tab = self.tabWidget.widget(index)

        if self.tabWidget.currentIndex() == index:
            nextIndex = index + 1
            if index == self.tabWidget.count() - 1:
                nextIndex = index - 1
            self.tabWidget.setCurrentIndex(nextIndex)

        if isinstance(tab, TraceTab):
            if len(self.traceTabs) == 1 and len(self.imageTabs) == 0:
                raise GraphException("Cannot close the last tab.")
            tab.deleteTab()
            self.tabWidget.removeTab(index)
            self.traceTabs.pop(tab.name)

        if isinstance(tab, ImageTab):
            if len(self.imageTabs) == 1 and len(self.traceTabs) == 0:
                raise GraphException("Cannot close the last tab.")
            tab.deleteTab()
            self.tabWidget.removeTab(index)
            self.imageTabs.pop(tab.name)

    def newTab(self, index):
        if index == 0:
            self.addTraceTab()
        if index == 1:
            self.addImageTab()

    def addTraceTab(self):
        tab = TraceTab(self)
        for ds in self.dataStreams.itervalues():
            ds.addToTab(tab)
            tab.addDataSource(ds)

        tab.setName(uniqueName("Trace Tab {}", 0, self.traceTabs.keys()))
        self.tabWidget.addTab(tab, tab.name)
        self.traceTabs[tab.name] = tab
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def addImageTab(self):
        tab = ImageTab(self)
        for ds in self.dataStreams.itervalues():
            ds.addToTab(tab)
            tab.addDataSource(ds)

        tab.setName(uniqueName("Image Tab {}", 0, self.imageTabs.keys()))
        self.tabWidget.addTab(tab, tab.name)
        self.imageTabs[tab.name] = tab
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    def loadFile(self):
        if self.first == True:
            self.first = False
            filePaths = ['graph/data/vidTest2.hdf5']
        else:
            filePaths = getFilePath()
            if filePaths is None:
                return

        filePaths = [str(path) for path in filePaths]
        nonHDF5 = []

        for path in filePaths:
            if path[-5:] == '.hdf5':
                f = h5py.File(path, 'r')
                for dsetName in f:
                    if 'Type' in f[dsetName].attrs:
                        if f[dsetName].attrs['Type'] == 'Dataset':
                            ds = DataStream(path, dsetName)
                            self.addDataSource(ds)
                            self.dataStreams[ds.name] = ds
                f.close()
            else:
                nonHDF5 += [path]

        if len(nonHDF5) > 0:
            nonHDF5 = ', '.join(nonHDF5)
            raise GraphException(
                "Cannot load {}. Not HDF5 files.".format(nonHDF5))

    def addDataSource(self, ds):
        for tab in self.traceTabs.itervalues():
            ds.addToTab(tab)
            tab.addDataSource(ds)

        for tab in self.imageTabs.itervalues():
            ds.addToTab(tab)
            tab.addDataSource(ds)


pqg.setConfigOptions(background='w')
# pqg.setConfigOptions(foreground='b')
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
