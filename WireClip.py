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

ODia=['8','9','10','12','14','16','18','20','22',]
wireDia={'8':('8',),
         '9':('9',),
         '10':('10',),
         '12':('12.5',),
         '14':('14',),
         '16':('16',),
         '18':('18',),
         '20':('20',),
         '22':('22.4')}

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 320)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 100, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'WireRope',"WireClip.png")
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
        self.label_wdia.setGeometry(QtCore.QRect(80, 38, 150, 12))
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 60, 22))
        #更新
        self.pushButton3 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(105, 60, 60, 22))
        #インポート
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(200, 60, 60, 22))


        self.comboBox_dia.addItems(ODia)
        self.comboBox_dia.setEditable(True)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia) 
        self.comboBox_dia.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "シンブル", None))
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "呼び径", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "作成", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "更新", None))  
    def onDia(self):
        key=self.comboBox_dia.currentText()
        sa=wireDia[key]
        self.label_wdia.setText('wireDia(max)=  '+sa[0])

    def import_data(self):
        global spreadsheet
        global nut
        global All_screw
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label[:11]=='hexagon_nut':
                         nut=obj
                     elif obj.Label[:9]=='All_screw':
                         All_screw=obj    
                     elif obj.Label[:7] == "shtClip":
                         spreadsheet = obj

                         key=spreadsheet.getContents('B27')
                         self.comboBox_dia.setCurrentText(key)
                         sa=wireDia[key]
                         self.label_wdia.setText('wireDia(max)=  '+sa[0])


    def update(self):
         key=self.comboBox_dia.currentText()
         for i in range(28,41):
             if key==spreadsheet.getContents('B'+str(i)):
                 cld=spreadsheet.getContents('A'+str(i))
                 clA=spreadsheet.getContents('C'+str(i))
                 clB=spreadsheet.getContents('D'+str(i))
                 clC=spreadsheet.getContents('E'+str(i))
                 clD=spreadsheet.getContents('F'+str(i))
                 clE=spreadsheet.getContents('G'+str(i))
                 clG1=spreadsheet.getContents('H'+str(i))
                 clr=spreadsheet.getContents('I'+str(i))
                 clbolt=spreadsheet.getContents('J'+str(i))
                 #print(clbolt)
                 db=spreadsheet.getContents('K'+str(i)) 
                 clL=spreadsheet.getContents('L'+str(i)) 
                 clS=spreadsheet.getContents('M'+str(i)) 
                 cln=spreadsheet.getContents('N'+str(i)) 
                 cll=spreadsheet.getContents('O'+str(i)) 
                 spreadsheet.set('B27',key)
                 spreadsheet.set('A27',str(cld))
                 spreadsheet.set('C27',str(clA))
                 spreadsheet.set('D27',str(clB))
                 spreadsheet.set('E27',str(clC))
                 spreadsheet.set('F27',str(clD))
                 spreadsheet.set('G27',str(clE))
                 spreadsheet.set('H27',str(clG1))
                 spreadsheet.set('I27',str(clr))
                 spreadsheet.set('J27',str(clbolt))
                 spreadsheet.set('K27',str(db))
                 spreadsheet.set('L27',str(clL))
                 spreadsheet.set('M27',str(clS))
                 spreadsheet.set('N27',str(cln))
                 spreadsheet.set('O27',str(cll))
         #print(nut.dia)  
         nut.dia=spreadsheet.getContents('J27')[1:]
         All_screw.dia=spreadsheet.getContents('J27')[1:]    
         App.ActiveDocument.recompute()

    def create(self): 
         dia=self.comboBox_dia.currentText()
         fname='WireClip.FCStd'
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