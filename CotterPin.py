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

ODia=['0.6','0.8','1.0','1.2','1.6','2.0','2.5','3.2','4.0','5.0','6.3','8.0']
boltDia={'0.6':('2.5',),
         '0.8':('3.5',),
         '1.0':('4.5',),
         '1.2':('5.5',),
         '1.6':('7',),
         '2.0':('9',),
         '2.5':('11',),
         '3.2':('14',),
         '4.0':('20',),
         '5.0':('27',),
         '6.3':('39',),
         '8.0':('56',)
         }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 250)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 60, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'pin_data',"cotterPin.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominal',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(35, 13, 150, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 10, 80, 22))
        #ワイヤー径
        self.label_wdia = QtGui.QLabel('BoltDia',Dialog)
        self.label_wdia.setGeometry(QtCore.QRect(80, 38, 150, 12))
        self.label_wdia.setStyleSheet("color: black;")
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(13, 60, 85, 22))
        #更新
        self.pushButton3 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(105, 60, 85, 22))
        #インポート
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(200, 60, 85, 22))


        self.comboBox_dia.addItems(ODia)
        self.comboBox_dia.setEditable(True)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia) 
        self.comboBox_dia.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "cotterPin", None))
        
    def onDia(self):
        key=self.comboBox_dia.currentText()
        sa=boltDia[key]
        self.label_wdia.setText('boltDia(max)=  '+sa[0])

    def import_data(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         key=spreadsheet.getContents('A3')[1:]
                         #print(key)
                         self.comboBox_dia.setCurrentText(key)
                         sa=boltDia[key]
                         self.label_wdia.setText('boltDia(max)=  '+sa[0])
        return


    def update(self):
         key=self.comboBox_dia.currentText()
         #print(key)
         for i in range(4,16):
             if key==spreadsheet.getContents('A'+str(i))[1:]:
                 d0=spreadsheet.getContents('B'+str(i))
                 D0=spreadsheet.getContents('C'+str(i))
                 a0=spreadsheet.getContents('D'+str(i))
                 H0=spreadsheet.getContents('E'+str(i))
                 bdia=spreadsheet.getContents('F'+str(i))
                 l0=spreadsheet.getContents('G'+str(i))
                 
                 spreadsheet.set('A3',spreadsheet.getContents('A'+str(i)))
                 spreadsheet.set('B3',str(d0))
                 spreadsheet.set('C3',str(D0))
                 spreadsheet.set('D3',str(a0))
                 spreadsheet.set('E3',str(H0))
                 spreadsheet.set('F3',str(bdia))
                 spreadsheet.set('G3',str(l0))
                 
         App.ActiveDocument.recompute()

    def create(self): 
         dia=self.comboBox_dia.currentText()
         fname='CotterPin.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','pin_data',fname) 
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