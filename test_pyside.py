from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
class Ui_Dialog(object):
        pass
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 