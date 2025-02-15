# -*- coding: utf-8 -*-
#from curses import keyname
import os
from pickle import TRUE
import sys
from tkinter.tix import ComboBox
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

superType=['superA','superB','superC']
superMOD=['0.8','1','1.5','2','2.5','3','4','5']


# 画面を並べて表示する
class Ui_Dialog(object):

    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 410)
        Dialog.move(1000, 0)


        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 240, 200, 200))
        self.label_6.setText("")
        
        
        
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #形状
        self.label_type = QtGui.QLabel('形状',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 22))
        #モジュール
        self.label_mod = QtGui.QLabel('モジュール',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(110, 35, 100, 22))
        
        
        #歯数
        self.label_N = QtGui.QLabel('歯数',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_N = QtGui.QLineEdit('25',Dialog)
        self.le_N.setGeometry(QtCore.QRect(110, 60, 50, 20))
        self.le_N.setAlignment(QtCore.Qt.AlignCenter)
        #歯幅
        self.label_B = QtGui.QLabel('歯幅',Dialog)
        self.label_B.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_B = QtGui.QLineEdit('15',Dialog)
        self.le_B.setGeometry(QtCore.QRect(110, 85, 50, 20))
        self.le_B.setAlignment(QtCore.Qt.AlignCenter)
        
        #穴径
        self.label_dia = QtGui.QLabel('穴径',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(110, 110, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス径
        self.label_Bdia = QtGui.QLabel('ボス径',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.le_Bdia = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia.setGeometry(QtCore.QRect(110, 135, 50, 20))
        self.le_Bdia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス幅
        self.label_BB = QtGui.QLabel('ボス幅',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_BB = QtGui.QLineEdit('25',Dialog)
        self.le_BB.setGeometry(QtCore.QRect(110, 160, 50, 20))
        self.le_BB.setAlignment(QtCore.Qt.AlignCenter)
         #ウエブ厚
        self.label_WB = QtGui.QLabel('ウエブ厚',Dialog)
        self.label_WB.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.le_WB = QtGui.QLineEdit('9',Dialog)
        self.le_WB.setGeometry(QtCore.QRect(110, 185, 50, 20))
        self.le_WB.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 213, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 210, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('データ読み込み',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 235, 150, 22))


        self.comboBox_type.addItems(superType)
        self.comboBox_type.setEditable(True)
        self.comboBox_mod.addItems(superMOD)
        self.comboBox_mod.setEditable(True)
        

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onShape) 
        self.comboBox_type.setCurrentIndex(0)
        
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onShape)

        self.comboBox_mod.setCurrentText('2')

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "SuperGear", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "作成", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "更新", None))  

    def onShape(self):
        global key
        key=self.comboBox_type.currentText()
        d0=self.le_Bdia.text()
        t0=self.le_Bdia.text()
        if key=='superA':
            self.le_Bdia.hide()
            self.le_BB.hide()
            self.le_WB.hide()
        elif key=='superB' :
            self.le_Bdia.show()
            self.le_BB.show()
            self.le_WB.hide()
        elif key=='superC' :
            self.le_Bdia.show()
            self.le_BB.show()
            self.le_WB.show()    

        fname=key+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    


    def read_data(self):
         #spreadsheet = App.ActiveDocument.getObject(key+'001')
         #Gui.Selection.clearSelection()
         #Gui.Selection.addSelection(spreadsheet)
         selection = Gui.Selection.getSelection()
         
         # Partsグループが選択されているかチェック
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
         key2= spreadsheet.getContents('A2') 
         fname=key2+'.png'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
         self.label_6.setPixmap(QtGui.QPixmap(joined_path))              

         self.comboBox_type.setCurrentText(key2[1:])

         self.comboBox_mod.setCurrentText(spreadsheet.getContents('C2'))
         self.le_N.setText(spreadsheet.getContents('B2'))
         self.le_B.setText(spreadsheet.getContents('D2'))   
         self.le_dia.setText(spreadsheet.getContents('E2'))  
         self.le_Bdia.setText(spreadsheet.getContents('F2'))  
         self.le_BB.setText(spreadsheet.getContents('G2'))  


    
    def update(self):
         # スプレッドシートを選択
         #spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         #Gui.Selection.clearSelection()
         #Gui.Selection.addSelection(spreadsheet)
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
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
                         
         mod=self.comboBox_mod.currentText() 
         #modi=self.comboBox_mod.currentIndex() 
         N=self.le_N.text()
         t=self.le_B.text()
         dia=self.le_dia.text()   
         Bdia=self.le_Bdia.text()  
         BB=self.le_BB.text() 
         WB=self.le_WB.text() 

         if selection:
             for obj in selection:
                 if obj.TypeId == "Spreadsheet::Sheet":
                     # スプレッドシートが見つかった場合の処理
                     spreadsheet = obj
                     dia=self.le_dia.text()
                     spreadsheet.set('A2',key)
                     #spreadsheet.set('A3',str(keyi))
                     spreadsheet.set('B2',N)
                     spreadsheet.set('C2',mod)
                     #spreadsheet.set('C3',str(modi))
                     spreadsheet.set('D2',t)
                     spreadsheet.set('E2',dia)
                     spreadsheet.set('F2',Bdia)
                     spreadsheet.set('G2',BB)
                     spreadsheet.set('H2',WB)

                     App.ActiveDocument.recompute()

    def create(self): 
         fname=key+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Gear_data',fname) 
         #print(joined_path)
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