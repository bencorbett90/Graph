import numpy as np
import os

class DataStream():
    def __init__(self):
        raise NotImplementedError()

    def getData(self):
        """Return the data in a numpy ndarray"""
        raise NotImplementedError()

    def dimensions(self):
        """Return the dimensions of the Data"""
        raise NotImplementedError()

    def getDimension(self, dim):
        """Return the data comprising the DIM'th dimension. Index from zero."""
        raise NotImplementedError()
    
    def getName(self):
        """Return the name of the data file."""
        raise NotImplementedError()

    def setName(self):
        """Set the name of this DataStream."""
        raise NotImplementedError()

    def dimName(self, dim):
        """Return the name of the DIM'th dimension."""
        return "Dimension {}".format(dim)

    def setDimName(self, dim, name):
        """Set the name of dimension DIM to NAME."""


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