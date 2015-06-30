import numpy as np
import math
import pyqtgraph as pq4
import random
import h5py




def genImageData():
    data = np.zeros((400, 400, 400))
    for t in range(0, 400):
        for xi in range(0, 400):
            for yi in range(0, 400):
                x = xi - 200
                y = yi - 200
                phase = t * math.pi / 200
                phase -= math.hypot(x, y) * math.pi / (50 * 2**.5)
                data[t][xi][yi] = 255.0 * math.cos(phase)
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
x = np.array([i for i in range(400)])
y = np.array([i for i in range(400)])
t = np.array([i for i in range(400)])
f = h5py.File('graph/data/vidTest2.hdf5', 'w')
f.create_dataset('vals', data=data)
f.create_dataset('args/t', data=t)
f.create_dataset('args/x', data=x)
f.create_dataset('args/y', data=y)
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