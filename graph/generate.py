import numpy as np
import math
import pyqtgraph as pqg
from PyQt4 import QtCore, QtGui
import random
import h5py



# dataFile = open("data/image.txt", 'w')
#dataFile.close()
def genImageData():
	data = np.zeros((100, 100))
	for x in range(0, 100):
		for y in range(0, 100):
			data[x][y] = math.hypot(x, y)
	return data

def genScatterData():
	x = []
	y = []
	brushes = []
	
	for xval in range(0, 400):
		for yval in range(0, 400):
			x += [xval]
			y += [yval]
			r = 255 * random.random()
			g = 255 * random.random()
			b = 255 * random.random()
			brushes += [pqg.mkColor(r, g, b)]
	return (np.array(x), np.array(y), brushes)
	
data = genImageData()
x = np.array([i for i in range(100)])
y = np.array([i for i in range(100)])
f = h5py.File('data/imageTest.hdf5', 'w')
f.create_dataset('vals', data = data)
f.create_dataset('args/x', data = x)
f.create_dataset('args/y', data = y)
f.close()



# dataFile = open("data/image.txt", 'w')
#dataFile.close()

# plot = pqg.plot()
# x, y, brushes = genScatterData()
# scatter = pqg.ScatterPlotItem(x, y, pxMode = False, size = 1, symbol = 's')
# scatter.setBrush(brushes)
# plot.addItem(scatter)


# plot = pqg.plot()
# imv = pqg.ImageView()
# imv.show()
# imv.setImage(genImageData())
# plot.addItem(imv)


# plot = pqg.plot()
# data = genImageData()
# image = pqg.ImageItem(image = data)
# plot.addItem(image)
# levels = [[0, 255] for _ in range(3)]
# levels = np.array(levels)