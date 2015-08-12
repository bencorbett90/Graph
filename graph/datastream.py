import numpy as np
from PyQt4 import QtCore, QtGui
import h5py
from utils import *


class DataStream():

    def __init__(self, path, dataPath):
        """Initializes a HDF5 DataStream. PATH is the path to the
        .hdf5 file, and DATAPATH is the path within the file to the
        specific dataset.
        """
        self.filePath = path
        self.dataPath = dataPath

        # Dictionary of the overall dataset attributes.
        self.attrs = {}

        # Dictionary of arg/val names to a dict of arg/val attributes,
        # the arg/val dataset path, and the dataset shape.
        # if a val also has dimScales which is a list of args names.
        self.args = {}
        self.vals = {}

        self.get_attrs()

        self.name = self.attrs['Name']

    def get_attrs(self):
        """Load all of the attributes of the dataset into SELF.ATTRS
        and all of the arg/val attributes into SELF.ARGS/SELF.VALS
        as well as the shape of the arg/val, the path to the arg/val
        and for vals the associated dimension scales."""

        f = h5py.File(self.filePath, 'r')
        for name, value in f[self.dataPath].attrs.iteritems():
            self.attrs[str(name)] = value

        for dsetName, dset in f[self.dataPath].iteritems():
            givenName = dset.attrs['Name']
            if dsetName[0:11] == 'Independent':
                if givenName not in self.args.iterkeys():
                    dsetName = givenName
                self.args[str(dsetName)] = {}
                attrDict = self.args[dsetName]
            elif dsetName[0:9] == 'Dependent':
                if givenName not in self.vals.iterkeys():
                    dsetName = givenName
                self.vals[str(dsetName)] = {}
                attrDict = self.vals[dsetName]
            else:
                continue

            # Adding the dataset attributes
            for name, value in dset.attrs.iteritems():
                attrDict[str(name)] = value

            # Adding the datset path and shape.
            attrDict['path'] = dset.name
            attrDict['shape'] = dset.shape

        # Taking care of dimension scales if the dataset
        # is an independent variable. Only use the first dim scale.
        for valDict in self.vals.itervalues():
            dset = f[valDict['path']]
            dimScales = []
            for i in range(len(dset.dims)):
                dimPath = dset.dims[i][0].name
                dimScales += [self._get_arg_name_from_path(dimPath)]
            valDict['dimScales'] = dimScales

        f.close()

    def get_vals(self, minDim):
        """Return a list of val names of vals of dimension greater than
        or equal to MINDIM."""
        valNames = []
        for valName, valDict in self.vals.iteritems():
            if len(valDict['shape']) >= minDim:
                valNames += [valName]

        return valNames

    def _get_arg_name_from_path(self, path):
        """Given an argument path, return the name used as the 
        given argumnet's key in SELF.ARGS"""
        for k, v in self.args.iteritems():
            if v['path'] == path:
                return k

    def load_arg(self, argName, s=None):
        """Return the argument ARGNAME[s]"""
        f = h5py.File(self.filePath, 'r')
        path = self.args[argName]['path']
        if s is None:
            data = f[path][:]
        else:
            data = f[path][s]
        f.close()
        return data

    def load_val(self, valName, s=None):
        f = h5py.File(self.filePath, 'r')
        path = self.vals[valName]['path']
        if s is None:
            data = f[path][..., :]
        else:
            data = f[path][s]
        f.close()
        return data

    def gen_slice(self, valName, sliceDict):
        """Generate a slice into val VALNAME using the dictionary SLICEDICT
        which is a dictionary from the names of the axis to the desired axis slice."""
        argNames = self.get_args_to_val(valName)
        s = []
        for argName in argNames:
            argSlice = sliceDict[argName]
            if isinstance(argSlice, tuple):
                argSlice = slice(*argSlice)
            s += [argSlice]
        return tuple(s)

    def get_args_to_val(self, valName):
        """Return the name of all the arguments to the value VALNAME."""
        return self.vals[valName]['dimScales']

    def get_val_shape(self, valName):
        return self.vals[valName]['shape']

    def get_arg_shape(self, argName):
        """Return the shape of arg ARGNAME. Return the first
        item of shape, since args are 1D."""
        return self.args[argName]['shape'][0]

    def addToTab(self, tab):
        """Add SELF to QTreeWidget TAB.TREE_DATA"""
        tree = tab.tree_data
        nameDict = tab.dataStreams

        if self.name in nameDict.keys():
            if nameDict[self.name] != self:
                baseName = self.name + '({})'
                self.name = uniqueName(baseName, 1, nameDict.keys())

        dsTW = QtGui.QTreeWidgetItem([self.name])

        for valName, valDict in self.vals.iteritems():
            valTW = QtGui.QTreeWidgetItem()
            valTW.setText(0, valName)
            valTW.setText(1, str(valDict['shape']))
            dsTW.addChild(valTW)

            #setting fields for action upon right click
            valTW.isClickable = True
            valTW.dataType = 'val'
            valTW.ds = self

            for argName in self.get_args_to_val(valName):
                argDict = self.args[argName]
                argTW = QtGui.QTreeWidgetItem()
                argTW.setText(0, argName)
                argTW.setText(1, str(argDict['shape']))
                valTW.addChild(argTW)

                #setting fields for action upon right click
                argTW.isClickable = True
                argTW.dataType = 'arg'
                argTW.valName = valName
                argTW.ds = self



        tree.addTopLevelItem(dsTW)
