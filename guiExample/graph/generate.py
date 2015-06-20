import numpy as np
import math
import pyqtgraph as pqg
from PyQt4 import QtCore, QtGui
import random



# dataFile = open("data/image.txt", 'w')
#dataFile.close()
def genImageData():
	data = []
	for x in range(0, 4000):
		col = []
		for y in range(0, 4000):
			r = 255 * random.random()
			g = 255 * random.random()
			b = 255 * random.random()
			col += [[r, g, b]]
		data += [col]
	return np.array(data)

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


plot = pqg.plot()
data = genImageData()
image = pqg.ImageItem(image = data)
plot.addItem(image)
levels = [[0, 255] for _ in range(3)]
levels = np.array(levels)