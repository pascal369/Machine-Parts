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

CDia=['10','12','14','15','16','17','18','20','22','25','28','30','32','35','40','45','50','55','60','65','70','75','80','85','90','95','100',
      '105','110','115','120','125','130','135','140','145','150','155','160','165','170','175']
# D,      dia3,   thick_t0, width_b,     dia4,     dia0,    length_a,        length_a1,    length_c
CDim={
'10':(    9.30,      1.0,    1.6,        11.70,     1.2,       3.0,            1.50,         0.40),
'12':(   11.10,      1.0,    1.8,        13.80,     1.5,       3.2,            1.60,         0.45),
'14':(   12.90,      1.0,    2.0,        15.90,     1.7,       3.4,            1.70,         0.50),
'15':(   13.80,      1.0,    2.1,        16.95,     1.7,       3.5,            1.75,         0.52),
'16':(   14.70,      1.0,    2.2,        18.00,     1.7,       3.6,            1.80,         0.55),
'17':(   15.70,      1.0,    2.2,        19.00,     1.7,       3.7,            1.85,         0.55),
'18':(   16.50,      1.0,    2.6,        20.40,     1.7,       3.8,            1.90,         0.65),
'20':(   18.50,      1.2,    2.7,        22.55,     2.0,       3.9,            1.95,         0.67),
'22':(   20.50,      1.2,    2.7,        24.55,     2.0,       4.1,            2.05,         0.67),
'25':(   23.20,      1.2,    3.1,        27.85,     2.0,       4.3,            2.15,         0.77),
'28':(   25.90,      1.6,    3.1,        30.55,     2.0,       4.6,            2.30,         0.78),
'30':(   27.90,      1.6,    3.5,        33.15,     2.0,       4.8,            2.40,         0.88),
'32':(   29.60,      1.6,    3.5,        34.85,     2.5,       5.0,            2.50,         0.88),
'35':(   32.20,      1.6,    4.0,        38.20,     2.5,       5.4,            2.70,         1.00),
'40':(   37.00,      1.8,    4.5,        43.75,     2.5,       5.8,            2.90,         1.13),
'45':(   41.50,      1.8,    4.8,        48.70,     2.5,       6.3,            3.15,         1.20),
'50':(   45.80,      2.0,    5.0,        53.30,     2.5,       6.7,            3.35,         1.25),
'55':(   50.80,      2.0,    5.0,        58.30,     2.5,       7.0,            3.50,         1.25),
'60':(   55.80,      2.0,    5.5,        64.05,     2.5,       7.2,            3.60,         1.38),
'65':(   60.80,      2.5,    6.4,        70.40,     3.0,       7.4,            3.70,         1.60),
'70':(   65.50,      2.5,    6.4,        75.10,     3.0,       7.8,            3.90,         1.60),
'75':(   70.50,      2.5,    7.0,        81.00,     3.0,       7.9,            3.95,         1.75),
'80':(   74.50,      2.5,    7.4,        85.60,     3.0,       8.2,            4.10,         1.85),
'85':(   79.50,      2.5,    8.0,        91.50,     3.0,       8.4,            4.20,         2.00),
'90':(   84.50,      3.0,    8.0,        96.50,     3.0,       8.7,            4.35,         2.00),
'95':(   89.50,      3.0,    8.6,       102.40,     3.0,       9.1,            4.55,         2.15),
'100':(  94.50,      3.0,    9.0,       108.00,     3.0,       9.5,            4.75,         2.25),
'105':(  98.00,      4.0,    9.5,       112.25,     3.0,       9.8,            4.90,         2.38),
'110':( 103.00,      4.0,    9.5,       117.25,     3.0,      10.0,            5.00,         2.38),
'115':( 108.00,      4.0,    9.5,       122.25,     3.0,      10.5,            5.25,         2.58),
'120':( 113.00,      4.0,   10.3,       128.45,     3.0,      10.9,            5.45,         2.58),
'125':( 118.00,      4.0,   10.3,       133.45,     3.5,      11.3,            5.65,         2.58),
'130':( 123.00,      4.0,   11.0,       139.50,     3.5,      11.5,            5.75,         2.75),
'135':( 128.00,      4.0,   11.0,       144.50,     3.5,      11.5,            5.75,         2.75),
'140':( 133.00,      4.0,   11.0,       149.50,     3.5,      11.8,            5.90,         2.75),
'145':( 138.00,      4.0,   11.6,       155.40,     3.5,      11.8,            5.90,         2.90),
'150':( 142.00,      4.0,   11.6,       159.40,     3.5,      12.3,            6.15,         2.90),
'155':( 146.00,      4.0,   12.2,       164.30,     3.5,      12.7,            6.35,         3.05),
'160':( 151.00,      4.0,   12.2,       169.30,     3.5,      12.9,            6.45,         3.05),    
'165':( 155.50,      4.0,   12.9,       174.35,     3.5,      13.1,            6.55,         2.23),    
'170':( 160.50,      4.0,   12.9,       179.35,     3.5,      13.1,            6.55,         2.23),    
'175':( 165.50,      4.0,   12.9,       184.35,     3.5,      13.1,            6.55,         2.23),    
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 110, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'CSnap_data',"CSnap_shaft.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('Nominal',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 8, 150, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 8, 90, 22))
        self.comboBox_dia.setEditable(True)
        self.comboBox_dia.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(105, 60, 80, 22))
        #Import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(10, 85, 185, 22))


        self.comboBox_dia.addItems(CDia)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Snap Ring", None))
        
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
                        
    def update(self):
         # スプレッドシートを選択
        #selection = Gui.Selection.getSelection()
        #if selection:
        #    selected_object = selection[0]
        #    if selected_object.TypeId == "App::Part":
        #        parts_group = selected_object
        #        for obj in parts_group.Group:
        #            if obj.TypeId == "Spreadsheet::Sheet":
        #                spreadsheet = obj
         key=self.comboBox_dia.currentText()
         #print(key)
         sa=CDim[key]
         spreadsheet.set('B2',key)
         spreadsheet.set('B3',str(sa[0]))
         spreadsheet.set('B4',str(sa[1]))
         spreadsheet.set('B5',str(sa[2]))
         spreadsheet.set('B6',str(sa[3]))
         spreadsheet.set('B7',str(sa[4]))
         spreadsheet.set('B8',str(sa[5]))
         spreadsheet.set('B9',str(sa[6]))
         spreadsheet.set('B10',str(sa[7]))
        #D=self.comboBox_dia.currentText()
            #st='d'+str(D)
            #label=obj.Label
            #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            #obj.addProperty("App::PropertyString", 'Standard','Standard').Standard=st   
         App.ActiveDocument.recompute()

    def create(self): 
         fname='CSnap_shaft.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','CSnap_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         App.ActiveDocument.recompute() 



         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
                            