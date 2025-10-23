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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 305)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 120, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'shft_data',"keyPlate.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominalDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 160, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.le_dia = QtGui.QLineEdit('30',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(80, 10, 90, 22))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter) 
        #軸長　
        self.label_L = QtGui.QLabel('shaftLength',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 38, 160, 22))
        self.label_L.setStyleSheet("color: black;")
        self.le_L = QtGui.QLineEdit('50',Dialog)
        self.le_L.setGeometry(QtCore.QRect(80, 35, 90, 22))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter) 
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 60, 90, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 85, 90, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 110, 90, 22))

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "KeyPlate", None))
        
    def read_data(self):
         global washer
         global bolt
         global spreadsheet
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label=='Spring_washer_general':
                         washer=obj
                     elif obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
    
                         self.le_dia.setText(spreadsheet.getContents('dia'))
                         self.le_L.setText(spreadsheet.getContents('L')) 
    def update(self):
         dia=self.le_dia.text()
         L=self.le_L.text()
         cell_value = spreadsheet.getContents('A3')
         for i in range(3,10):
              cell_value = spreadsheet.getContents('B'+str(i))
              if float(dia) <= float(cell_value):
                break
         a=spreadsheet.getContents('C'+str(i))  
         b=spreadsheet.getContents('D'+str(i))
         c=spreadsheet.getContents('E'+str(i))
         d=spreadsheet.getContents('F'+str(i))
         e=spreadsheet.getContents('G'+str(i))
         f=spreadsheet.getContents('H'+str(i))
         g=spreadsheet.getContents('I'+str(i))
         h=spreadsheet.getContents('J'+str(i))  
         n=spreadsheet.getContents('K'+str(i))
         
         spreadsheet.set('A2',L)    
         spreadsheet.set('B2',dia)
         spreadsheet.set('C2',a)
         spreadsheet.set('D2',b)
         spreadsheet.set('E2',c)
         spreadsheet.set('F2',d)
         spreadsheet.set('G2',e)
         spreadsheet.set('H2',f)
         spreadsheet.set('I2',g)
         spreadsheet.set('J2',h)
         spreadsheet.set('K2',n)
                
            
         App.ActiveDocument.recompute()

    def create(self): 
        
         fname='keyPlate.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'shft_data',fname) 
        
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            