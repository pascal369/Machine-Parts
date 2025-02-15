# -*- coding: utf-8 -*-
import os
import sys
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from scsft_data import paramscshaft
DEBUG = True # set to True to show debug messages
type=['0_shaft','1_blade']

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 365)
        Dialog.move(1000, 0)

        #type
        self.type= QtGui.QLabel(Dialog)
        self.type.setGeometry(QtCore.QRect(10, 15, 50, 12))
        self.combo_type = QtGui.QComboBox(Dialog)
        self.combo_type.setGeometry(QtCore.QRect(80, 10, 70, 22))
        #screw pitch
        self.pitch = QtGui.QLabel(Dialog)
        self.pitch.setGeometry(QtCore.QRect(10, 40, 80, 12))
        self.le_pitch = QtGui.QLineEdit(Dialog)
        self.le_pitch.setGeometry(QtCore.QRect(80, 35, 69, 20))
        #L
        self.L = QtGui.QLabel(Dialog)
        self.L.setGeometry(QtCore.QRect(10, 65, 50, 12))
        self.le_L = QtGui.QLineEdit(Dialog)
        self.le_L.setGeometry(QtCore.QRect(80, 60, 69, 20))
        #L1
        self.L1 = QtGui.QLabel(Dialog)
        self.L1.setGeometry(QtCore.QRect(10, 90, 50, 12))
        self.le_L1 = QtGui.QLineEdit(Dialog)
        self.le_L1.setGeometry(QtCore.QRect(80, 85, 69, 20))
        #L2
        self.L2 = QtGui.QLabel(Dialog)
        self.L2.setGeometry(QtCore.QRect(10, 115, 50, 12))
        self.le_L2 = QtGui.QLineEdit(Dialog)
        self.le_L2.setGeometry(QtCore.QRect(80, 110, 69, 20))
        #D1
        self.D1 = QtGui.QLabel(Dialog)
        self.D1.setGeometry(QtCore.QRect(10, 140, 50, 12))
        self.le_D1 = QtGui.QLineEdit(Dialog)
        self.le_D1.setGeometry(QtCore.QRect(80, 135, 69, 20))
        #D
        self.D = QtGui.QLabel(Dialog)
        self.D.setGeometry(QtCore.QRect(155, 15, 50, 12))
        self.le_D = QtGui.QLineEdit(Dialog)
        self.le_D.setGeometry(QtCore.QRect(200, 10, 69, 20))
        #d0
        self.d0 = QtGui.QLabel(Dialog)
        self.d0.setGeometry(QtCore.QRect(155, 40, 50, 12))
        self.le_d0 = QtGui.QLineEdit(Dialog)
        self.le_d0.setGeometry(QtCore.QRect(200, 35, 69, 20))
        #d1
        self.d1 = QtGui.QLabel(Dialog)
        self.d1.setGeometry(QtCore.QRect(155, 65, 50, 12))
        self.le_d1 = QtGui.QLineEdit(Dialog)
        self.le_d1.setGeometry(QtCore.QRect(200, 60, 69, 20))
        #l
        self.l = QtGui.QLabel(Dialog)
        self.l.setGeometry(QtCore.QRect(155, 90, 50, 12))
        self.le_l = QtGui.QLineEdit(Dialog)
        self.le_l.setGeometry(QtCore.QRect(200, 85, 69, 20))
        #t
        self.t = QtGui.QLabel(Dialog)
        self.t.setGeometry(QtCore.QRect(155, 115, 50, 12))
        self.le_t = QtGui.QLineEdit(Dialog)
        self.le_t.setGeometry(QtCore.QRect(200, 110, 69, 20))
        #h
        self.h = QtGui.QLabel(Dialog)
        self.h.setGeometry(QtCore.QRect(155, 140, 50, 12))
        self.le_h = QtGui.QLineEdit(Dialog)
        self.le_h.setGeometry(QtCore.QRect(200, 135, 69, 20))

        #checkbox
        self.checkbox = QtGui.QCheckBox(Dialog)
        self.checkbox.setGeometry(QtCore.QRect(80, 155, 150, 22))
        self.checkbox.setObjectName("checkbox")
        #create
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 180, 240, 22))
        self.pushButton.setObjectName("pushButton")

        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setStyleSheet("background-color:#ffffff;");
        self.img.setGeometry(QtCore.QRect(30, 215, 240, 140))
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.retranslateUi(Dialog)

        self.combo_type.addItems(type)

        self.combo_type.setCurrentIndex(1)
        self.combo_type.currentIndexChanged[int].connect(self.on_type)
        self.combo_type.setCurrentIndex(0)

        self.le_pitch.textChanged.connect(self.on_type)
        self.le_L.textChanged.connect(self.on_type)
        self.le_L1.textChanged.connect(self.on_type)
        self.le_L2.textChanged.connect(self.on_type)
        self.le_D1.textChanged.connect(self.on_type)
        self.le_D.textChanged.connect(self.on_type)
        self.le_d0.textChanged.connect(self.on_type)
        self.le_d1.textChanged.connect(self.on_type)
        self.le_l.textChanged.connect(self.on_type)
        self.le_t.textChanged.connect(self.on_type)
        

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.on_create)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Screw shaft", None)) 
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))
        self.type.setText(QtGui.QApplication.translate("Dialog", "type", None))
        self.pitch.setText(QtGui.QApplication.translate("Dialog", "p[mm]", None))
        self.L.setText(QtGui.QApplication.translate("Dialog", "L[mm]", None))
        self.L1.setText(QtGui.QApplication.translate("Dialog", "L1[mm]", None))
        self.L2.setText(QtGui.QApplication.translate("Dialog", "L2[mm]", None))
        self.D1.setText(QtGui.QApplication.translate("Dialog", "D1[mm]", None))
        self.D.setText(QtGui.QApplication.translate("Dialog", "D[mm]", None))
        self.d0.setText(QtGui.QApplication.translate("Dialog", "d0[mm]", None))
        self.d1.setText(QtGui.QApplication.translate("Dialog", "d1[mm]", None))
        self.l.setText(QtGui.QApplication.translate("Dialog", "l[mm]", None))
        self.t.setText(QtGui.QApplication.translate("Dialog", "t[mm]", None))
        self.h.setText(QtGui.QApplication.translate("Dialog", "h[mm]", None))
        self.checkbox.setText(QtGui.QApplication.translate("Dialog", "Right_hand thread", None, ))
        self.le_pitch.setText('300')
        self.le_L.setText('3456') 
        self.le_L1.setText('2650')
        self.le_L2.setText('399') 
        self.le_D1.setText('500')
        self.le_D.setText('165.2')
        self.le_d0.setText('143.2')
        self.le_d1.setText('147')
        self.le_l.setText('148')
        self.le_t.setText('8')

    def on_type(self):
        global key
        global pitch
        global L
        global L1
        global L2
        global D1
        global D
        global d0
        global d1
        global l
        global t
        #global h
        
        key=self.combo_type.currentText()[:1]
        pitch=float(self.le_pitch.text())
        L=float(self.le_L.text())
        L1=float(self.le_L1.text())
        L2=float(self.le_L2.text())
        D1=float(self.le_D1.text())
        D=float(self.le_D.text())
        d0=float(self.le_d0.text())
        d1=float(self.le_d1.text())
        l=float(self.le_l.text())
        t=float(self.le_t.text())
        h=(D1-D)/2
        self.le_h.setText(str(h))
        if key=='0':
            pic='shaft.png'
        elif key=='1':
            pic='blade.png' 
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "scsft_data",pic)
        self.img.setPixmap(QtGui.QPixmap(joined_path))

    def on_create(self):
        if key=='0':
            label='shaft'
        elif key=='1':
            label='blade'
        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        obj.addProperty("App::PropertyString", "key",'shaft').key=key
        obj.addProperty("App::PropertyFloat", "pitch",'shaft').pitch=pitch
        obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
        obj.addProperty("App::PropertyFloat", "L1",'shaft').L1=L1
        obj.addProperty("App::PropertyFloat", "L2",'shaft').L2=L2
        obj.addProperty("App::PropertyFloat", "D1",'shaft').D1=D1
        obj.addProperty("App::PropertyFloat", "D",'shaft').D=D
        obj.addProperty("App::PropertyFloat", "d0",'shaft').d0=d0
        obj.addProperty("App::PropertyFloat", "d1",'shaft').d1=d1
        obj.addProperty("App::PropertyFloat", "l",'shaft').l=l
        obj.addProperty("App::PropertyFloat", "t",'shaft').t=t
        if self.checkbox.isChecked():
            obj.addProperty("App::PropertyBool",'RightHandThread',label).RightHandThread = True
        else:
            obj.addProperty("App::PropertyBool",'RightHandThread',label).RightHandThread = False
        paramscshaft.ScSft(obj) 
        obj.ViewObject.Proxy=0
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
         # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)                 
