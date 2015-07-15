import pyqtgraph as pqg


class ImageView(pqg.ImageView):
    def __init__(self, parent=None, name='ImageView', view=None, imageItem=None, *args):
        self.plotItem = pqg.PlotItem()
        self.plotItem.showGrid(True, True, 255)
        super(ImageView, self).__init__(parent, name, self.plotItem, imageItem, *args)

    def getPlotItem(self):
        return self.plotItem

    def getView(self):
        return self.plotItem.getViewBox()

    def getRatio(self):
        """Returns the aspect ratio of my imageItem."""
        xIndex = self.axes.get('x', None)
        yIndex = self.axes.get('y', None)

        if self.image == None:
            return None
        if xIndex == None:
            return None
        if yIndex == None:
            return None
        else:
            return float(self.image.shape[yIndex]) / float(self.image.shape[xIndex])
