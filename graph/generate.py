import numpy as np
import math
import pyqtgraph as pq4
import random
import h5py
import time
import datetime


def genImageData():
    data = np.zeros((100, 1000, 1000))
    w = 2 * math.pi / 100
    scale = (250 * (2**.5)) / 3
    print('calculating radius')
    for xi in range(0, 1000):
        x = xi - 500
        for yi in range(0, 1000):
            y = yi - 500
            r = math.hypot(x, y)
            data[:, xi, yi] = r / scale
    print('taking sinc')
    data = 100 * np.sinc(data)
    print('multiplying by cos(w t)')
    for t in range(100):
        data[t, ...] *= math.cos(w * t)
    return data

def genImageData2():
    data = np.zeros((10, 10, 10, 10, 10, 10, 10, 10, 10))
    items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    w = math.pi / 5.0
    for a in items:
        A = math.exp(a)
        for b in items:
            B = math.cos(b * w)
            print(10 * a + b)
            for c in items:
                C = c * c
                for d in items:
                    D = 1+d
                    for e in items:
                        E = math.tan(e * w)
                        for f in items:
                            F = math.exp(-f * f)
                            for g in items:
                                G = math.tan(g * w)
                                for h in items:
                                    H = h**g
                                    for i in items:
                                        I = 1+i
                                        data[a][b][c][d][e][f][g][h][i] = A*B*C/D + E*F*H/I
    return data

def genLargeImage():
    data = np.zeros((10001, 10001))
    w = math.pi / 500
    print('starting x')
    for xIndex in xrange(10001):
        x = (xIndex - 5000) * w
        f = math.tan(x) * math.exp((x**3) / 50000)
        data[xIndex, :] = f
    print("done with x")
    for yIndex in xrange(10001):
        y = (yIndex - 5000) * w
        f = math.cos(y) / (.1 + (math.sin(y)**2))
        data[:, yIndex] *= f
    print('done with y')
    return data

def genColorTest():
    data = np.zeros((255, 255, 255, 3))
    for r in range(255):
        data[r, :, :, 0] = r
    for g in range(255):
        data[:, g, :, 1] = g
    for b in range(255):
        data[:, :, b, 2] = b
    return data

def genImageRandom():
    data = genImageData()
    data += np.random.normal(0, 1, size=data.shape)
    return data

def saveData(path, data, args):
    f = h5py.File(path, 'w')
    dset = f.create_group("Dataset0")
    dset.attrs['Name'] = 'Dataset 0'
    dset.attrs['Type'] = 'Dataset'
    dset.attrs['Description'] = 'Color test.'
    dset.attrs['Timestamp'] = time.time()
    dset.attrs['Date Created'] = str(datetime.datetime.now())
    dset.attrs['Comments'] = [
        (str(datetime.datetime.now()), 'Ben Corbett', 'parameters test')]

    val = dset.create_dataset("Dependent0", data=data)
    val.attrs['Name'] = 'Function'
    val.attrs['Units'] = 'meters'
    
    index = 0
    argNames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for arg in args:
        name = "Independent{}".format(index)
        ind = dset.create_dataset(name, data=arg)
        ind.attrs['Name'] = argNames[index]
        ind.attrs['Units'] = 'm'
        val.dims.create_scale(ind)
        val.dims[index].attach_scale(ind)
        index += 1

    f.close()


data = genImageRandom()
w = 2 * math.pi / 100
t = np.array([w * i for i in range(100)])
x = np.array([i-500 for i in range(1000)])
args = [t, x, x]
path = "graph/data/random.hdf5"
print("Saving...")
saveData(path, data, args)
print('Done')
