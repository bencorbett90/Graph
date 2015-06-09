from PyQt4 import QtGui, QtCore


class MemoryButton(QtGui.QPushButton):
    def __init__(self, *args, **kw):
        QtGui.QPushButton.__init__(self, *args, **kw)
        self.last_mouse_pos = None

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
        QtGui.QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = event.pos()
        QtGui.QPushButton.mouseReleaseEvent(self, event)

    def get_last_pos(self):
        if self.last_mouse_pos:
            return self.mapToGlobal(self.last_mouse_pos)
        else:
            return None

#button = MemoryButton("Click Me!")

def popup_menu():
    popup = QMenu()
    menu = popup.addMenu("Do Action")

    def _action(check):
        print "Action Clicked!"

    menu.addAction("Action").triggered.connect(_action)                                                             
    popup.exec_(button.get_last_pos())

#button.clicked.connect(popup_menu)