import numpy as np

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
        return NotImplementedError()


class DataTxtFile(dataStream):
    def __init__(self, path):
        """Set the parent GUI element of the datastream. Set the path of the .txt file,
        and load the data it contains."""
        self.path = path
        self.shape = (0, 0)
        self.data = np.zeros(self.shape)
        self.loadData()

    def getData(self):
        return self.data

    def dimensions(self):
        return self.shape[1]

    def getDimension(self, dim):
        condition = [True for _ in range(len(self.data))]
        if dim > self.shape[1]:
            return np.zeros((0, 0))
        return np.compress(condition, data, dim)

    def loadData(self):
        try:
            data = open(path, 'r')
        except IOError:
            print("The requested file doesn't exist: " + path)
            self.destroy()
            return
    
        data = []
        lineNum = 1

        for line in data:
            items = line.split
            if lineNum == 1:
                numDim = len(items)
            elif len(items) != numDim:
                print("Length error at line: " + str(lineNum))
                self.destroy()
                return
            else:
                try:
                    temp = []
                    for value in items:
                        temp += [float(value)]
                    data += temp
                except ValueError:
                    print("Error coercing value to float at line: " + str(lineNum))
                    self.destroy()
                    return
            lineNum += 1

        self.data = np.array(data)
        self.shape = self.data.shape