from PyQt4 import QtGui
import os

def getFilePath(caption='', dir='', filter=''):
    """Opens a OS native file browser in Windows / OSX.
    Returns a list of paths to the selected files."""
    f = QtGui.QFileDialog.getOpenFileNames
    return f(caption=caption, directory=dir, filter=filter)


def uniqueName(baseName, baseNum, nameList):
    """Return a new name formed from BASENAME.format(BASENUM) that is not
    in nameList."""
    name = baseName.format(baseNum)
    while name in nameList:
        baseNum += 1
        name = baseName.format(baseNum)
    return name


def shorten_filename(filename):
    f = os.path.split(filename)[1]
    return "%s~%s" % (f[:3], f[-16:]) if len(f) > 19 else f


class GraphException(Exception):
    """A custom exception for the graphing program."""
    def __init__(self, message):
        super(GraphException, self).__init__(message)
        errorBox = QtGui.QMessageBox()
        errorBox.setText(message)
        errorBox.exec_()


class GraphMessage():
    def __init__(self):
        self.messageBox = QtGui.QMessageBox()

    def setMessage(self, message):
        self.messageBox.setText(message)

    def display(self):
        self.messageBox.exec_()
