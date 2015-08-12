from PyQt4 import QtGui
from utils import *
import pyqtgraph as pqg
import numpy as np
from colorButton import ColorButton
import traceitem


class ImageItem():
    def __init__(self, imageTab):
        self.imageTab = imageTab
        self.sliceTable = None
        self.name = None
        self.sliceParams = {}
        self.ds = None
        self.valName = None
        self.sliceSpins = {}

        self.axis = {}
        self.axisNames = {}
        self.gradient = None
        self.levels = None
        self.time = None
        self.rgb = False
        
        self.isocurves = []
        self.isoLevelMin = float('inf')
        self.isoLevelMax = float('-inf')

        self.isoGradient = self.imageTab.gradient_isocurve
        self.savedGradient = None
        self.isoWidth = 3
        self.displayIso = True
        self.isoIndex = 0

        self.updateSlice = True

    def copy_data(self, other):
        if isinstance(other, ImageItem):
            self.ds = other.ds
            self.valName = other.valName
            self.sliceParams = other.sliceParams.copy()
            self.axis = other.axis.copy()
            self.axisNames = other.axisNames.copy()
            self.gradient = other.gradient
            self.levels = other.levels
            self.time = other.time
            self.rgb = other.rgb

            self.isoLevelMin = other.isoLevelMin
            self.isoLevelMax = other.isoLevelMax
            self.isoWidth = other.isoWidth
            self.displayIso = other.displayIso

            for curve in other.isocurves:
                width = curve.width
                color = curve.color
                level = curve.level
                self.add_isocurve(level, color, width)
        elif isinstance(other, traceitem.TraceItem):
            self.ds = other.ds
            self.valName = other.valName
            args =  self.ds.get_args_to_val(self.valName)
            if len(args) < 2:
                self.delete()
                raise GraphException("{} does not have two dimensions to plot.".format(self.valName))
            xIndex = args.index(other.argName)
            yIndex = (xIndex + 1) % len(args)
            self.axis = {'x': xIndex, 'y': yIndex, 't': None, 'c': None}
            self.axisNames = {'x': args[xIndex], 'y': args[yIndex], 't': 'None', 'c': 'None'}
            
            self.sliceParams = other.sliceParams.copy()
            self.sliceParams[args[yIndex]] = (0, self.ds.get_arg_shape(args[yIndex]))

    def name(self):
        return self.name

    def setName(self, newName):
        """Set SELF's name to NEWNAME."""
        newName = str(newName)
        if newName == self.name:
            return

        validName = self.imageTab.rename(self, newName)
        self.name = validName
        self.item_name.setText(validName)

    def set_axis(self, xAxis, yAxis, tAxis='None', cAxis='None'):
        correctLength = 4
        if tAxis == 'None' and cAxis == 'None':
            correctLength = 3
        if len(set([xAxis, yAxis, tAxis, cAxis])) != correctLength:
            message = "Duplicates selected. Won't update image until proper selection."
            raise GraphException(message)

        args = self.ds.get_args_to_val(self.valName)
        if xAxis not in args:
            raise GraphException("{} is not in {}".format(xAxis, self.ds.name))
        if yAxis not in args:
            raise GraphException("{} is not in {}".format(yAxis, self.ds.name))
        if tAxis != 'None' and tAxis not in args:
            raise GraphException("{} is not in {}".format(tAxis, self.ds.name))
        if cAxis != 'None' and cAxis not in args:
            raise GraphException("{} is not in {}".format(cAxis, self.ds.name))
        xIndex = args.index(xAxis)
        yIndex = args.index(yAxis)
        tIndex = None
        cIndex = None
        if tAxis != 'None':
            tIndex = args.index(tAxis)
        if cAxis != 'None':
            cIndex = args.index(cAxis)
        self.axis = {'x': xIndex, 'y': yIndex, 't': tIndex, 'c': cIndex}
        self.axisNames = {'x': xAxis, 'y': yAxis, 't': tAxis, 'c': cAxis}

        for arg in args:
            self.sliceParams[arg] = 0
        self.sliceParams[xAxis] = (0, self.ds.get_arg_shape(xAxis))
        self.sliceParams[yAxis] = (0, self.ds.get_arg_shape(yAxis))
        if tAxis != 'None':
            self.sliceParams[tAxis] = (0, self.ds.get_arg_shape(tAxis))

        self.rgb = False
        if cAxis != 'None':
            self.sliceParams[cAxis] = (0, self.ds.get_arg_shape(cAxis))
            gradient = self.imageTab.plot.getHistogramWidget().gradient
            gradient.loadPreset('grey')
            self.rgb = True

        self.update_slice_table(self.imageTab.table_slice)
        self.display_image()

    def set_data_source(self, ds, valName):
        self.ds = ds
        self.valName = valName
        self.sliceParams.clear()
        args = ds.get_args_to_val(valName)

        for arg in args:
            self.sliceParams[arg] = 0

        if len(args) < 2:
            raise GraphException("Not enough dimensions to create an image.")
        else:
            self.set_axis(args[0], args[1])

    def display_image(self):
        image = self.imageTab.plot

        tVals = None
        if self.axis['t'] is not None:
            args = self.ds.get_args_to_val(self.valName)
            tArg = args[self.axis['t']]
            tSlice = slice(*self.sliceParams[tArg])
            tVals = self.ds.load_arg(tArg, tSlice)

        axis = self._convert_axis()
        s = self.ds.gen_slice(self.valName, self.sliceParams)
        data = self.ds.load_val(self.valName, s)
        data, axisDict = self.swap_axis(data, axis)
        image.setImage(data, levels=self.levels,
                       axes=axisDict, xvals=tVals)

    def swap_axis(self, data, axisDict):
        """Shuffles the axis in DATA around until they are
        in t, x, y, c order. With the t, x ,y, c axis specified by
        AXISDICT. Returns the new data, as well as the new axisDict."""
        if axisDict['t'] is not None:
            tIndex = axisDict['t']
            for k, v in axisDict.iteritems():
                if v is None:
                    continue
                if v < tIndex:
                    axisDict[k] += 1
            data = np.rollaxis(data, tIndex, 0)

            xIndex = axisDict['x']
            for k, v in axisDict.iteritems():
                if v is None:
                    continue
                if 0 < v < xIndex:
                    axisDict[k] += 1
            data = np.rollaxis(data, xIndex, 1)

            yIndex = axisDict['y']
            for k, v in axisDict.iteritems():
                if v is None:
                    continue
                if 1 < v < yIndex:
                    axisDict[k] += 1
            data = np.rollaxis(data, yIndex, 2)

            cIndex = None
            if axisDict['c'] is not None:
                cIndex = 3
            return data, {'t': 0, 'x': 1, 'y': 2, 'c': cIndex}
        else:
            xIndex = axisDict['x']
            for k, v in axisDict.iteritems():
                if v is None:
                    continue
                if v < xIndex:
                    axisDict[k] += 1
            data = np.rollaxis(data, xIndex, 0)

            yIndex = axisDict['y']
            for k, v in axisDict.iteritems():
                if v is None:
                    continue
                if 0 < v < yIndex:
                    axisDict[k] += 1
            data = np.rollaxis(data, yIndex, 1)

            cIndex = None
            if axisDict['c'] is not None:
                cIndex = 3
            return data, {'x': 0, 'y': 1, 't': None, 'c': cIndex}

    def toggleUpdate(self):
        raise NotImplementedError()

    def delete(self):
        """Delete this imageItem, and all associated Isocurves and data."""
        for curve in self.isocurves:
            self.delete_iso(curve)

        self.imageTab.delete_image(self)
        del self.imageTab

    def add_to_image_table(self, imageTable):
        table = imageTable
        row = table.rowCount()
        table.setRowCount(row + 1)
        self.item_name = QtGui.QTableWidgetItem(self.name)
        self.item_name.image = self
        table.setItem(row, 0, self.item_name)

        self.checkBoxUpdate = QtGui.QCheckBox()
        self.checkBoxUpdate.setChecked(False)
        self.checkBoxUpdate.stateChanged.connect(self.toggleUpdate)
        table.setCellWidget(row, 1, self.checkBoxUpdate)

        btn_delete = QtGui.QPushButton('Delete')
        btn_delete.clicked.connect(self.delete)
        table.setCellWidget(row, 2, btn_delete)

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)

    def update_slice_table(self, sliceTable):
        if self.valName is None:
            sliceTable.clear()
            sliceTable.setHorizontalHeaderLabels(['axis', 'indices', 'values'])
            sliceTable.resizeColumnsToContents()
            sliceTable.horizontalHeader().setStretchLastSection(True)
            return

        self.sliceTable = sliceTable
        sliceTable.clear()
        sliceTable.setHorizontalHeaderLabels(['axis', 'indices', 'values'])
        sliceTable.setRowCount(len(self.sliceParams))
        args = self.ds.get_args_to_val(self.valName)
        axisArgs = []
        for i in self.axis.values():
            if i is not None:
                axisArgs += [args[i]]

        row = 0
        for argName in axisArgs:
            argItem = QtGui.QTableWidgetItem(argName)
            sliceTable.setItem(row, 0, argItem)
            minBounds = (0, self.ds.get_arg_shape(argName) - 2)
            maxBounds = (1, self.ds.get_arg_shape(argName) - 1)
            spin_sliceMin = pqg.SpinBox(bounds=minBounds, step=1.0, int=True)
            spin_sliceMin.setValue(self.sliceParams[argName][0])
            spin_sliceMax = pqg.SpinBox(bounds=maxBounds, step=1.0, int=True)
            spin_sliceMax.setValue(self.sliceParams[argName][1])
            self.sliceSpins[argName] = (spin_sliceMin, spin_sliceMax)

            spin_sliceMin.sigValueChanged.connect(self.update_slice)
            spin_sliceMax.sigValueChanged.connect(self.update_slice)
            spinLayout = QtGui.QHBoxLayout()
            spinLayout.addWidget(spin_sliceMin)
            spinLayout.addWidget(spin_sliceMax)
            cellWidget = QtGui.QWidget()
            cellWidget.setLayout(spinLayout)
            
            sliceTable.setCellWidget(row, 1, cellWidget)
            sliceTable.setCellWidget(row, 2, QtGui.QLabel())
            row += 1
        
        for argName, s in self.sliceParams.iteritems():
            if argName in axisArgs:
                continue

            argItem = QtGui.QTableWidgetItem(argName)
            sliceTable.setItem(row, 0, argItem)

            bounds = (0, self.ds.get_arg_shape(argName) - 1)
            spin = pqg.SpinBox(bounds=bounds, step=1.0, int=True)
            spin.setValue(self.sliceParams[argName])
            spin.sigValueChanged.connect(self.update_slice)
            self.sliceSpins[argName] = spin

            sliceTable.setCellWidget(row, 1, spin)
            sliceTable.setCellWidget(row, 2, QtGui.QLabel())
            row += 1

        self.update_slice_labels()
        sliceTable.resizeColumnsToContents()
        sliceTable.resizeRowsToContents()
        sliceTable.horizontalHeader().setStretchLastSection(True)

    def update_slice_labels(self):
        for row in range(self.sliceTable.rowCount()):
            argName = str(self.sliceTable.item(row, 0).text())
            s = self.sliceParams[argName]
            if isinstance(s, tuple):
                valString = '[' + str(self.ds.load_arg(argName, s[0])) + ',  '
                valString += str(self.ds.load_arg(argName, s[1] - 1)) + ']'
            else:
                valString = str(self.ds.load_arg(argName, s))
            label = self.sliceTable.cellWidget(row, 2)
            label.setText(valString)

    def update_slice(self):
        if self.updateSlice == False:
            return

        self.updateSlice = False
        for argName, spins in self.sliceSpins.iteritems():
            if isinstance(spins, tuple):
                sliceMin = spins[0]
                sliceMax = spins[1]
                sliceMin.setMaximum(sliceMax.value() - 1)
                sliceMax.setMinimum(sliceMin.value() + 1)
                
                sMin = sliceMin.value()
                sMax = sliceMax.value() + 1
                self.sliceParams[argName] = (sMin, sMax)
            else:
                self.sliceParams[argName] = spins.value()

        self.update_slice_labels()
        levels = self.imageTab.plot.get_levels()
        self.display_image()
        self.imageTab.plot.setLevels(*levels)
        self.updateSlice = True

    def _convert_axis(self):
        axis = []
        for k, v in self.axis.iteritems():
            axis += [[k, v]]
        axis = sorted(axis, key=lambda item: item[1])
        axisDict = {}
        index = 0
        for i in range(len(axis)):
            if axis[i][1] is None:
                axisDict[axis[i][0]] = None
            else:
                axisDict[axis[i][0]] = index
                index += 1
        return axisDict

    def new_isocurve(self, table):
        """Create a new isocurve."""
        width = self.isoWidth
        level = 0
        if len(self.isocurves) == 0:
            color = self.isoGradient.getColor(0.5)
            isocurve = self.add_isocurve(level, color, width)
            self.add_isocurve_to_table(isocurve)
            self.isoLevelMin = 0
            self.isoLevelMax = 1
        elif len(self.isocurves) == 1:
            other = self.isocurves[0]
            if other.level > level:
                otherColor = self.isoGradient.getColor(1.0)
                other.setPen(otherColor, width=other.width)
                color = self.isoGradient.getColor(0.0)
                self.isoLevelMin = level
                self.isoLevelMax = other.level
            if other.level < level:
                otherColor = self.isoGradient.getColor(0.0)
                other.setPen(otherColor, width=other.width)
                color = self.isoGradient.getColor(1.0)
                self.isoLevelMin = other.level
                self.isoLevelMax = level
            else:
                level += 1
                otherColor = self.isoGradient.getColor(0.0)
                other.setPen(otherColor, width=other.width)
                color = self.isoGradient.getColor(1.0)
                self.isoLevelMin = other.level
                self.isoLevelMax = level
            isocurve = self.add_isocurve(level, color, width)
            self.add_isocurve_to_table(isocurve)
        else:
            if level < self.isoLevelMin:
                self.isoLevelMin = level
                color = self.isoGradient.getColor(0.0)
                isocurve = self.add_isocurve(level, color, width)
                self.add_isocurve_to_table(isocurve)
                self.update_iso_colors()
            if level > self.isoLevelMax:
                self.isoLevelMax = level
                color = self.isoGradient.getColor(1.0)
                isocurve = self.add_isocurve(level, color, width)
                self.add_isocurve_to_table(isocurve)
                self.update_iso_colors()
            else:
                x = (level - self.isoLevelMin)
                x /= (self.isoLevelMax - self.isoLevelMin)
                color = self.isoGradient.getColor(1.0)
                isocurve = self.add_isocurve(level, color, width)
                self.add_isocurve_to_table(isocurve)

        if self.displayIso:
            self.display_isocurve(isocurve)


    def add_isocurve(self, level, color, width):
        """Create and return a new isocurve."""
        pen = pqg.mkPen(color, width=width)
        curve = pqg.IsocurveItem(None, level, pen)
        curve.width = width
        curve.color = color
        curve.horzLine = pqg.InfiniteLine(pos=level, angle=0, pen=pen)
        curve.vertLine = pqg.InfiniteLine(pos=level, angle=90, pen=pen)
        curve.id = self.isoIndex
        self.isoIndex += 1
        self.isocurves += [curve]
        return curve

    def add_isocurve_to_table(self, curve):
        """Add the isocurve CURVE to self.imageTab.table_isocurve."""
        table = self.imageTab.table_isocurve
        row = table.rowCount()
        table.setRowCount(row + 1)

        spin = pqg.SpinBox(value=curve.level, step=.1, dec=True, minStep=.1)
        setLevel = lambda: self.set_iso_level(curve, spin)
        spin.sigValueChanging.connect(setLevel)
        table.setCellWidget(row, 0, spin)
        curve.spinLevel = spin

        cButton = ColorButton(color=curve.color)
        setColor = lambda: self.set_iso_color(curve, cButton)
        cButton.sigColorChanging.connect(setColor)
        table.setCellWidget(row, 1, cButton)
        curve.colorBtn = cButton

        spin2 = pqg.SpinBox(value=curve.width, step=.1, dec=True, minStep=.1)
        setWidth = lambda: self.set_iso_width(curve, spin2)
        spin2.sigValueChanging.connect(setWidth)
        table.setCellWidget(row, 2, spin2)
        curve.spinWidth = spin2

        btnDelete = QtGui.QPushButton('delete')
        btnDelete.id = curve.id
        deleteIso = lambda: self.delete_iso(curve)
        btnDelete.clicked.connect(deleteIso)
        table.setCellWidget(row, 3, btnDelete)

    def delete_iso(self, curve):
        curve.setData(None)
        curve.setParentItem(None)
        self.imageTab.plot.ui.plot_slice_horiz.removeItem(curve.horzLine)
        self.imageTab.plot.ui.plot_slice_vert.removeItem(curve.vertLine)

        index = -1
        for i in range(len(self.isocurves)):
            c = self.isocurves[i]
            if c.id == curve.id:
                index = i
        if index == -1:
            raise Exception("Curve not found")
        self.isocurves.pop(index)
        
        table = self.imageTab.table_isocurve
        index = -1
        for row in range(table.rowCount()):
            btn = table.cellWidget(row, 3)
            if btn.id == curve.id:
                index = row
        if index == -1:
            raise Exception("Curve not found")
        self.imageTab.table_isocurve.removeRow(index)

        if len(self.isocurves) == 0:
            self.isoLevelMin = float('inf')
            self.isoLevelMax = float('-inf')
        elif curve.level in [self.isoLevelMin, self.isoLevelMax]:
            levels = [c.level for c in self.isocurves]
            self.isoLevelMin = min(levels)
            self.isoLevelMax = max(levels)
            self.update_iso_colors()
        del curve


    def set_iso_level(self, curve, spin):
        level = spin.value()
        prevLevel = curve.level
        curve.setLevel(level)
        curve.horzLine.setValue(level)
        curve.vertLine.setValue(level)

        if prevLevel == self.isoLevelMax and level < prevLevel:
            levels = [iso.level for iso in self.isocurves]
            if prevLevel not in levels:
                self.isoLevelMax = level
                self.update_iso_colors()
        if prevLevel == self.isoLevelMin and level > prevLevel:
            levels = [iso.level for iso in self.isocurves]
            if prevLevel not in levels:
                self.isoLevelMin = level
                self.update_iso_colors()
        if level > self.isoLevelMax:
            self.isoLevelMax = level
            self.update_iso_colors()
        if level < self.isoLevelMin:
            self.isoLevelMin = level
            self.update_iso_colors()
        if self.isoLevelMin < level < self.isoLevelMax:
            x = (level - self.isoLevelMin)
            x /= (self.isoLevelMax - self.isoLevelMin)
            color = self.isoGradient.getColor(x)
            curve.colorBtn.setColor(color)
            curve.color = color
            curve.setPen(color, width=curve.width)
            curve.horzLine.setPen(curve.color, width=curve.width)
            curve.vertLine.setPen(curve.color, width=curve.width)

    def set_iso_width(self, curve, spin):
        curve.width = spin.value()
        curve.setPen(curve.color, width=curve.width)
        curve.horzLine.setPen(curve.color, width=curve.width)
        curve.vertLine.setPen(curve.color, width=curve.width)

    def set_iso_color(self, curve, colorBtn):
        color = colorBtn.color()
        curve.color = color
        curve.setPen(color, width=curve.width)
        curve.horzLine.setPen(curve.color, width=curve.width)
        curve.vertLine.setPen(curve.color, width=curve.width)

    def update_iso_colors(self):
        """Update all the isocurve colors to match the new gradient or 
        new bounds."""
        if self.isoLevelMin == self.isoLevelMax:
            self.isoLevelMin -= 1

        for i in range(len(self.isocurves)):
            curve = self.isocurves[i]
            x = (curve.level - self.isoLevelMin)
            x /= (self.isoLevelMax - self.isoLevelMin)
            color = self.isoGradient.getColor(x)
            curve.colorBtn.setColor(color)
            curve.color = color
            curve.setPen(color, width=curve.width)
            curve.horzLine.setPen(curve.color, width=curve.width)
            curve.vertLine.setPen(curve.color, width=curve.width)

    def update_iso_widths(self):
        width = self.imageTab.spin_width.value()
        for curve in self.isocurves:
            curve.spinWidth.setValue(width)

    def display_isocurve(self, curve):
        """Display the curve on the current plot."""
        data = self.imageTab.plot.imageItem.image
        curve.setParentItem(self.imageTab.plot.imageItem)
        curve.setData(data)
        self.imageTab.plot.ui.plot_slice_horiz.addItem(curve.horzLine)
        self.imageTab.plot.ui.plot_slice_vert.addItem(curve.vertLine)

    def update_iso_data(self):
        if self.displayIso is False:
            return

        data = self.imageTab.plot.imageItem.image
        for curve in self.isocurves:
            curve.setData(data)

    def init_isocurves(self):
        for curve in self.isocurves:
            self.add_isocurve_to_table(curve)
        if self.displayIso:
            self.display_isocurves()

    def remove_isocurves(self):
        for curve in self.isocurves:
            curve.setData(None)
            curve.setParentItem(None)
            self.imageTab.plot.ui.plot_slice_horiz.removeItem(curve.horzLine)
            self.imageTab.plot.ui.plot_slice_vert.removeItem(curve.vertLine)

    def display_isocurves(self):
        for curve in self.isocurves:
            self.display_isocurve(curve)
