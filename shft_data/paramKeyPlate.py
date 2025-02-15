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
        Dialog.resize(200, 280)
        Dialog.move(900, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 80, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'shft_data',"keyPlate.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominalDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 80, 12))
        self.le_dia = QtGui.QLineEdit('30',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(80, 10, 90, 22))
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 35, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 60, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 85, 80, 22))

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "KeyPlate", None))
        
    def update(self):
         # スプレッドシートを選択
         spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         Gui.Selection.clearSelection()
         Gui.Selection.addSelection(spreadsheet)
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj
                         #Gui.Selection.clearSelection()
                         Gui.Selection.addSelection(spreadsheet)
         # 選択したスプレッドシートを取得
         if selection:
             for obj in selection:
                 if obj.TypeId == "Spreadsheet::Sheet":
                     # スプレッドシートが見つかった場合の処理
                     spreadsheet = obj
                     dia=self.le_dia.currentText()
                     for i in range(3,10):
                         if dia<'B'+str(i):
                             break
                     spreadsheet.set('B2',dia)
                     spreadsheet.set('C2','C'+str(i))
                     spreadsheet.set('D2','D'+str(i))
                     spreadsheet.set('E2','E'+str(i))
                     spreadsheet.set('F2','F'+str(i))
                     spreadsheet.set('G2','G'+str(i))
                     spreadsheet.set('H2','H'+str(i))
                     spreadsheet.set('I2','I'+str(i))
                     spreadsheet.set('J2','J'+str(i))
                     spreadsheet.set('K2','K'+str(i))
                     
                     
                     App.ActiveDocument.recompute()
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
                     print(obj.Label)
                     if obj.Label=='Spring_washer_general':
                         washer=obj
                     elif obj.Label=='hexagon_bolt':
                         bolt=obj    
                     elif obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
    
                         self.le_dia.setText(spreadsheet.getContents('dia'))
                         self.combo_blt.setCurrentText(spreadsheet.getContents('size')[1:])
                         self.le_t.setText(spreadsheet.getContents('t0')) 
    def create(self): 
         #global fname
         #global joined_path
         fname='keyPlate.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'shft_data',fname) 
         print(fname)
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