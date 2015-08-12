from PyQt4 import QtGui, QtCore
from imagetab_ui import Ui_Form
import pyqtgraph as pqg
from imageitem import ImageItem
from traceitem import TraceItem
from utils import *
from colorButton import ColorButton

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
        self.name = None
        self.curImage = None

        # unlock the aspect ratio and uninvert the y axis.
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
        self.spin_t.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_lvl_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_lvl_max.setOpts(step=.1, dec=True, minStep=.1)
        self.plot.getView().sigRangeChanged.connect(self.updateRangeBoxes)
        self.spin_x_min.sigValueChanged.connect(self.setRange)
        self.spin_x_max.sigValueChanged.connect(self.setRange)
        self.spin_y_min.sigValueChanged.connect(self.setRange)
        self.spin_y_max.sigValueChanged.connect(self.setRange)
        self.updateRangeBoxes()
        self.spin_t.sigValueChanged.connect(self.setTime)
        self.plot.playTimer.timeout.connect(self.updateTime)
        self.plot.sigTimeChanged.connect(self.updateTime)
        self.spin_lvl_min.sigValueChanging.connect(self.setLevels)
        self.spin_lvl_max.sigValueChanging.connect(self.setLevels)
        self.plot.getHistogramWidget().sigLevelsChanged.connect(self.updateLevels)

        # Setting background color
        self.plot.getView().setBackgroundColor(self.backgroundColor)

        # Connecting the check boxes.
        self.checkBox_showGrid.setChecked(True)
        self.checkBox_showGrid.clicked.connect(self.showGrid)
        self.checkBox_lockRatio.clicked.connect(self.lockRatio)

        # Connecting the color buttons
        self.btnColor_background.sigColorChanging.connect(self.setBackgroundColor)
        self.btnColor_grid.sigColorChanging.connect(self.setGridColor)

        # Initializing the color buttons
        self.btnColor_background.setColor(self.backgroundColor)
        self.btnColor_grid.setColor(self.gridColor)

        # Connecting the Create New Trace button
        self.btn_newImage.clicked.connect(self.newImage)

        # Connecting the Create New Isocurve button
        self.btn_new_isocurve.clicked.connect(self.new_isocurve)
        self.gradient_isocurve.sigGradientChanged.connect(self.update_iso_gradient)
        self.spin_width.sigValueChanging.connect(self.update_iso_width)
        self.plot.imageItem.sigImageChanged.connect(self.update_iso_data)
        self.checkBox_isocurve.setChecked(True)
        self.checkBox_isocurve.clicked.connect(self.show_isocurve)

        self.btn_autoLvl.clicked.connect(self.autoLvl)
        self.btn_autoRange.clicked.connect(self.autoRange)

        # connecting data selectors
        self.combo_select_source.activated.connect(self.select_source)
        self.combo_select_val.activated.connect(self.select_val)
        self.combo_x.activated.connect(self.select_data)
        self.combo_y.activated.connect(self.select_data)
        self.combo_t.activated.connect(self.select_data)
        self.combo_c.activated.connect(self.select_data)

        # connecting table clicks, and setting no selection.
        self.table_images.cellClicked.connect(self.cell_clicked)
        self.table_images.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

        # Connecting slice buttons
        self.checkBox_x_slice.clicked.connect(self.show_x_slice)
        self.checkBox_y_slice.clicked.connect(self.show_y_slice)
        self.checkBox_x_slice.setChecked(False)
        self.checkBox_y_slice.setChecked(False)
        self.show_x_slice()
        self.show_y_slice()

        # reset the gradient for color plots.
        self.plot.getHistogramWidget().gradient.sigGradientChanged.connect(self.gradient_changed)
        self.changeGradient = True

        self.tree_data.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_data.customContextMenuRequested.connect(self.ds_menu)

        self.table_images.itemChanged.connect(self.item_changed)

    def zoom_to_current(self):
        self.autoRange()

    def paste_plot(self, plot):
        if isinstance(plot, ImageItem):
            self.newImage()
            self.curImage.setName(plot.name)
            self.curImage.copy_data(plot)

            self.sync_buttons()
            
            image = self.curImage
            self.curImage = None
            self.change_to_image(image)

        elif isinstance(plot, TraceItem):
            self.newImage()
            self.curImage.setName(plot.name())
            self.curImage.copy_data(plot)

            self.sync_buttons()
            
            image = self.curImage
            self.curImage = None
            self.change_to_image(image)

    def item_changed(self, item):
        col = item.column()
        if col == 0:
            item.image.setName(item.text())

    def addDataSource(self, ds):
        self.combo_select_source.addItem(ds.name)

    def autoLvl(self):
        self.plot.autoLevels()

    def autoRange(self):
        self.plot.autoRange()

    def setName(self, newName):
        self.name = str(newName)

    def setTime(self):
        self.plot.timeLine.blockSignals(True)

        timeTo = self.spin_t.value()
        self.plot.timeLine.setValue(timeTo)
        self.plot.timeLineChanged()

        self.plot.timeLine.blockSignals(False)

    def updateTime(self, index=None, time=None):
        self.spin_t.blockSignals(True)

        curTime = self.plot.timeLine.value()
        self.spin_t.setValue(curTime)

        self.spin_t.blockSignals(False)

    def setLevels(self):
        self.plot.blockSignals(True)
        minLvl = self.spin_lvl_min.value()
        maxLvl = self.spin_lvl_max.value()
        self.plot.setLevels(minLvl, maxLvl)
        self.plot.blockSignals(False)

    def updateLevels(self):
        self.spin_lvl_min.blockSignals(True)
        self.spin_lvl_max.blockSignals(True)

        minLvl, maxLvl = self.plot.getHistogramWidget().getLevels()
        self.spin_lvl_min.setValue(minLvl)
        self.spin_lvl_max.setValue(maxLvl)

        self.spin_lvl_min.blockSignals(False)
        self.spin_lvl_max.blockSignals(False)

    def updateRangeBoxes(self):
        """ Sets the values of the spin boxes to the current viewable range."""
        self.spin_x_min.blockSignals(True)
        self.spin_x_max.blockSignals(True)
        self.spin_y_min.blockSignals(True)
        self.spin_y_max.blockSignals(True)

        ((x_min, x_max), (y_min, y_max)) = self.plot.getView().viewRange()
        self.spin_x_min.setValue(float(x_min))
        self.spin_x_max.setValue(float(x_max))
        self.spin_y_min.setValue(float(y_min))
        self.spin_y_max.setValue(float(y_max))

        self.spin_x_min.blockSignals(False)
        self.spin_x_max.blockSignals(False)
        self.spin_y_min.blockSignals(False)
        self.spin_y_max.blockSignals(False)

    def setRange(self):
        self.plot.getView().blockSignals(True)

        x_min = self.spin_x_min.value()
        x_max = self.spin_x_max.value()
        y_min = self.spin_y_min.value()
        y_max = self.spin_y_max.value()
        self.plot.getView().setRange(xRange=(x_min, x_max), yRange=(y_min, y_max), padding=False)
        
        self.plot.getView().blockSignals(False)

    def showGrid(self):
        """ Toggles the grid on or off. """
        if self.checkBox_showGrid.isChecked():
            self.plot.getPlotItem().getAxis('left').setGrid(255)
            self.plot.getPlotItem().getAxis('bottom').setGrid(255)
        else:
            self.plot.getPlotItem().getAxis('left').setGrid(False)
            self.plot.getPlotItem().getAxis('bottom').setGrid(False)

    def lockRatio(self):
        """ Lock the aspect ratio of my view box to be that of my Image."""
        if self.checkBox_lockRatio.isChecked():
            self.plot.getView().setAspectLocked(True, 1.0)
        else:
            self.plot.getView().setAspectLocked(False)

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
        image.name = uniqueName("Image {}", 0, self.images)
        self.images[image.name] = image
        image.add_to_image_table(self.table_images)
        self.change_to_image(image)

    def select_source(self):
        """Change the dataStream that COMBO_SELECT_VAL pulls from
        and clear x,y,t,c combo."""
        dsName = str(self.combo_select_source.currentText())
        ds = self.dataStreams[dsName]
        self.combo_select_val.clear()
        self.combo_x.clear()
        self.combo_y.clear()
        self.combo_t.clear()
        self.combo_c.clear()
        self.combo_select_val.addItems(ds.get_vals(2))

    def select_val(self):
        """Clear and then add the args to the selected val, to the x, y, t, c
        selectors."""
        self.combo_x.blockSignals(True)
        self.combo_y.blockSignals(True)
        self.combo_t.blockSignals(True)
        self.combo_c.blockSignals(True)

        valName = str(self.combo_select_val.currentText())
        dsName = str(self.combo_select_source.currentText())
        ds = self.dataStreams[dsName]
        self.combo_x.clear()
        self.combo_y.clear()
        self.combo_t.clear()
        self.combo_t.addItem('None')
        self.combo_c.clear()
        self.combo_c.addItem('None')
        self.combo_x.addItems(ds.get_args_to_val(valName))
        self.combo_y.addItems(ds.get_args_to_val(valName))
        self.combo_t.addItems(ds.get_args_to_val(valName))
        self.combo_c.addItems(ds.get_args_to_val(valName))
        
        self.combo_x.blockSignals(False)
        self.combo_y.blockSignals(False)
        self.combo_t.blockSignals(False)
        self.combo_c.blockSignals(False)

        self.curImage.set_data_source(ds, valName)
        self.curImage.update_slice_table(self.table_slice)
        self.sync_buttons()

    def sync_buttons(self):
        self.combo_x.blockSignals(True)
        self.combo_y.blockSignals(True)
        self.combo_t.blockSignals(True)
        self.combo_c.blockSignals(True)
        self.combo_select_source.blockSignals(True)
        self.combo_select_val.blockSignals(True)
        self.checkBox_isocurve.blockSignals(True)

        self.combo_x.clear()
        self.combo_y.clear()
        self.combo_t.clear()
        self.combo_c.clear()
        self.combo_select_val.clear()
        self.combo_select_source.clear()
        self.combo_select_source.addItems(self.dataStreams.keys())

        if self.curImage.ds is not None:
            dsName = self.curImage.ds.name
            index = self.combo_select_source.findText(dsName)
            self.combo_select_source.setCurrentIndex(index)
            self.combo_select_val.addItems(self.curImage.ds.get_vals(2))
            self.combo_select_val.setCurrentIndex(-1)

            if self.curImage.valName is not None:
                valName = self.curImage.valName
                index = self.combo_select_val.findText(valName)
                self.combo_select_val.setCurrentIndex(index)

                argNames = self.curImage.ds.get_args_to_val(valName)
                self.combo_x.addItems(argNames)
                self.combo_y.addItems(argNames)
                self.combo_t.addItem('None')
                self.combo_c.addItem('None')
                self.combo_t.addItems(argNames)
                self.combo_c.addItems(argNames)

                xName = self.curImage.axisNames['x']
                xIndex = self.combo_x.findText(xName)
                self.combo_x.setCurrentIndex(xIndex)

                yName = self.curImage.axisNames['y']
                yIndex = self.combo_y.findText(yName)
                self.combo_y.setCurrentIndex(yIndex)

                tName = self.curImage.axisNames['t']
                tIndex = self.combo_t.findText(tName)
                self.combo_t.setCurrentIndex(tIndex)

                cName = self.curImage.axisNames['c']
                cIndex = self.combo_c.findText(cName)
                self.combo_c.setCurrentIndex(cIndex)

        self.checkBox_isocurve.setChecked(self.curImage.displayIso)

        self.combo_x.blockSignals(False)
        self.combo_y.blockSignals(False)
        self.combo_t.blockSignals(False)
        self.combo_c.blockSignals(False)
        self.combo_select_source.blockSignals(False)
        self.combo_select_val.blockSignals(False)
        self.checkBox_isocurve.blockSignals(False)

    def ds_menu(self, pos):
        item = self.tree_data.itemAt(pos)
        if item is None:
            return
        try:
            if item.isClickable:
                pass
        except AttributeError:
            return

        if item.dataType == 'val':
            ds = item.ds
            valName = str(item.text(0))
            extra = ""
            args = ds.get_args_to_val(valName)
            if len(args) < 2:
                raise GraphException("Not enough dimensions to create an image.")
            xAxis = args[0]
            yAxis = args[1]
        if item.dataType == 'arg':
            ds = item.ds
            valName = item.valName
            argName = str(item.text(0))
            extra = " vs " + argName
            args = ds.get_args_to_val(valName)
            if len(args) < 2:
                raise GraphException("Not enough dimensions to create an image.")
            xAxis = argName
            yAxis = args[(args.index(xAxis) + 1) % len(args)]

        globalPos = self.tree_data.mapToGlobal(pos)
        myMenu = QtGui.QMenu()
        myMenu.addAction("plot " + valName + extra)
        selectedItem = myMenu.exec_(globalPos)
        if selectedItem is None:
            return
        if str(selectedItem.text()) == "plot " + valName + extra:
            self.newImage()
            self.curImage.ds = ds
            self.curImage.valName = valName
            self.curImage.set_axis(xAxis, yAxis)
            self.sync_buttons()

    def select_data(self):
        xArg = str(self.combo_x.currentText())
        yArg = str(self.combo_y.currentText())
        tArg = str(self.combo_t.currentText())
        cArg = str(self.combo_c.currentText())
        
        self.curImage.set_axis(xArg, yArg, tArg, cArg)

    def cell_clicked(self, row, column):
        if column != 0:
            return

        item = self.table_images.item(row, 0)
        imageName = str(item.text())
        image = self.images.get(imageName, None)
        if image is None:
            raise GraphException("Not in known images")
        else:
            self.change_to_image(image)

    def change_to_image(self, image):
        """ Set curTrace to TRACE. Update all the buttons/table_slice
        and then highlight the proper row in the table_traces."""
        # Deselecting the previous curTrace
        if self.curImage is not None:
            index = -1
            for row in range(self.table_images.rowCount()):
                item = self.table_images.item(row, 0)
                if str(item.text()) == self.curImage.name:
                    index = row
            if index != -1: 
                item = self.table_images.item(index, 0)
                item.setBackground(pqg.mkBrush((255, 255, 255, 255)))

        # Selecting the current trace
        index = -1
        for row in range(self.table_images.rowCount()):
            item = self.table_images.item(row, 0)
            if str(item.text()) == image.name:
                index = row
        if index != -1:
            item = self.table_images.item(index, 0)
            item.setBackground(pqg.mkBrush((0, 255, 127, 100)))

        if self.curImage is not None:
            self.curImage.gradient = self.plot.getHistogramWidget().gradient.saveState()
            self.curImage.levels = self.plot.getHistogramWidget().getLevels()
            if self.plot.axes.get('t', None) is not None:
                self.curImage.time = self.plot.timeLine.value()

            self.curImage.savedGradient = self.gradient_isocurve.saveState()
            self.curImage.remove_isocurves()

        self.curImage = image
        image.update_slice_table(self.table_slice)
        self.sync_buttons()

        if image.gradient is not None:
            self.plot.getHistogramWidget().gradient.restoreState(image.gradient)

        if image.valName is not None:
            image.display_image()
        else:
            self.plot.clear()

        if image.levels is not None:
            self.plot.setLevels(*image.levels)
        if image.time is not None and self.plot.axes['t'] is not None:
            self.plot.timeLine.setValue(image.time)
            self.plot.timeLineChanged()

        if image.savedGradient is not None:
            self.gradient_isocurve.restoreState(image.savedGradient)
        self.table_isocurve.setRowCount(0)
        image.init_isocurves()

    def new_isocurve(self):
        """Create a new isocurve and add it to the table."""
        if self.curImage is None:
            return

        self.curImage.new_isocurve(self.table_isocurve)

    def update_iso_gradient(self):
        if self.curImage is not None:
            self.curImage.update_iso_colors()

    def update_iso_width(self):
        if self.curImage is not None:
            self.curImage.update_iso_widths()

    def update_iso_data(self):
        if self.curImage is not None:
            self.curImage.update_iso_data()

    def show_isocurve(self):
        if self.curImage is None:
            return
        if self.checkBox_isocurve.isChecked():
            self.curImage.display_isocurves()
            self.curImage.displayIso = True
        else:
            self.curImage.remove_isocurves()
            self.curImage.displayIso = False

    def show_x_slice(self):
        if self.checkBox_x_slice.isChecked():
            self.plot.ui.plot_slice_horiz.show()
            sizes = self.plot.ui.splitter_slice_horiz.sizes()
            total = sum(sizes)
            self.plot.ui.splitter_slice_horiz.setSizes([3*total/4, total/4])
            self.plot.enable_x_slice(True)

        else:
            self.plot.ui.plot_slice_horiz.hide()
            sizes = self.plot.ui.splitter_slice_horiz.sizes()
            total = sum(sizes)
            self.plot.ui.splitter_slice_horiz.setSizes([total, 0])
            self.plot.enable_x_slice(False)

    def show_y_slice(self):
        if self.checkBox_y_slice.isChecked():
            self.plot.ui.plot_slice_vert.show()
            sizes = self.plot.ui.splitter_slice_vert.sizes()
            total = sum(sizes)
            self.plot.ui.splitter_slice_vert.setSizes([4*total/5, total/5])
            self.plot.enable_y_slice(True)
        else:
            self.plot.ui.plot_slice_vert.hide()
            sizes = self.plot.ui.splitter_slice_vert.sizes()
            total = sum(sizes)
            self.plot.ui.splitter_slice_vert.setSizes([total, 0])
            self.plot.enable_y_slice(False)

    def gradient_changed(self):
        """If the current Image is displaying in RGB mode, then the image will not
        display unless the gradient is set to the 'grey' preset. This ensures that the
        gradient stays 'grey' if the current image is in RGB mode."""
        if self.changeGradient is False:
            return

        self.changeGradient = False
        if self.curImage is not None and self.curImage.rgb is True:
            self.plot.getHistogramWidget().gradient.loadPreset('grey')
        self.changeGradient = True

    def delete_image(self, image):
        """Remove IMAGEITEM from self.images, and handle
        if the image is the currently displayed image."""
        # remove the image from self.images
        self.images.pop(image.name)

        # delete the row from self.table_images
        index = -1
        for row in range(self.table_images.rowCount()):
            item = self.table_images.item(row, 0)
            if str(item.text()) == image.name:
                index = row
        if index == -1:
            raise Exception("Cannot find image in table.")

        if self.curImage == image:
            self.table_isocurve.setRowCount(0)
            if len(self.images) == 0:
                self.curImage = None
                self.plot.clear()
            elif index == self.table_images.rowCount()-1:
                name = str(self.table_images.item(index-1, 0).text())
                image = self.images[name]
                self.change_to_image(image)
            elif index < self.table_images.rowCount()-1:
                name = str(self.table_images.item(index+1, 0).text())
                image = self.images[name]
                self.change_to_image(image)

        self.table_images.removeRow(index)

    def deleteTab(self):
        for key, image in self.images.items():
            image.delete()

        del self.images
        del self.graph
        self.plot.close()
        del self.plot
        self.destroy()

    def rename(self, image, newName):
        oldName = image.name
        if newName in self.images.keys():
            return oldName
        else:
            self.images.pop(oldName)
            self.images[newName] = image
            return newName
