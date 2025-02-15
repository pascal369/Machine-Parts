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
Type=['Outer Link','Inner Link','Offset Link','SprocketA','SprocketB','SprocketC']
nominalDia=['25','35','40','50','60','80','100','120','140','160','180','200','240',]
# D,      Pich,        h0,     t0,         W0,        d,      d2,     h1     
RDim={
'25':(     6.350,      5.05,   0.75,       3.18,     2.31,    3.30,   5.84),
'35':(     9.525,      7.80,   1.25,       4.78,     3.59,    5.08,   9.00),
'40':(    12.700,     10.40,   1.50,       7.95,     3.97,    7.92,  12.00),
'50':(    15.875,     13.00,   2.00,       9.53,     5.09,   10.16,  15.00),
'60':(    19.050,     15.60,   2.40,      12.70,     5.96,   11.91,  18.10),
'80':(    25.400,     20.80,   3.20,      15.88,     7.94,   15.88,  24.10),
'100':(   31.750,     26.00,   4.00,      19.05,     9.54,   19.05,  30.10),
'120':(   38.100,     31.20,   4.80,      25.40,    11.11,   22.23,  36.20),
'140':(   44.450,     36.40,   5.60,      25.40,    12.71,   25.40,  42.20),
'160':(   50.800,     41.60,   6.40,      31.75,    14.29,   28.58,  48.20),
'180':(   57.150,     46.80,   7.15,      35.72,    17.46,   35.71,  54.20),
'200':(   63.500,     52.00,   8.00,      38.10,    19.85,   39.68,  60.30),
'240':(   76.200,     62.40,   9.50,      47.63,    23.81,   47.63,  72.40),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 145)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(180, 10, 150, 100))
        self.label_6.setText("")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('NominalDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 10, 110, 22))
        #タイプ　Type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 35, 110, 22))

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 60, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 85, 80, 22))

        self.comboBox_dia.addItems(nominalDia)
        self.comboBox_type.addItems(Type)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_type.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Roller Chain", None))
    def on_type(self):
        type=self.comboBox_type.currentText()
        print(type)
        if type=='Outer Link':
            pic='OuterLink.png'
        elif type=='Inner Link':
            pic='InnerLink.png'
        elif type=='Offset Link':
            pic='OffsetLink.png'  
        elif type=='SprocketA':
            pic='sproA.png' 
        elif type=='SprocketB':
            pic='sproB.png'         
        elif type=='SprocketC':
            pic='sproC.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Chain_data','RollerChain',pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

    def update(self):
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         key=self.comboBox_dia.currentText()
                         sa=RDim[key]
                         spreadsheet.set('B2',key)
                         spreadsheet.set('B3',str(sa[0]))#pitch
                         spreadsheet.set('B4',str(sa[1]))#h0
                         spreadsheet.set('B5',str(sa[2]))#t0
                         spreadsheet.set('B6',str(sa[3]))#w0
                         spreadsheet.set('B7',str(sa[4]))#d
                         spreadsheet.set('B8',str(sa[5]))#d2
                         spreadsheet.set('B9',str(sa[6]))#h1

                         App.ActiveDocument.recompute()

    def create(self): 
         type=self.comboBox_type.currentText()
         if type=='Outer Link':
             fname='OuterLink.FCStd'
         elif type=='Inner Link':
             fname='InnerLink.FCStd'
         elif type=='Offset Link':
             fname='OffsetLink.FCStd'    
         elif type=='SprocketA':
             fname='sprocket_A.FCStd' 
         elif type=='SprocketB':
             fname='sprocket_B.FCStd'  
         elif type=='SprocketC':
             fname='sprocket_C.FCStd'       
         
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Chain_data','RollerChain',fname) 

         try:
            doc=App.activeDocument()
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