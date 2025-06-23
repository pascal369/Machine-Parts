# -*- coding: utf-8 -*-
import os
import sys
import Import
#import ImportGui as Gui
import Spreadsheet
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from prt_data.CSnap_data import paramCSnap


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 200)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(200, 10, 250, 100))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spring_data',"inlet.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #W
        self.label_dia = QtGui.QLabel('Wire_dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.lineEdit_dia = QtGui.QLineEdit('1.6',Dialog)
        self.lineEdit_dia.setGeometry(QtCore.QRect(80, 15, 50, 20))
        self.lineEdit_dia.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_dia.setObjectName("Wire_dia")
        
        #L
        self.label_Pitch = QtGui.QLabel('Pitch',Dialog)
        self.label_Pitch.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.lineEdit_Pitch = QtGui.QLineEdit('2.0',Dialog)
        self.lineEdit_Pitch.setGeometry(QtCore.QRect(80, 35, 50, 20))
        self.lineEdit_Pitch.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_Pitch.setObjectName("Pitch")
        #sita
        self.label_coilDia = QtGui.QLabel('Coil_dia',Dialog)
        self.label_coilDia.setGeometry(QtCore.QRect(10, 63, 150, 12))
        self.lineEdit_coilDia = QtGui.QLineEdit('10.0',Dialog)
        self.lineEdit_coilDia.setGeometry(QtCore.QRect(80, 65, 50, 20))
        self.lineEdit_coilDia.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_coilDia.setObjectName("CoilRa")
        #h
        self.label_Turns = QtGui.QLabel('Turns',Dialog)
        self.label_Turns.setGeometry(QtCore.QRect(10, 88, 150, 12))
        self.lineEdit_Turns = QtGui.QLineEdit('10.0',Dialog)
        self.lineEdit_Turns.setGeometry(QtCore.QRect(80, 85, 50, 20))
        self.lineEdit_Turns.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_Turns.setObjectName("CoilHight")

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 125, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(190, 125, 60, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(100, 125, 60, 22))
        self.pushButton3.setObjectName("pushButton3")
       
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onImport)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "compression coil spring", None))
        
    def onImport(self):
        global spreadsheet
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

                         self.lineEdit_dia.setText(spreadsheet.getContents('Wire_dia'))  
                         self.lineEdit_Pitch.setText(spreadsheet.getContents('Pitch'))  
                         self.lineEdit_coilDia.setText(spreadsheet.getContents('Coil_dia'))  
                         self.lineEdit_Turns.setText(spreadsheet.getContents('Turns')) 
                         #print('bbbbbbbbbbbbbbbb')
    def update(self):
         
         dia=self.lineEdit_dia.text()
         Pitch=self.lineEdit_Pitch.text()
         Coil_dia=self.lineEdit_coilDia.text()
         Turns=self.lineEdit_Turns.text()
         
         try:
            
            spreadsheet.set('B2',dia)
            spreadsheet.set('B3',Pitch)
            spreadsheet.set('B4',Coil_dia)
            spreadsheet.set('B5',Turns)
            App.ActiveDocument.recompute()
         except:
            pass    

    def create(self): 
         fname='CompressionCoilSpring.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Spring_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
            Gui.SendMsgToActiveView("ViewFit")
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)               