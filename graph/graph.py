import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pqg
import numpy as np
from datastream import DataStream, SliceTreeItem
from graph_ui import Ui_MainWindow
from tracetab import TraceTab
from graphexception import GraphException
from traceitem import TraceItem
from imageitem import ImageItem
from utils import *


class MyWindowClass(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.file_open.triggered.connect(self.loadFile)
        self.traceTabs = {}
        self.imageTabs = {}
        self.dataStreams = {}
        self.dataSources = {}        

        self.comboNewTab = QtGui.QComboBox()
        self.comboNewTab.addItems(["Trace Tab", "Image Tab"]) 
        self.comboNewTab.activated.connect(self.newTab)
        self.tabWidget.setCornerWidget(self.comboNewTab)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        self.addTraceTab()

    def closeTab(self, index):
        tab = self.tabWidget.widget(index)
        if isinstance(tab, TraceTab):
            if len(self.traceTabs) == 1:
                raise GraphException("Cannot close the last trace tab.")
            self.traceTabs.pop(tab.name)
        # if isinstance(tab, ImageTab):
        #     ...
        tab.deleteTab()
        self.tabWidget.removeTab(index)

    def newTab(self, index):
        if index == 0:
            self.addTraceTab()
        if index == 1:
            self.addImageTab()

    def addTraceTab(self):
        # layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, parent)
        tab = TraceTab(self)
        for ds in self.dataStreams.itervalues():
            ds.addToTraceTab(tab)
            tab.addDataSource(ds)

        tab.setName(uniqueName("Trace Tab {}", 0, self.traceTabs.keys()))
        self.tabWidget.addTab(tab, tab.name)
        self.traceTabs[tab.name] = tab

    def addImageTab(self):
        print('adding image tab.')

    def addImage(self, image):
        """Add a new image to the list of currently selectable images."""
        self.curImage = image
        self.comboBox_selectImage.addItem(image.name)
        curIndex = len(self.images) - 1
        self.comboBox_selectImage.setCurrentIndex(curIndex)
        self.syncButtons()

    def loadFile(self):
        filePaths = getFilePath()
        if filePaths is None:
            return

        for path in filePaths:
            ds = DataStream(str(path))
            self.addDataSource(ds)
            self.dataStreams[ds.name] = ds

    def addDataSource(self, ds):
        for tab in self.traceTabs.itervalues():
            ds.addToTraceTab(tab)
            tab.addDataSource(ds)

        # for tab in self.imageTabs.itervalues():
        #     ds.addToTab(tab)

    def removeSources(self, sourcePaths):
        """for for each path in SOURCEPATHS remove path from the combo boxes."""
        for path in sourcePaths:
            for trace in self.traces.itervalues():
                for comboBox in trace.comboBoxes:
                    index = comboBox.findText(path)
                    if index != -1:
                        comboBox.removeItem(index)

            for image in self.images.itervalues():
                for comboBox in image.comboBoxes:
                    index = comboBox.findText(path)
                    if index != -1:
                        comboBox.removeItem(index)

    def updateSources(self, sourcePaths):
        """for for each path in SOURCEPATHS remove path from the combo boxes
        and then re-add it to the appropriate ones."""
        self.removeSources(sourcePaths)
        self.addSources(sourcePaths)

    def sourceNames(self, *dims):
        """Return a list of current data source (args, vals, slices) names
        of dimension DIM."""
        names = []
        for ds, source, tag in self.dataSources.values():
            if ds.getSourceDim(source, tag) in dims:
                name = ds.name + '.'
                name += ds.getSourceName(source, tag)
                names += [name]

        return names

    def treeItemClicked(self, item, column):
        """Handles a click in column COLUMN of item ITEM in SELF.TREE_DATA."""
        return

    def newImage(self):
        image = ImageItem()
        image.setName(uniqueName("Image {}", 0, self.images))
        self.images[image.name] = image
        image.addToTree(self)

    #########################################
    #### Methods Dealing with Plot Table ####
    #########################################

    def setImageData(self, image, dataPath):
        ds, source, tag = self.dataSources[str(dataPath)]

        if ds.getSourceDim(source, tag) not in (2, 3, 4):
            raise GraphException("Can only create images with 2-4D data.")

        image.setData(ds, source, tag)

    def setImageName(self, image, name, lineEdit):
        oldName = image.name
        if name in self.images.keys():
            lineEdit.setText(oldName)
            raise GraphException("Duplicate names not allowed.")
        else:
            self.images.pop(oldName)
            image.setName(name)
            self.images[image.name] = image
            index = self.comboBox_selectImage.findText(oldName)
            self.comboBox_selectImage.setItemText(index, name)

    def toggleUpdate(self, sc):
        raise NotImplementedError()

    def toggleShowImage(self, image, checkBox):
        if checkBox.isChecked():
            self.addImage(image)
        else:
            image.removeFrom(self.image)
            index = self.comboBox_selectPlot.findText(image.name)
            self.comboBox_selectImage.removeItem(index)

    ##########################################
    #### Methods dealing with the plot tab ###
    ##########################################

    def selectCurImage(self):
        """Change the current visible Image to that in the COMBOBOX_SELECTPLOT."""
        name = self.comboBox_selectImage.currentText()
        self.changeToImage(name)

    def changeToImage(self, name):
        name = str(name)
        index = self.comboBox_selectImage.findText(name, QtCore.Qt.MatchExactly)
        if name not in self.images.keys():
            raise GraphException("Cannot find trace {}.".format(name))
        if index < 0:
            raise GraphException("Cannot find trace {} in ComboBox.".format(name))

        img = self.images[name]
        self.image.setImage(img.getData())
        self.comboBox_selectImage.setCurrentIndex(index)


pqg.setConfigOptions(background='w')
# pqg.setConfigOptions(foreground='b')
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
