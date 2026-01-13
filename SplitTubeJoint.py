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

CDia=['40','45','50','55','60','65','70','75','80','85','90','95','100','105',
      '110','115','120','125','130','135','140','145','150','155','160','165','170',]
# D,      d,       D,     L,         A,      B,        C,              E,           F,     G,       H,       S,       BoltNo,      BoltSize
CDim={
'40':(   40,     115,   160,        70,     32,       20,            1.0,         27,     53,      38,      15,         6,           'M12',),
'45':(   45,     127,   180,        76,     36,       22,            1.0,         30,     60,      40,      15,         6,           'M12',),
'50':(   50,     138,   200,        82,     39,       24,            1.0,         33,     67,      43,      18,         6,           'M16',),
'55':(   55,     150,   220,        88,     42,       26,            1.0,         37,     73,      46,      18,         6,           'M16',),
'60':(   60,     162,   240,        96,     46,       28,            1.0,         40,     80,      50,      22,         6,           'M20',),
'65':(   65,     172,   260,       102,     50,       30,            1.5,         43,     87,      52,      22,         6,           'M20',),
'70':(   70,     185,   280,       108,     53,       32,            1.5,         47,     93,      55,      25,         6,           'M22',),
'75':(   75,     195,   300,       114,     56,       35,            1.5,         50,    100,      58,      25,         6,           'M22',),
'80':(   80,     207,   320,       120,     60,       37,            1.5,         53,    107,      60,      28,         6,           'M26',),
'85':(   85,     218,   340,       127,     63,       39,            1.5,         57,    113,      64,      28,         6,           'M26',),
'90':(   90,     230,   360,       134,     68,       41,            1.5,         60,    120,      66,      32,         6,           'M30',),
'95':(   95,     240,   380,       140,     70,       43,            2.0,         63,    127,      70,      32,         6,           'M30',),
'100':( 100,     248,   400,       145,     78,       45,            2.0,         50,    100,      66,      28,         8,           'M26',),
'105':( 105,     248,   400,       145,     78,       45,            2.0,         50,    100,      66,      28,         8,           'M26',),
'110':( 110,     259,   440,       157,     86,       50,            2.0,         55,    110,      71,      32,         8,           'M30',),
'115':( 115,     259,   440,       157,     86,       50,            2.0,         55,    110,      71,      32,         8,           'M30',),
'120':( 120,     279,   480,       170,     93,       54,            2.0,         60,    120,      76,      35,         8,           'M32',),
'125':( 125,     279,   480,       170,     93,       54,            2.0,         60,    120,      76,      35,         8,           'M32',),
'130':( 130,     300,   520,       183,    101,       58,            2.0,         65,    130,      81,      35,         8,           'M32',),
'135':( 135,     300,   520,       183,    101,       58,            2.0,         65,    130,      81,      35,         8,           'M32',),
'140':( 140,     321,   560,       195,    108,       62,            2.0,         70,    140,      86,      38,         8,           'M35',),
'145':( 145,     321,   560,       195,    108,       62,            2.0,         70,    140,      86,      38,         8,           'M35',),
'150':( 150,     341,   600,       207,    116,       66,            2.0,         75,    150,      91,      38,         8,           'M35',),
'155':( 155,     341,   600,       207,    116,       66,            2.5,         75,    150,      91,      38,         8,           'M35',),
'160':( 160,     362,   640,       219,    123,       70,            2.5,         80,    160,      96,      42,         8,           'M38',),
'165':( 165,     362,   640,       219,    123,       70,            2.5,         80,    160,      96,      42,         8,           'M38',),
'170':( 170,     383,   680,       232,    131,       75,            2.5,         85,    170,     101,      45,         8,           'M42',),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 290)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 80, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Joint_data','SplitTubeJoint','SplitTubeJoint.png')
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(50, 13, 150, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(130, 10, 90, 22))
        self.comboBox_dia.setEditable(True)
        self.comboBox_dia.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 38, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(130, 60, 80, 22))


        self.comboBox_dia.addItems(CDia)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Axial coupling", None))
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "nominalDia", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "upDate", None))  

    def update(self):
         # 選択したオブジェクトを取得
         spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         Gui.Selection.clearSelection()
         Gui.Selection.addSelection(spreadsheet)
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
                         #Gui.Selection.addSelection(spreadsheet)
         # 選択したスプレッドシートを取得
         if selection:
             for obj in selection:
                 if obj.TypeId == "Spreadsheet::Sheet":
                     # スプレッドシートが見つかった場合の処理
                     spreadsheet = obj

                     key=self.comboBox_dia.currentText()
                     sa=CDim[key]
                     spreadsheet.set('B2',key)
                     spreadsheet.set('B3',str(sa[0]))#d
                     spreadsheet.set('B4',str(sa[1]))#D
                     spreadsheet.set('B5',str(sa[2]))#L
                     spreadsheet.set('B6',str(sa[3]))#A
                     spreadsheet.set('B7',str(sa[4]))#B
                     spreadsheet.set('B8',str(sa[5]))#C
                     spreadsheet.set('B9',str(sa[6]))#E
                     spreadsheet.set('B10',str(sa[7]))#F
                     spreadsheet.set('B11',str(sa[8]))#G
                     spreadsheet.set('B12',str(sa[9]))#H
                     spreadsheet.set('B13',str(sa[10]))#S
                     spreadsheet.set('B14',str(sa[11]))#BoltNo
                     spreadsheet.set('B15',str(sa[12]))#BoltL
                     App.ActiveDocument.recompute()


    def create(self): 
         fname='SplitTubeJoint.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Joint_data','SplitTubeJoint',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         Gui.ActiveDocument.ActiveView.fitAll()      
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        