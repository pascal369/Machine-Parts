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
from prt_data.CSnap_data import paramCSnap

parts=['グランドパッキン','ランタンリング','グランド押さえ']

S_Width=['3','4','5','6','6.5','8','9.5','10','11','12.5','14.5',
      '16','19','20','22','25']
# D,      min,   max
S_Dim={
'3':(    3,      12, ),
'4':(    4,      20, ),
'5':(    5,      25, ),
'6':(    8,      28, ),
'6.5':(  8,      28, ),
'8':(   12,      50, ),
'9.5':( 18,      70, ),
'10':(  18,      70, ),
'11':(  18,      70, ),
'12.5':(32,     125, ),
'14.5':(32,     125, ),
'16':(  56,     180, ),
'19':(  90,     250, ),
'20':( 125,     250, ),
'22':( 125,     250, ),
'25':( 125,     250, ),
 }

# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 350)
        Dialog.move(1000, 0)


        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 140, 200, 200))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'GlandP_data',"glandpackingAssy.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        #パッキン幅　packing width
        self.label_S = QtGui.QLabel('gland Packing width',Dialog)
        self.label_S.setGeometry(QtCore.QRect(10, 13, 130, 22))
        self.comboBox_S = QtGui.QComboBox(Dialog)
        self.comboBox_S.setGeometry(QtCore.QRect(150, 13, 50, 22))
        self.comboBox_S.listIndex=11
        
        #適用軸径shaft diameter
        self.label_shaftdia = QtGui.QLabel('Applicable shaft dia',Dialog)
        self.label_shaftdia.setGeometry(QtCore.QRect(60, 38, 200, 22))
        #self.label_shaftdia.setText("適用軸径 3～12")
        #軸径
        self.label_dia = QtGui.QLabel('shaft dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_dia = QtGui.QLineEdit(Dialog)
        self.le_dia.setGeometry(QtCore.QRect(150, 63, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(40, 95, 50, 22))
        #インポート
        self.pushButton4 = QtGui.QPushButton('Import',Dialog)
        self.pushButton4.setGeometry(QtCore.QRect(40, 120, 180, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(130, 95, 50, 22))
        self.comboBox_S.addItems(S_Width)

        self.comboBox_S.setCurrentIndex(1)
        self.comboBox_S.currentIndexChanged[int].connect(self.onWidth) 
        self.comboBox_S.setCurrentIndex(0)
        self.le_dia.setText('100')
        QtCore.QObject.connect(self.pushButton4, QtCore.SIGNAL("pressed()"), self.onImport)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Gland packing Assy", None))
        
    def onImport(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.comboBox_S.setCurrentText(spreadsheet.getContents('s0'))  
                         self.le_dia.setText(spreadsheet.getContents('d0'))  

    def onWidth(self):
        global dmin
        global dmax
        global S0
        S0=self.comboBox_S.currentText()
        sa=S_Dim[S0]
        dmin=sa[0]
        dmax=sa[1]
        appDia='Applicable shaft dia'+str(dmin)+'～'+str(dmax)
        self.label_shaftdia.setText(appDia)
        #print(appDia)
        self.le_dia.setText(str(dmin))
        return    
    
    def update(self):
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         dia=self.le_dia.text()
                         S0=self.comboBox_S.currentText()
                         spreadsheet.set('s0',str(S0))
                         spreadsheet.set('d0',dia)
                         App.ActiveDocument.recompute()

    def create(self): 

         fname='glandPackingAssy.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','GlandP_data',fname) 

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