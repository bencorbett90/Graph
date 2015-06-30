from PyQt4 import QtGui
from graphexception import GraphException


class ImageItem():
    def __init__(self):
        self.name = None
        self.comboBoxes = ()
        self.data = None

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

    def addToTree(self, Graph):
        """Add my ImageItem to GRAPH.TREE_IMAGE."""

        tree = Graph.tree_image
        updateName = Graph.setImageName
        toggleShow = Graph.toggleShowImage
        updateData = Graph.setImageData
        comboNames = Graph.sourceNames(2, 3, 4)

        parentTWI = QtGui.QTreeWidgetItem()
        tree.addTopLevelItem(parentTWI)

        nameBox = QtGui.QLineEdit(self.name)
        f = lambda name: updateName(self, name, nameBox)
        nameBox.textEdited.connect(f)
        tree.setItemWidget(parentTWI, 0, nameBox)

        checkBoxShow = QtGui.QCheckBox("Show")
        show = lambda: toggleShow(self, checkBoxShow)
        checkBoxShow.stateChanged.connect(show)
        checkBoxShow.setChecked(True)
        tree.setItemWidget(parentTWI, 1, checkBoxShow)

        childData = QtGui.QTreeWidgetItem(['Data'])
        parentTWI.addChild(childData)
        comboData = QtGui.QComboBox()
        comboData.addItems(comboNames)

        curText = comboData.currentText
        loadData = lambda name: updateData(self, curText())
        comboData.activated.connect(loadData)
        self.comboBoxes = (comboData, )

        tree.setItemWidget(childData, 1, comboData)
