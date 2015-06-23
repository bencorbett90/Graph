import numpy as np
from PyQt4 import QtCore, QtGui
import os
from graphexception import GraphException

class DataStream():
    def __init__(self, path):
        self.dataPath = path
        self.shape = None
        self.numArgs = 0
        self.numVals = 0
        self.name = None
        self.argNames = []
        self.valNames = []
        self.slices = {}

        self.getInfo()
        

    def LoadArgs(self):
        """Return a list of 1D numpy ndarrays compromising my arguments or independ variables"""
        raise NotImplementedError()

    def loadArrayMap(self):
        """Return a list of my maps, from dependent to independ variables."""
        raise NotImplementedError()

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
        args = self.LoadArgs()
        funcMap = self.loadArrayMap()
        self.numArgs = len(args)
        self.shape = funcMap.shape
        self.numVals = self.shape[-1]
        self.argNames = [None] * self.numArgs
        self.valNames = [None] * self.numVals

    def slice(self, sliceStr):
        """Return a slice through my map specified by PARAMS.
        PARAMS is a list of pairs specifying the slicing indices for each
        dimension."""
        evalStr = "self.loadArrayMap()[" + sliceStr + ']'
        return eval(evalStr)



    def addToTree(self, tree, nameDict):
        """Add SELF to QTreeWidget TREE, with a name that is not in 
        NAMEDICT."""
        if self.name != None and self.name not in nameDict.keys():
            name = self.name
        else:
            if self.name != None and self.name in nameDict.keys():
                print("A DataStream with name {} already exists. Generating a default name.".format(self.name))
            name = uniqueName("DataStream {}", len(nameDict), nameDict.keys())

        parentTW = QtGui.QTreeWidgetItem([name])

        # taking care of my arguments
        argParentTW = QtGui.QTreeWidgetItem(['Independent Variables'])
        for arg in range(self.numArgs):
            if self.argNames[arg] == None:
                self.argNames[arg] = uniqueName('arg {}', 0, self.argNames)
            argTW = QtGui.QTreeWidgetItem([self.argNames[arg], self.shape[arg]])
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
            valTW = QtGui.QTreeWidgetItem([self.valNames[val], self.shape[0:-1])
            #
            # If want to allow val name edditing, impliment here.
            #
            valParentTW.addChild(valTW)
        parentTW.addChild(valParentTW)

        # taking care of slices







    
class SliceTreeItem(QtGui.QTreeWidgetItem):
   """Represents a Slice in a QTreeWidgetItem"""

    def __init__(self, parent, name, dataStream): 
        super(SliceTreeItem, self).__init__(parent)
        self.name = name
        self.ds = dataStream
        self.sliceStr = None

        self.setText(0, name)
        self.initChildren()

    def initChildren(self):
        for arg in range(self.ds.numArgs):
            argName = self.ds.argNames[arg]
            argTW = QtGui.QTreeWidgetItem([argName])
            lineEdit = QtGui.QLineEdit()
            lineEdit.editingFinished.connect(self.updateSlice)
            self.treeWidget().setItemWidget(self, 2, lineEdit)
            self.addChild(argTW)

        for val in range(self.ds.numVals):
            valName = self.ds.valNames[val]
            valTW = QtGui.QTreeWidgetItem([valName])
            lineEdit = QtGui.QLineEdit()
            lineEdit.editingFinished.connect(self.updateSlice)
            self.treeWidget().setItemWidget(self, 2, lineEdit)
            self.addChild(valTW)

    def updateSlice(self):


    def getSlice(self):
        return self.ds.slice(self.sliceStr)

    




class DataTxtFile(DataStream):
    def __init__(self, path):
        """Set the parent GUI element of the datastream. Set the path of the .txt file,
        and load the data it contains."""
        self.path = path
        self.name = shorten_filename(path)
        self.shape = (0, 0)
        self.data = np.zeros(self.shape)
        self.loadData()
        self.dimNames = ["Dimension {}".format(i) for i in range(self.shape[1])]

    def getData(self):
        return self.data

    def dimensions(self):
        return self.shape[1]

    def getDimension(self, dim):
        condition = [True if i == dim else False for i in range(len(self.data))]
        if dim > self.shape[1]:
            return np.zeros(0)
        return np.compress(condition, self.data, 1).flatten()

    def getName(self):
        """Return the name of the data file."""
        return self.name

    def setName(self, newName):
        """Set the name of the data file."""
        self.name = newName

    def dimName(self, dim):
        return self.dimNames[dim]

    def setDimName(self, dim, newName):
        self.dimNames[dim] = newName

    def loadData(self):
        try:
            data = open(self.path, 'r')
        except IOError:
            print("The requested file doesn't exist: " + self.path)
            self.destroy()
            return
    
        points = []
        lineNum = 1

        for line in data:
            items = line.split()
            if lineNum == 1:
                numDim = len(items)
            if len(items) != numDim:
                print("Length error at line: " + str(lineNum))
                self.destroy()
                return
            else:
                try:
                    point = []
                    for value in items:
                        point += [float(value)]
                    points += [point]
                except ValueError:
                    print("Error coercing value to float at line: " + str(lineNum))
                    self.destroy()
                    return
            lineNum += 1

        self.data = np.array(points)
        self.shape = self.data.shape

    def indexedArray(self, *args):
        """Return an array of my data indexed by dimensions in *args."""
        indexDims = *args
        dataDims = []
        for i in range(self.dimensions())
            if i not in indexDims:
                dataDims += [i]

        dataShape = []
        dataArray = np.zeros()
        for point in self.data()



    def destroy(self):
        raise NotImplementedError()


def shorten_filename(filename):
    f = os.path.split(filename)[1]
    return "%s~%s" % (f[:3], f[-16:]) if len(f) > 19 else f

def uniqueName(baseName, baseNum, nameList):
    """Return a new name formed from BASENAME.format(BASENUM) that is not
    in nameList."""
    name = baseName.format(baseNum)
    while name in nameDict.keys():
        baseNum += 1
        name = baseName.format(baseNum)
    return name