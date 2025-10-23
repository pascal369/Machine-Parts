# -*- coding: utf-8 -*-
import os
import sys
import Import
import ImportGui
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

CDia=['10','11','12','14','16','18','19','20','22','25','28','30','32','35','37','40','42','45',
      '47','50','52','55','60','62','68','72','75','80','85','90','95','100',
      '110','120','125']
# D,      d3,        t,     b,          a         d0,      a5,            d1,          d2,       m         n
CDim={
'10':(   10.7,      1.0,    1.8,        3.1,     1.2,       3,            10,         10.4,      1.15,      1.5, ),
'11':(   11.8,      1.0,    1.8,        3.2,     1.2,       4,            11,         11.4,      1.15,      1.5, ),
'12':(   13.0,      1.0,    1.8,        3.3,     1.5,       5,            12,         12.5,      1.15,      1.5, ),
'14':(   15.1,      1.0,    2.0,        3.6,     1.7,       7,            14,         14.6,      1.15,      1.5, ),
'16':(   17.3,      1.0,    2.0,        3.7,     1.7,       8,            16,         16.8,      1.15,      1.5, ),
'18':(   19.5,      1.0,    2.5,        4.0,     1.7,      10,            18,         19.0,      1.15,      1.5, ),
'19':(   20.5,      1.0,    2.5,        4.0,     2.0,      11,            19,         20.0,      1.15,      1.5, ),
'20':(   21.5,      1.0,    2.5,        4.0,     2.0,      12,            20,         21.0,      1.15,      1.5, ),
'22':(   23.5,      1.0,    2.5,        4.1,     2.0,      13,            22,         23.0,      1.15,      1.5, ),
'25':(   26.9,      1.2,    3.0,        4.4,     2.0,      16,            25,         26.2,      1.35,      1.5, ),
'28':(   30.1,      1.2,    3.0,        4.6,     2.0,      18,            28,         29.4,      1.35,      1.5, ),
'30':(   32.1,      1.2,    3.0,        4.7,     2.0,      20,            30,         31.4,      1.35,      1.5, ),
'32':(   34.4,      1.2,    3.5,        5.2,     2.5,      21,            32,         33.7,      1.35,      1.5, ),
'35':(   37.8,      1.5,    3.5,        5.2,     2.5,      24,            35,         37.0,      1.65,      1.5, ),
'37':(   39.8,      1.5,    3.5,        5.2,     2.5,      26,            37,         39.0,      1.65,      2.0, ),
'40':(   43.5,      1.75,   4.0,        5.7,     2.5,      28,            40,         42.5,      1.90,      2.0, ),
'42':(   45.5,      1.75,   4.0,        5.8,     2.5,      30,            42,         44.5,      1.90,      2.0, ),
'45':(   48.5,      1.75,   4.5,        5.9,     2.5,      33,            45,         47.5,      1.90,      2.0, ),
'47':(   50.5,      1.75,   4.5,        6.1,     2.5,      34,            47,         49.5,      1.90,      2.0, ),
'50':(   54.2,      2.0,    4.5,        6.5,     2.5,      37,            50,         53.0,      2.20,      2.0, ),
'52':(   56.2,      2.0,    5.1,        6.5,     2.5,      39,            52,         55.0,      2.20,      2.0, ),
'55':(   59.2,      2.0,    5.1,        6.5,     2.5,      41,            55,         58.0,      2.20,      2.0, ),
'60':(   64.2,      2.0,    5.5,        6.8,     2.5,      46,            60,         63.0,      2.20,      2.0, ),
'62':(   66.2,      2.0,    5.5,        6.9,     2.5,      48,            62,         65.0,      2.70,      2.0, ),
'68':(   72.5,      2.5,    6.0,        7.4,     2.5,      53,            68,         71.0,      2.70,      2.5, ),
'72':(   76.5,      2.5,    6.6,        7.4,     2.5,      57,            72,         75.0,      2.70,      2.5, ),
'75':(   79.5,      2.5,    6.6,        7.8,     2.5,      60,            75,         78.0,      2.70,      2.5, ),
'80':(   85.5,      2.5,    7.0,        8.0,     2.5,      64,            80,         83.5,      2.70,      2.5, ),
'85':(   90.5,      3.0,    7.0,        8.0,     3.0,      69,            85,         88.5,      3.20,      3.0, ),
'90':(   95.5,      3.0,    7.6,        8.3,     3.0,      73,            90,         93.5,      3.20,      3.0, ),
'95':(  100.5,      3.0,    8.0,        8.5,     3.0,      77,            95,         98.5,      3.20,      3.0, ),
'100':( 105.5,      3.0,    8.3,        8.8,     3.0,      82,           100,        103.5,      3.20,      3.0, ),
'110':( 117.0,      4.0,    8.9,       10.2,     3.0,      89,           110,        114.0,      4.20,      4.0, ),
'120':( 127.0,      4.0,    9.5,       10.7,     3.0,      98,           120,        124.0,      4.20,      4.0, ),
'125':( 132.0,      4.0,   10.0,       10.7,     3.5,     103,           125,        129.0,      4.20,      4.0, ),
 }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 150, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'CSnap_data',"CSnap_hole.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('Nominal Dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 10, 150, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 8, 95, 22))
        self.comboBox_dia.setEditable(True)
        self.comboBox_dia.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(25, 35, 150, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(25, 60, 150, 22))
        #Import
        self.pushButton4 = QtGui.QPushButton('Import',Dialog)
        self.pushButton4.setGeometry(QtCore.QRect(25, 85, 150, 22))

        #エクスポート
        self.pushButton3 = QtGui.QPushButton('Stp_Export',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(25, 110, 150, 24))
        self.pushButton3.setObjectName("pushButton2")


        self.comboBox_dia.addItems(CDia)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.export_step)
        QtCore.QObject.connect(self.pushButton4, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Snap Ring for hole", None))

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
             self.comboBox_dia.setCurrentText(spreadsheet.getContents('B2'))        

    def export_step(self):
        
        sel = Gui.Selection.getSelection()
        if len(sel) == 0:
            return
        obj = sel[0]
        label=sel[0].Label
        #print(label)
        path = os.path.splitext(obj.Document.FileName)[0] +'_'+label+'.step'
        print(label)
        ImportGui.export([obj],path)

    def update(self):
         # スプレッドシートを選択
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
                    
                         key=self.comboBox_dia.currentText()
                         sa=CDim[key]
                         spreadsheet.set('B2',key)
                         spreadsheet.set('B3',str(sa[0]))#d3
                         spreadsheet.set('B4',str(sa[1]))#t
                         spreadsheet.set('B5',str(sa[2]))#b
                         spreadsheet.set('B6',str(sa[3]))#a
                         spreadsheet.set('B7',str(sa[4]))#d0
                         spreadsheet.set('B8',str(sa[5]))#a5
                         spreadsheet.set('B9',str(sa[6]))#d1
                         spreadsheet.set('B10',str(sa[7]))#d2
                         spreadsheet.set('B11',str(sa[8]))#m
                         spreadsheet.set('B12',str(sa[9]))#n
                     App.ActiveDocument.recompute()

    def create(self): 
         fname='CSnap_hole.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','CSnap_data',fname) 
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