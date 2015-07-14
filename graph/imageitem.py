from PyQt4 import QtGui
from graphexception import GraphException


class ImageItem():
    def __init__(self, imageTab):
        self.imageTab = imageTab
        self.name = None
        self.dataFunc = None

    def addTo(self, plotItem):
        """Add SELF to PLOTITEM."""
        plotItem.addItem(self)

    def removeFrom(self, plotItem):
        """"Remove SELF from PLOTITEM."""
        plotItem.removeItem(self)

    def setName(self, newName):
        self.name = str(newName)

    def setData(self, ds, source, tag):
        if ds.getSourceDim(source, tag) not in (2, 3, 4):
            raise GraphException("Can only create images with 2-4D data.")
        else:
            self.data = (ds, source, tag)

    def getData(self):
        if self.data is not None:
            ds, source, tag = self.data
            return ds.getData(source, tag)
        else:
            raise GraphException("{} has no data to get.".format(self.name))

    def setImageData(self):
        dataString = str(self.dataSelector.currentText())
        self.dataFunc = self.getDataFromName(dataString)

    def getDataFromName(self, Name):
        Name = str(Name)
        name = Name.split('[')
        dataName = name[0].strip()

        if len(name) not in (1, 2):
            raise GraphException("{} is not a valid slice".format(Name))
        elif dataName not in self.ds.argNames:
            if dataName not in self.ds.valNames:
                message = "{} does not contain {}".format(self.ds.name, dataName)
                raise GraphException(message)
        if len(name) == 1:
            return lambda: self.ds.getDataFromName(dataName)
        if len(name) == 2:
            sliceStr = name[1].split(']')
            if len(sliceStr) < 2:
                raise GraphException("{} is not a valid slice".format(Name))
            sliceStr = sliceStr[0].strip()
            return lambda: self.ds.getDataFromName(name[0], sliceStr)

    def setImageName(self, name, lineEdit):
        oldName = self.name
        if name in self.imageTab.images.keys():
            lineEdit.setText(oldName)
            raise GraphException("Duplicate names not allowed.")
        else:
            self.imageTab.images.pop(oldName)
            self.setName(name)
            self.imageTab.images[self.name] = self

    def toggleUpdate(self):
        raise NotImplementedError()

    def toggleShow(self, checkBoxShow):
        self.imageTab.plot.setImage(self.dataFunc())

    def selectDataSource(self, comboBox, index):
        """Change the dataStream from which I pull my data."""
        dsName = str(comboBox.itemText(index))
        self.ds = self.imageTab.dataStreams[dsName]
        i = self.dataSelector.count()
        while i > 0:
            i -= 1
            self.dataSelector.removeItem(i)

        self.dataSelector.addItems(self.ds.valNames)

    def addToTree(self, imageTab):
        """Add my ImageItem to TRACETAB.TREE_IMAGE."""

        tree = imageTab.tree_image
        dataStreamNames = imageTab.dataStreams.keys()

        parentTWI = QtGui.QTreeWidgetItem()
        tree.addTopLevelItem(parentTWI)

        nameBox = QtGui.QLineEdit(self.name)
        f = lambda name: self.setImageName(name, nameBox)
        nameBox.textEdited.connect(f)
        tree.setItemWidget(parentTWI, 0, nameBox)

        checkBoxShow = QtGui.QCheckBox("Show")
        show = lambda: self.toggleShow(checkBoxShow)
        checkBoxShow.stateChanged.connect(show)
        checkBoxShow.setChecked(True)
        tree.setItemWidget(parentTWI, 1, checkBoxShow)

        # Adding the data parent item and update check box
        dataParent = QtGui.QTreeWidgetItem(['Data'])
        parentTWI.addChild(dataParent)
        checkBoxUpdate = QtGui.QCheckBox("Update")
        checkBoxUpdate.stateChanged.connect(self.toggleUpdate)
        checkBoxUpdate.setChecked(False)
        tree.setItemWidget(dataParent, 1, checkBoxUpdate)

        # Adding the sourceSelector
        childSource = QtGui.QTreeWidgetItem(['Source'])
        dataParent.addChild(childSource)
        comboSource = QtGui.QComboBox()
        comboSource.addItems(dataStreamNames)
        comboSource.setEditable(True)
        selectSource = lambda index: self.selectDataSource(comboSource, index)
        comboSource.activated.connect(selectSource)
        tree.setItemWidget(childSource, 1, comboSource)
        self.sourceSelector = comboSource

        # Adding xData selector
        childData = QtGui.QTreeWidgetItem(['Data'])
        dataParent.addChild(childData)
        comboData = QtGui.QComboBox()
        comboData.setEditable(True)
        comboData.activated.connect(self.setImageData)
        tree.setItemWidget(childData, 1, comboData)
        self.dataSelector = comboData