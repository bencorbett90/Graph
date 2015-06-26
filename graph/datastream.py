import numpy as np
from PyQt4 import QtCore, QtGui
import os
from graphexception import GraphException
import h5py

class DataStream():
    def __init__(self, path):
        self.dataFile = None
        if path[-5:] == '.hdf5':
            self.dataFile = HDF5File(path)
        self.shape = None
        self.numArgs = 0
        self.numVals = 0
        self.name = path
        
        # Lists of arg and val names
        self.argNames = []
        self.valNames = []
        
        # Dictionary from ints to SliceTreeItems
        self.slices = {}
        
        self.getInfo()

    def getSourceDim(self, source, tag):
        """Source specifies one of ARG, VAL, or SLICE, and tag specifies
        the number or string specifying the arg, val, or slice."""
        if source == 'ARG':
            return 1
        if source == 'VAL':
            if self.numVals == 1:
                return len(self.shape)
            else:
                return len(self.shape) - 1
        if source == 'SLICE':
            return self.slices[tag].dimensions()

    def getSourceName(self, source, tag):
        """Source specifies one of ARG, VAL, or SLICE, and tag specifies
        the number or string specifying the arg, val, or slice."""
        if source == 'ARG':
            return self.argNames[tag]
        if source == 'VAL':
            return self.valNames[tag]
        if source == 'SLICE':
            return tag




    def LoadArgs(self):
        """Return a list of 1D numpy ndarrays compromising my arguments or independ variables"""
        return self.dataFile.loadArgs()

    def loadArrayMap(self):
        """Return a list of my maps, from dependent to independ variables."""
        return self.dataFile.loadArrayMap()

    def getNumArgs(self):
        """Return the number of my arguments or independent variables."""
        return self.numArgs

    def getNumVals(self):
        """Return the number of my values or dependent variables."""
        return self.numVals
    
    def getName(self):
        """Return the name of the data file."""
        return self.name

    def setName(self, newName):
        """Set the name of this DataStream."""
        self.name = newName

    def getInfo(self):
        args = self.dataFile.loadArgs()
        funcMap = self.dataFile.loadArrayMap()
        self.numArgs = len(args)
        self.shape = funcMap.shape
        if self.numArgs == len(self.shape):
            self.numVals = 1
        else:
            self.numVals = self.shape[-1]
        self.argNames = [None] * self.numArgs
        self.valNames = [None] * self.numVals

    def slice(self, sliceStr):
        """Return a slice through my map specified by PARAMS.
        PARAMS is a list of pairs specifying the slicing indices for each
        dimension."""
        return self.dataFile.slice(sliceStr)

    def addToTree(self, Graph):
        """Add SELF to QTreeWidget GRAPH.TREE_DATA"""
        tree = Graph.tree_data
        nameDict = Graph.dataStreams
        newSlice = Graph.createNewSlice

        if self.name != None and self.name in nameDict.keys():
            baseName = self.name + '({})'
            self.name = uniqueName(baseName, 1, nameDict.keys())
        else:
            self.name = uniqueName("DataStream {}", len(nameDict), nameDict.keys())

        parentTW = QtGui.QTreeWidgetItem([self.name])

        # taking care of my arguments
        argParentTW = QtGui.QTreeWidgetItem(['Independent Variables'])
        for arg in range(self.numArgs):
            if self.argNames[arg] == None:
                self.argNames[arg] = uniqueName('arg {}', 0, self.argNames)
            argTW = QtGui.QTreeWidgetItem()
            argTW.setText(0, self.argNames[arg])
            argTW.setText(1, str(self.shape[arg]))
            #
            # If want to allow arg name edditing, impliment here.
            #
            argParentTW.addChild(argTW)
        parentTW.addChild(argParentTW)

        # taking care of my values
        valParentTW = QtGui.QTreeWidgetItem(['Dependent Variables'])
        for val in range(self.numVals):
            if self.valNames[val] == None:
                self.valNames[val] = uniqueName('val {}', 0, self.argNames)
            valTW = QtGui.QTreeWidgetItem()
            valTW.setText(0, self.valNames[val])
            valTW.setText(1, str(self.shape))
            #
            # If want to allow val name edditing, impliment here.
            #
            valParentTW.addChild(valTW)
        parentTW.addChild(valParentTW)

        # taking care of slices
        self.sliceParentTW = QtGui.QTreeWidgetItem(['Slices'])
        sliceBtnTW = QtGui.QTreeWidgetItem()
        sliceBtnTW.btn = True
        sliceBtnTW.ds = self
        sliceBtn = QtGui.QPushButton('New Slice')
        f = lambda : newSlice(self)
        sliceBtn.clicked.connect(f)
        self.sliceParentTW.addChild(sliceBtnTW)
        parentTW.addChild(self.sliceParentTW)
        
        tree.addTopLevelItem(parentTW)
        tree.setItemWidget(sliceBtnTW, 0, sliceBtn)


