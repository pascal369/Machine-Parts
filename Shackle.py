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

ODia=['6','8','10','12','16','20',]
wireDia={'6':('8',),
         '8':('10',),
         '10':('14',),
         '12':('16',),
         '16':('22.4',),
         '20':('28',),
         }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 320)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 115, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'WireRope',"shackle.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominal',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 10, 80, 22))
        #ワイヤー径
        self.label_wdia = QtGui.QLabel('WireDia',Dialog)
        self.label_wdia.setGeometry(QtCore.QRect(80, 38, 160, 12))

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 60, 50, 22))
        #更新
        self.pushButton3 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(150, 60, 50, 22))
        #インポート
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(60, 85, 180, 22))


        self.comboBox_dia.addItems(ODia)
        self.comboBox_dia.setEditable(True)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia) 
        self.comboBox_dia.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Shackle", None))

    def onDia(self):
        key=self.comboBox_dia.currentText()
        sa=wireDia[key]
        self.label_wdia.setText('wireDia(max)=  '+sa[0])

    def import_data(self):
        global Bolt
        global Nut
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.Label[:18] == "SpreadsheetShackle":
                         spreadsheet = obj
                     elif obj.Label[:4] == "Bolt":
                         Bolt = obj  
                     elif obj.Label[:3] == "Nut":
                         Nut = obj      

                         key=spreadsheet.getContents('B2')
                         self.comboBox_dia.setCurrentText(key)
                         sa=wireDia[key]
                         self.label_wdia.setText('wireDia(max)=  '+sa[0])
        return

    def update(self):
         key=self.comboBox_dia.currentText()
         for i in range(3,12):
             if key==spreadsheet.getContents('B'+str(i)):
                 wdia=spreadsheet.getContents('A'+str(i))
                 d0=spreadsheet.getContents('C'+str(i))
                 B0=spreadsheet.getContents('D'+str(i))
                 D0=spreadsheet.getContents('E'+str(i))
                 d1=spreadsheet.getContents('F'+str(i))
                 l1=spreadsheet.getContents('G'+str(i))
                 l2=spreadsheet.getContents('H'+str(i))
                 r1=spreadsheet.getContents('I'+str(i))
                 bolt=spreadsheet.getContents('J'+str(i))
                 
                 spreadsheet.set('B2',key)
                 spreadsheet.set('A2',str(wdia))
                 spreadsheet.set('C2',str(d0))
                 spreadsheet.set('D2',str(B0))
                 spreadsheet.set('E2',str(D0))
                 spreadsheet.set('F2',str(d1))
                 spreadsheet.set('G2',str(l1))
                 spreadsheet.set('H2',str(l2))
                 spreadsheet.set('I2',str(r1))
                 spreadsheet.set('J2',str(bolt))
         Bolt.dia=spreadsheet.getContents('J2')[1:]  
         Nut.dia=spreadsheet.getContents('J2')[1:] 
               
         App.ActiveDocument.recompute()

    def create(self): 
         dia=self.comboBox_dia.currentText()
         fname='ShackleSB.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','WireRope',fname) 
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