import time
import math

updatePath = "C:\Users\Ben\Google Drive\QNL\guis\guiExample\graph\update\updateFile.txt"
dataPath = "C:\Users\Ben\Google Drive\QNL\guis\guiExample\graph\update\updateData.txt"

def update(x, y):
	f = open(dataPath, 'a+')
	f.write("{0}	{1}\n".format(x, y))
	f.close()


# Clearing the data file.
g = open(dataPath, 'w')
g.close()

# Writing to the data file and updating the UPDATE file. 
for i in range(10000):
	update(float(i) / 100, 10 * math.sin(float(i) / 100))

	if (i % 100 == 0):
		f = open(updatePath, 'w')
		f.write(str(time.time()) + '\n')
		f.write(dataPath + '\n')
		f.close()
		time.sleep(1)