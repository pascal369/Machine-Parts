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
#from prt_data.CSnap_data import paramCSnap

CDia=['10x80x50','10x100x50','10x110x50','10x120x50',]
# D,               d       L     H    
CDim={
'10x80x50': (     10,     80,   50),
'10x100x50': (    10,    100,   50),
'10x110x50': (    10,    110,   50),
'10x120x50': (    10,    120,   50),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 80, 200, 200))
        self.label_6.setText("aaa")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 8, 90, 22))
        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 35, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 60, 80, 22))

        self.comboBox_dia.addItems(CDia)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_dia.setCurrentIndex(0)

        #QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Handle", None))
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "nominalDia", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "upDate", None))  
    
    def on_type(self):
        type=self.comboBox_dia.currentText()
        #print(type)
        pic='Handle.png'
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Handle_data',pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

    def update(self):
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label == "Spreadsheet":
                         spreadsheet = obj
                         key=self.comboBox_dia.currentText()
                         sa=CDim[key]
                         spreadsheet.set('B1',key)
                         spreadsheet.set('B2',str(sa[0]))#A0
                         spreadsheet.set('B3',str(sa[1]))#B0
                         spreadsheet.set('B4',str(sa[2]))#H0
                         App.ActiveDocument.recompute()

    def create(self): 

         fname='Handle.FCStd'    
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Handle_data',fname) 
         doc=App.newDocument()
         Gui.ActiveDocument.mergeProject(joined_path)
        

         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        