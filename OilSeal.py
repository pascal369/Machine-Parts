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

CDia=['6 16 7','6 22 7','7 22 7','8 22 7','8 24 7','9 22 7','10 22 7','10 25 7','12 24 7','12 25 7',
      '12 30 7','15 26 7','15 30 7','15 35 7','16 30 7','18 30 7','18 35 7','20 35 7','20 40 7',
      '22 35 7','22 40 7','22 47 7','25 40 7','25 45 7','25 47 7','28 40 7','28 47 7','28 52 7','30 42 7',
      '30 47 7','30 50 7','30 52 8','32 45 8','32 47 8','32 52 8','35 50 8','35 52 8','35 55 8','38 55 8',
      '38 58 8','38 62 8','40 55 8','40 62 8','42 55 8','42 62 8','45 62 8','45 65 8','50 68 8',
      '50 72 8','55 72 8','55 80 8','60 80 8','60 85 8','65 85 10','65 90 10','70 90 10','70 95 10',
      '75 95 10','75 100 10','80 100 10','80 110 10','85 110 12','85 120 12','90 115 13','90 120 12','90 120 12',
      '95 120 12','95 120 12','100 125 12','110 140 12','115 145 14','120 150 12','130 160 12','140 170 15','150 180 15',
      '160 190 16','170 200 16']
# D,            d1,      D0,   b0,     
CDim={
'6 16 7': (      6,      16,    7,    ),
'6 22 7': (      6,      22,    7,    ),
'7 22 7': (      7,      22,    7,    ),
'8 22 7': (      8,      22,    7,    ),
'8 24 7': (      8,      24,    7,    ),
'9 22 7': (      9,      22,    7,    ),
'10 22 7':(     10,      22,    7,    ),
'10 25 7':(     10,      25,    7,    ),
'12 24 7':(     12,      24,    7,    ),
'12 25 7':(     12,      25,    7,    ),
'12 30 7':(     12,      30,    7,    ),
'15 26 7':(     15,      26,    7,    ),
'15 30 7':(     15,      30,    7,    ),
'15 35 7':(     15,      35,    7,    ),
'16 30 7':(     16,      30,    7,    ),
'18 30 7':(     18,      30,    7,    ),
'18 35 7':(     18,      35,    7,    ),
'20 35 7':(     20,      35,    7,    ),
'20 40 7':(     20,      40,    7,    ),
'22 35 7':(     22,      35,    7,    ),
'22 40 7':(     22,      40,    7,    ),
'22 47 7':(     22,      47,    7,    ),
'25 40 7':(     25,      40,    7,    ),
'25 45 7':(     25,      45,    7,    ),
'25 47 7':(     25,      47,    7,    ),
'28 40 7':(     28,      40,    7,    ),
'28 47 7':(     28,      47,    7,    ),
'28 52 7':(     28,      52,    7,    ),
'30 42 7':(     30,      42,    7,    ),
'30 47 7':(     30,      47,    7,    ),
'30 50 7':(     30,      50,    7,    ),
'30 52 8':(     30,      52,    8,    ),
'32 45 8':(     32,      45,    8,    ),
'32 47 8':(     32,      47,    8,    ),
'32 52 8':(     32,      52,    8,    ),
'35 50 8':(     35,      50,    8,    ),
'35 52 8':(     35,      52,    8,    ),
'35 55 8':(     35,      55,    8,    ),
'38 55 8':(     38,      55,    8,    ),
'38 58 8':(     38,      58,    8,    ),
'38 62 8':(     38,      62,    8,    ),
'40 55 8':(     40,      55,    8,    ),
'40 62 8':(     40,      62,    8,    ),
'42 55 8':(     42,      55,    8,    ),
'42 62 8':(     42,      62,    8,    ),
'45 62 8':(     45,      62,    8,    ),
'45 65 8':(     45,      65,    8,    ),
'50 68 8':(     50,      68,    8,    ),
'50 72 8':(     50,      72,    8,    ),
'55 72 8':(     55,      72,    8,    ),
'55 80 8':(     55,      80,    8,    ),
'60 80 8':(     60,      80,    8,    ),
'60 85 8':(     60,      85,    8,    ),
'65 85 10':(    65,      85,   10,    ),
'65 90 10':(    65,      90,   10,    ),
'70 90 10':(    70,      90,   10,    ),
'70 95 10':(    70,      95,   10,    ),
'75 95 10':(    75,      95,   10,    ),
'75 100 10':(   75,     100,   10,    ),
'80 100 10':(   80,     100,   10,    ),
'80 110 10':(   80,     110,   10,    ),
'85 110 12':(   85,     110,   12,    ),
'85 120 12':(   85,     120,   12,    ),
'90 115 13':(   90,     115,   13,    ),
'90 120 12':(   90,     120,   12,    ),
'90 120 12':(   90,     120,   12,    ),
'95 120 12':(   95,     120,   12,    ),
'95 120 12':(   95,     120,   12,    ),
'100 125 12':( 100,     125,   12,    ),
'110 140 12':( 110,     140,   12,    ),
'115 145 14':( 115,     145,   14,    ),
'120 150 12':( 120,     150,   12,    ),
'130 160 12':( 130,     160,   12,    ),
'140 170 15':( 140,     170,   15,    ),
'150 180 15':( 150,     180,   15,    ),
'160 190 16':( 160,     190,   16,    ),
'170 200 16':( 170,     200,   16,    ),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 80, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'OilSeal_data',"Oilseal.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominal Dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(50, 13, 150, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(130, 10, 90, 22))
        self.comboBox_dia.setEditable(True)
        self.comboBox_dia.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(35, 40, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(130, 40, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(35, 65, 185, 22))

        self.comboBox_dia.addItems(CDia)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.Import)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "JIS B 2402-1 Oil Seal", None))
        
    def Import(self):
         global spreadsheet
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj  
          
    def update(self):
        
        #                 #Gui.Selection.addSelection(spreadsheet)
        # # 選択したスプレッドシートを取得
        # if selection:
        #     for obj in selection:
        #         if obj.TypeId == "Spreadsheet::Sheet":
        #             # スプレッドシートが見つかった場合の処理
        #             spreadsheet = obj

                     key=self.comboBox_dia.currentText()
                     sa=CDim[key]
                     spreadsheet.set('B1',key)
                     spreadsheet.set('B2',str(sa[0]))#d1
                     spreadsheet.set('B3',str(sa[1]))#D0
                     spreadsheet.set('B4',str(sa[2]))#b0
                     
                     App.ActiveDocument.recompute()

    def create(self): 
         fname='Oilseal.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','OilSeal_data',fname) 
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
        