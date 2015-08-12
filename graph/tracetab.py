from PyQt4 import QtGui, QtCore
from tracetab_ui import Ui_Form
import pyqtgraph as pqg
from traceitem import TraceItem
from imageitem import ImageItem
from utils import *
from colorButton import ColorButton


class TraceTab(QtGui.QWidget, Ui_Form):

    """A widget that represents one tab for displaying traces."""

    def __init__(self, Graph):
        """Add SELF to PARENT in GRAPH, which should be a tab page."""
        # Initialize the widget and UI.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

        # Default Fields
        self.graph = Graph
        self.backgroundColor = pqg.mkColor(255, 255, 255, 100)
        self.gridColor = pqg.mkColor(0, 0, 0, 255)
        self.traces = {}
        self.dataStreams = Graph.dataStreams
        self.traceCombos = []
        self.legend = None
        self.name = None
        self.enableSetRange = True
        self.enableUpdateBoxes = True
        self.curTrace = None

        # Add the grid, and get rid of the autoscale button.
        self.plot.getPlotItem().showGrid(True, True, 255)
        self.plot.getPlotItem().hideButtons()

        # Initializing the spin boxes:
        self.spin_x_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_x_max.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_y_min.setOpts(step=.1, dec=True, minStep=.1)
        self.spin_y_max.setOpts(step=.1, dec=True, minStep=.1)
        self.plot.getPlotItem().sigRangeChanged.connect(self.updateRangeBoxes)
        self.spin_x_min.valueChanged.connect(self.setRange)
        self.spin_x_max.valueChanged.connect(self.setRange)
        self.spin_y_min.valueChanged.connect(self.setRange)
        self.spin_y_max.valueChanged.connect(self.setRange)
        self.updateRangeBoxes()

        # Setting background color
        self.plot.getPlotItem().getViewBox().setBackgroundColor(
            self.backgroundColor)

        # Connecting buttons.
        self.btn_autoScaleX.clicked.connect(self.autoScaleX)
        self.btn_autoScaleY.clicked.connect(self.autoScaleY)

        # Connecting the check boxes.
        self.checkBox_showGrid.setChecked(True)
        self.checkBox_showGrid.clicked.connect(self.showGrid)
        self.checkBox_showLegend.clicked.connect(self.showLegend)
        self.checkBox_logX.clicked.connect(self.toggleLogX)
        self.checkBox_logY.clicked.connect(self.toggleLogY)
        self.checkBox_lockRatio.clicked.connect(self.lockRatio)

        # Connecting the color buttons
        self.btnColor_background.sigColorChanging.connect(self.setBackgroundColor)
        self.btnColor_grid.sigColorChanging.connect(self.setGridColor)
        # self.btnColor_background.colorDialog.setParent(self.graph)
        self.btnColor_background.parent44 = self.graph


        # Initializing the color buttons
        self.btnColor_background.setColor(self.backgroundColor)
        self.btnColor_grid.setColor(self.gridColor)

        # Connecting the Create New Trace button
        self.btn_newTrace.clicked.connect(self.newTrace)

        # Connecting trace data selectors
        self.combo_selectSource.activated.connect(self.select_source)
        self.combo_select_val.activated.connect(self.select_val)
        self.combo_select_arg.activated.connect(self.select_arg)

        # Connecting checkboxes
        showPoints = lambda: self.toggle_show_points(self.checkBox_points)
        self.checkBox_points.clicked.connect(showPoints)
        showCurve = lambda: self.toggle_show_curve(self.checkBox_curve)
        self.checkBox_curve.clicked.connect(showCurve)
        showFill = lambda: self.toggle_show_fill(self.checkBox_fill)
        self.checkBox_fill.clicked.connect(showFill)

        self.splitter.setSizes([10000, 1])
        self.table_traces.cellClicked.connect(self.cell_clicked)
        self.table_traces.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.init_appearance()

        self.tree_data.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_data.customContextMenuRequested.connect(self.ds_menu)

        self.table_traces.itemChanged.connect(self.item_changed)

    def zoom_to_current(self):
        """Zoom the viewbox to view the current plot."""
        xMin, xMax = self.curTrace.dataBounds(0)
        yMin, yMax = self.curTrace.dataBounds(1)
        xMin -= (xMax - xMin) / 20.0
        xMax += (xMax - xMin) / 20.0
        yMin -= (yMax - yMin) / 20.0
        yMax += (yMax - yMin) / 20.0
        self.spin_x_min.setValue(xMin)
        self.spin_x_max.setValue(xMax)
        self.spin_y_min.setValue(yMin)
        self.spin_y_max.setValue(yMax)

    def item_changed(self, item):
        col = item.column()
        if col == 0:
            item.trace.setName(item.text())

    def paste_plot(self, plot):
        if isinstance(plot, TraceItem):
            self.newTrace()
            self.curTrace.setName(plot.name())
            self.curTrace.copy_data(plot)
            
            self.sync_buttons()
            self.curTrace.toggleShowFill(self.checkBox_fill)
            self.curTrace.toggleShowPoints(self.checkBox_points)
            self.curTrace.toggleShowCurve(self.checkBox_curve)
            self.curTrace.update_slice_table(self.table_slice)
        
        if isinstance(plot, ImageItem):
            self.newTrace()
            self.curTrace.setName(plot.name)
            self.curTrace.copy_data(plot)

            self.sync_buttons()
            self.curTrace.toggleShowFill(self.checkBox_fill)
            self.curTrace.toggleShowPoints(self.checkBox_points)
            self.curTrace.toggleShowCurve(self.checkBox_curve)
            self.curTrace.update_slice_table(self.table_slice)

    def ds_menu(self, pos):
        item = self.tree_data.itemAt(pos)
        if item is None:
            return
        try:
            if item.isClickable:
                pass
        except AttributeError:
            return

        valName = str(item.text(0))
        argIndex = 0
        extra = ""
        ds = item.ds
        if item.dataType == 'arg':
            valName = item.valName
            argName = str(item.text(0))
            extra = " vs " + argName
            argIndex = ds.get_args_to_val(valName).index(argName)

        globalPos = self.tree_data.mapToGlobal(pos)
        myMenu = QtGui.QMenu()
        myMenu.addAction("plot " + valName + extra)
        selectedItem = myMenu.exec_(globalPos)
        if selectedItem is None:
            return
        if str(selectedItem.text()) == "plot " + valName + extra:
            self.newTrace()
            index = self.combo_selectSource.findText(ds.name)
            self.combo_selectSource.setCurrentIndex(index)
            self.select_source(index)
            
            index = self.combo_select_val.findText(valName)
            self.combo_select_val.setCurrentIndex(index)
            self.select_val(index)

            self.combo_select_arg.setCurrentIndex(argIndex)
            self.select_arg(argIndex)

    def init_appearance(self):
        """Initialize the Trace Appearance table."""
        tbl = self.table_appearance

        # Creating and connecting point pen buttons
        self.point_pen_color = ColorButton()
        self.point_pen_size = pqg.SpinBox(
            step=.1, dec=True, minStep=.1, bounds=(0, None))
        self.point_pen_color.sigColorChanging.connect(self.set_point_pen)
        self.point_pen_size.sigValueChanging.connect(self.set_point_pen)
        tbl.setCellWidget(0, 0, self.point_pen_color)
        tbl.setCellWidget(0, 1, self.point_pen_size)

        # Creating and connecting point outline buttons
        self.point_outline_color = ColorButton()
        self.point_outline_size = pqg.SpinBox(
            step=.1, dec=True, minStep=.01, bounds=(0, 1))
        self.point_outline_color.sigColorChanging.connect(self.set_point_outline)
        self.point_outline_size.sigValueChanging.connect(self.set_point_outline)
        tbl.setCellWidget(1, 0, self.point_outline_color)
        tbl.setCellWidget(1, 1, self.point_outline_size)

        # Creating and connecting point style buttons
        self.point_shape = QtGui.QComboBox()
        self.point_shape.addItems(
            ["Circle", "Square", "Triangle", "Diamond", 'Plus'])
        self.point_shape.activated.connect(self.set_point_shape)
        self.px_mode = QtGui.QCheckBox("px mode")
        self.px_mode.setChecked(True)
        self.px_mode.stateChanged.connect(self.toggle_px_mode)
        tbl.setCellWidget(2, 0, self.point_shape)
        tbl.setCellWidget(2, 1, self.px_mode)

        # Creating and connecting curve pen buttons
        self.curve_pen_color = ColorButton()
        self.curve_pen_size = pqg.SpinBox(
            step=.1, dec=True, minStep=.1, bounds=(0, None))
        self.curve_pen_color.sigColorChanging.connect(self.set_curve_pen)
        self.curve_pen_size.sigValueChanging.connect(self.set_curve_pen)
        tbl.setCellWidget(3, 0, self.curve_pen_color)
        tbl.setCellWidget(3, 1, self.curve_pen_size)

        # Creating and connecting curve shadow buttons
        self.curve_shadow_color = ColorButton()
        self.curve_shadow_size = pqg.SpinBox(
            step=.1, dec=True, minStep=.1, bounds=(0, 1))
        self.curve_shadow_color.sigColorChanging.connect(self.set_curve_shadow)
        self.curve_shadow_size.sigValueChanging.connect(self.set_curve_shadow)
        tbl.setCellWidget(4, 0, self.curve_shadow_color)
        tbl.setCellWidget(4, 1, self.curve_shadow_size)

        # Creating and connecting fill buttons
        self.curve_fill_color = ColorButton()
        self.curve_fill_level = pqg.SpinBox(step=.1, dec=True, minStep=.1)
        self.curve_fill_color.sigColorChanging.connect(self.set_curve_fill)
        self.curve_fill_level.sigValueChanging.connect(self.set_curve_fill)
        tbl.setCellWidget(5, 0, self.curve_fill_color)
        tbl.setCellWidget(5, 1, self.curve_fill_level)

    def toggle_show_points(self, checkBox):
        if self.curTrace is not None:
            self.curTrace.toggleShowPoints(checkBox)

    def toggle_show_curve(self, checkBox):
        if self.curTrace is not None:
            self.curTrace.toggleShowCurve(checkBox)

    def toggle_show_fill(self, checkBox):
        if self.curTrace is not None:
            self.curTrace.toggleShowFill(checkBox)

    def set_point_pen(self, *args):
        if self.curTrace is not None:
            color = self.point_pen_color.color()
            size = self.point_pen_size.value()
            self.curTrace.setPointPen(color, size)

    def set_point_outline(self, *args):
        if self.curTrace is not None:
            color = self.point_outline_color.color()
            size = self.point_outline_size.value()
            self.curTrace.setPointOutline(color, size)

    def set_point_shape(self):
        if self.curTrace is not None:
            self.curTrace.setPointShape(self.point_shape)

    def toggle_px_mode(self):
        if self.curTrace is not None:
            self.curTrace.togglePxMode(self.px_mode)

    def set_curve_pen(self, *args):
        if self.curTrace is not None:
            color = self.curve_pen_color.color()
            size = self.curve_pen_size.value()
            self.curTrace.setCurvePen(color, size)

    def set_curve_shadow(self, *args):
        if self.curTrace is not None:    
            color = self.curve_shadow_color.color()
            size = self.curve_shadow_size.value()
            self.curTrace.setCurveShadow(color, size)

    def set_curve_fill(self, *args):
        if self.curTrace is not None:
            color = self.curve_fill_color.color()
            level = self.curve_fill_level.value()
            self.curTrace.setFill(color, level)

    def sync_buttons(self):
        if self.curTrace is None:
            return

        trace = self.curTrace

        self.combo_select_val.blockSignals(True)
        self.combo_selectSource.blockSignals(True)
        self.combo_select_arg.blockSignals(True)
        self.point_pen_color.blockSignals(True)
        self.point_pen_size.blockSignals(True)
        self.point_outline_color.blockSignals(True)
        self.point_outline_size.blockSignals(True)
        self.point_shape.blockSignals(True)
        self.px_mode.blockSignals(True)
        self.curve_pen_color.blockSignals(True)
        self.curve_pen_size.blockSignals(True)
        self.curve_shadow_color.blockSignals(True)
        self.curve_shadow_size.blockSignals(True)
        self.curve_fill_color.blockSignals(True)
        self.curve_fill_level.blockSignals(True)
        self.checkBox_points.blockSignals(True)
        self.checkBox_curve.blockSignals(True)
        self.checkBox_fill.blockSignals(True)


        if trace.argName is not None:
            index = self.combo_selectSource.findText(trace.ds.name)
            self.combo_selectSource.setCurrentIndex(index)
            self.select_source(index)

            index = self.combo_select_val.findText(trace.valName)
            self.combo_select_val.setCurrentIndex(index)
            self.select_val(index)

            index = self.combo_select_arg.findText(trace.argName)
            self.combo_select_arg.setCurrentIndex(index)
        else:
            self.combo_selectSource.setCurrentIndex(-1)
            self.combo_select_val.clear()
            self.combo_select_arg.clear()

        pointDict = {'o': 'Circle', 's': 'Square',
                     't': 'Triangle', 'd': 'Diamond', '+': 'Plus'}
        index = self.point_shape.findText(pointDict[trace.symbol])
        self.point_shape.setCurrentIndex(index)

        self.point_pen_color.setColor(trace.pointColor)
        self.point_pen_size.setValue(trace.pointSize)
        self.point_outline_color.setColor(trace.outlineColor)
        self.point_outline_size.setValue(trace.outlineSize)
        self.px_mode.setChecked(trace.pxMode)
        self.curve_pen_color.setColor(trace.curveColor)
        self.curve_pen_size.setValue(trace.curveSize)
        self.curve_shadow_color.setColor(trace.shadowColor)
        self.curve_shadow_size.setValue(trace.shadowSize)
        self.curve_fill_color.setColor(trace.fillColor)
        self.curve_fill_level.setValue(trace.fillLevel)
        self.checkBox_points.setChecked(trace.showPoints)
        self.checkBox_curve.setChecked(trace.showCurve)
        self.checkBox_fill.setChecked(trace.showFill)

        self.combo_select_val.blockSignals(False)
        self.combo_selectSource.blockSignals(False)
        self.combo_select_arg.blockSignals(False)
        self.point_pen_color.blockSignals(False)
        self.point_pen_size.blockSignals(False)
        self.point_outline_color.blockSignals(False)
        self.point_outline_size.blockSignals(False)
        self.point_shape.blockSignals(False)
        self.px_mode.blockSignals(False)
        self.curve_pen_color.blockSignals(False)
        self.curve_pen_size.blockSignals(False)
        self.curve_shadow_color.blockSignals(False)
        self.curve_shadow_size.blockSignals(False)
        self.curve_fill_color.blockSignals(False)
        self.curve_fill_level.blockSignals(False)
        self.checkBox_points.blockSignals(False)
        self.checkBox_curve.blockSignals(False)
        self.checkBox_fill.blockSignals(False)

    def select_source(self, index):
        """Change the dataStream that COMBO_SELECT_VAL pulls from
        and clear COMBO_SELECT_ARG."""
        dsName = str(self.combo_selectSource.currentText())
        ds = self.dataStreams[dsName]
        self.combo_select_val.clear()
        self.combo_select_arg.clear()
        self.combo_select_val.addItems(ds.vals.keys())

    def select_val(self, index):
        valName = str(self.combo_select_val.currentText())
        dsName = str(self.combo_selectSource.currentText())
        ds = self.dataStreams[dsName]
        self.combo_select_arg.clear()
        self.combo_select_arg.addItems(ds.get_args_to_val(valName))

    def select_arg(self, index):
        argName = str(self.combo_select_arg.currentText())
        valName = str(self.combo_select_val.currentText())
        dsName = str(self.combo_selectSource.currentText())
        ds = self.dataStreams[dsName]
        
        if self.curTrace is None:
            self.newTrace()
        
        self.curTrace.set_data_source(ds, valName, argName)
        self.curTrace.update_slice_table(self.table_slice)
        self.sync_buttons()

    def toggleLogX(self):
        if self.checkBox_logX.isChecked():
            self.plot.getPlotItem().setLogMode(x=True)
        else:
            self.plot.getPlotItem().setLogMode(x=False)

    def toggleLogY(self):
        if self.checkBox_logY.isChecked():
            self.plot.getPlotItem().setLogMode(y=True)
        else:
            self.plot.getPlotItem().setLogMode(y=False)

    def deleteTab(self):
        for key, trace in self.traces.items():
            trace.delete()

        del self.traces
        del self.graph
        del self.plot

        self.destroy()

    def delete_trace(self, trace):
        self.traces.pop(trace.name())

        index = -1
        for row in range(self.table_traces.rowCount()):
            item = self.table_traces.item(row, 0)
            if str(item.text()) == trace.name():
                index = row
        if index == -1:
            raise Exception("Cannot find trace in table.")

        if self.curTrace == trace:
            if len(self.traces) == 0:
                self.curTrace = None
            elif index == self.table_traces.rowCount()-1:
                name = str(self.table_traces.item(index-1, 0).text())
                trace = self.traces[name]
                self.change_to_trace(trace)
            elif index < self.table_traces.rowCount()-1:
                name = str(self.table_traces.item(index+1, 0).text())
                trace = self.traces[name]
                self.change_to_trace(trace)

        if self.graph.plotToPaste == trace:
            self.graph.plotToPaste = None

        self.table_traces.removeRow(index)

    def setName(self, newName):
        self.name = str(newName)

    def addDataSource(self, ds):
        self.combo_selectSource.addItem(ds.name)

    def updateRangeBoxes(self):
        """ Sets the values of the spin boxes to the current viewable range."""
        if self.enableUpdateBoxes:
            self.enableSetRange = False
            ((x_min, x_max), (y_min, y_max)
             ) = self.plot.getPlotItem().viewRange()
            self.spin_x_min.setValue(float(x_min))
            self.spin_x_max.setValue(float(x_max))
            self.spin_y_min.setValue(float(y_min))
            self.spin_y_max.setValue(float(y_max))
            self.enableSetRange = True
            autoRange = self.plot.getPlotItem().getViewBox().autoRangeEnabled()
            self.btn_autoScaleX.setChecked(autoRange[0])
            self.btn_autoScaleY.setChecked(autoRange[1])

    def setRange(self):
        if self.enableSetRange:
            self.enableUpdateBoxes = False
            x_min = self.spin_x_min.value()
            x_max = self.spin_x_max.value()
            y_min = self.spin_y_min.value()
            y_max = self.spin_y_max.value()
            self.plot.getPlotItem().setRange(
                xRange=(x_min, x_max), yRange=(y_min, y_max), padding=False)
            self.enableUpdateBoxes = True
            self.btn_autoScaleX.setChecked(False)
            self.btn_autoScaleY.setChecked(False)
            self.plot.enableAutoRange(enable=False)

    def autoScaleX(self):
        """ Auto scales the x axis such that all item are viewable. """
        enable = self.btn_autoScaleX.isChecked()
        XAxis = pqg.ViewBox.XAxis
        self.plot.enableAutoRange(axis=XAxis, enable=enable)

    def autoScaleY(self):
        """ Auto scales the y axis such that all item are viewable. """
        enable = self.btn_autoScaleY.isChecked()
        YAxis = pqg.ViewBox.YAxis
        self.plot.enableAutoRange(axis=YAxis, enable=enable)

    def showGrid(self):
        """ Toggles the grid on or off. """
        enable = self.checkBox_showGrid.isChecked()
        if enable:
            self.plot.getPlotItem().getAxis('left').setGrid(255)
            self.plot.getPlotItem().getAxis('bottom').setGrid(255)
        else:
            self.plot.getPlotItem().getAxis('left').setGrid(False)
            self.plot.getPlotItem().getAxis('bottom').setGrid(False)

    def showLegend(self):
        if self.checkBox_showLegend.isChecked():
            self.legend = pqg.LegendItem()
            for trace in self.traces.itervalues():
                self.legend.addItem(trace, trace.NAME)
            self.legend.setParentItem(self.plot.getPlotItem())
        elif self.legend is not None:
            vb = self.plot.getPlotItem().getViewBox()
            vb.removeItem(self.legend)
            self.legend = None

    def setBackgroundColor(self):
        """ Sets the background color to the value of the value
        of btnColor_background."""
        self.backgroundColor = self.btnColor_background.color()
        self.plot.getPlotItem().getViewBox().setBackgroundColor(
            self.backgroundColor)

    def setGridColor(self):
        """Sets the axis color to the value of btnColor_grid. """
        self.axisColor = self.btnColor_grid.color()
        self.plot.getPlotItem().getAxis('left').setPen(self.axisColor)
        self.plot.getPlotItem().getAxis('bottom').setPen(self.axisColor)

    def lockRatio(self):
        """ Lock the aspect ratio of my view box to be that of my Image."""
        if self.checkBox_lockRatio.isChecked():
            self.plot.getPlotItem().getViewBox().setAspectLocked(True, 1.0)
        else:
            self.plot.getPlotItem().getViewBox().setAspectLocked(False)

    def cell_clicked(self, row, column):
        item = self.table_traces.item(row, 0)
        traceName = str(item.text())
        trace = self.traces.get(traceName, None)
        if trace is None:
            raise GraphException("Not in known traces")
        else:
            self.change_to_trace(trace)

    def change_to_trace(self, trace):
        """ Set curTrace to TRACE. Update all the buttons/table_slice
        and then highlight the proper row in the table_traces."""
        # Deselecting the previous curTrace
        if self.curTrace is not None:
            index = -1
            for row in range(self.table_traces.rowCount()):
                item = self.table_traces.item(row, 0)
                if str(item.text()) == self.curTrace.name():
                    index = row
            if index != -1: 
                item = self.table_traces.item(index, 0)
                item.setBackgroundColor(pqg.mkColor(255, 255, 255, 255))

        # Selecting the current trace
        index = -1
        for row in range(self.table_traces.rowCount()):
            item = self.table_traces.item(row, 0)
            if str(item.text()) == trace.name():
                index = row
        if index != -1:
            item = self.table_traces.item(index, 0)
            item.setBackgroundColor(pqg.mkColor(0, 200, 200, 200))

        self.curTrace = trace
        trace.update_slice_table(self.table_slice)
        self.sync_buttons()

    def newTrace(self):
        trace = TraceItem(self)
        trace.NAME = uniqueName("Trace {}", 0, self.traces)
        self.traces[trace.NAME] = trace

        trace.add_to_trace_table(self.table_traces)
        self.change_to_trace(trace)

    def rename(self, trace, newName):
        oldName = trace.name()
        if newName in self.traces.keys():
            return oldName
        else:
            self.traces.pop(oldName)
            self.traces[newName] = trace
            return newName

