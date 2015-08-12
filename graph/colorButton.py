import pyqtgraph as pqg

class ColorButton(pqg.ColorButton):
    def selectColor(self):
        self.origColor = self.color()
        self.colorDialog.setCurrentColor(self.color())
        self.colorDialog.exec_()