class HDF5File():
    def __init__(self, path):
        self.dataPath = path

    def loadArgs(self):
        f = h5py.File(self.dataPath, 'r')
        args = []
        for name in f['args']:
            path = 'args/' + name
            args += [f[path][:]]
        f.close()
        return args

    def loadArrayMap(self):
        f = h5py.File(self.dataPath, 'r')
        arrayMap = f['vals'][..., :]
        f.close()
        return arrayMap

    def slice(self, sliceStr):
        f = h5py.File(self.dataPath, 'r')
        dataMap = f['calib/vals/twpa thru']
        evalStr = "dataMap[" + sliceStr + ']'
        dataSlice = eval(evalStr)
        f.close()
        return dataSlice


    
class SliceTreeItem(QtGui.QTreeWidgetItem, object):
    """Represents a Slice in a QTreeWidgetItem"""

    def __init__(self, name, parent, dataStream, update): 
        super(SliceTreeItem, self).__init__(parent)
        self.name = name
        self.ds = dataStream
        self.shape = None
        self.limits = []
        for i in range(self.ds.numArgs):
            self.limits += [self.ds.shape[i]]
        self.limits += [self.ds.numVals]
        self.slice = [[0, i] for i in self.limits]

        self.initChildren(update)
        self.setText(0, name)
        self.setText(1, self.getSliceStr())
        
    def initChildren(self, update):
        updateSlice = lambda : update(self)
        for arg in range(self.ds.numArgs):
            argName = self.ds.argNames[arg]
            argTW = QtGui.QTreeWidgetItem([argName])
            lineEdit = QtGui.QLineEdit()
            lineEdit.setText(' : ')

            lineEdit.editingFinished.connect(updateSlice)
            self.addChild(argTW)
            self.treeWidget().setItemWidget(argTW, 1, lineEdit)

        valTW = QtGui.QTreeWidgetItem(['vals'])
        lineEdit = QtGui.QLineEdit()
        lineEdit.setText(' : ')
        lineEdit.index = self.ds.numArgs
        lineEdit.editingFinished.connect(updateSlice)
        self.addChild(valTW)
        self.treeWidget().setItemWidget(valTW, 1, lineEdit)

        sliceBtnTW = QtGui.QTreeWidgetItem()
        sliceBtn = QtGui.QPushButton('Print Slice')
        sliceBtn.clicked.connect(self.printSlice)
        self.addChild(sliceBtnTW)
        self.treeWidget().setItemWidget(sliceBtnTW, 0, sliceBtn)

    def printSlice(self):
        print(self.slice)

    def getSliceStr(self):
        """Get a string representing my slice."""
        sliceStr = ''
        for item in self.slice:
            if len(item) == 1:
                sliceStr += '{}, '.format(item[0])
            elif len(item) == 2:
                sliceStr += '{} : {}, '.format(item[0], item[1])
        sliceStr = sliceStr[0:-2]
        return sliceStr

    def getSlice(self):
        """Return the actual ndarray that I represent."""
        sliceStr = self.getSliceStr()
        return ds.slice(sliceStr)

    def dimensions(self):
        """Return the number of indices needed to index into myself to get a scalar."""
        dim = 0
        for item in self.slice:
            if len(item) != 1:
                dim += 1

def uniqueName(baseName, baseNum, nameList):
    """Return a new name formed from BASENAME.format(BASENUM) that is not
    in nameList."""
    name = baseName.format(baseNum)
    while name in nameList:
        baseNum += 1
        name = baseName.format(baseNum)
    return name