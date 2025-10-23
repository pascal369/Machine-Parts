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
parts=['LinkChain','Wheel','LinkChainAssy']
CDia=['6','7','8','9.5','11','13','16','19','22','24','27','30',]
# No,      d,       L,     Bi,     Load[N],       
CDim={
'6':(     6.0,     30,    9,       2600,  ),     
'7':(     7.0,     36,   10,       3430,  ),
'8':(     8.0,     40,   12,       4900,  ),
'9.5':(   9.5,     46,   14,       7350,  ),
'11':(   11.0,     53,   17,       9800,  ),
'13':(   13.0,     62,   20,      14700,  ),
'16':(   16.0,     77,   24,      24500,  ),
'19':(   19.0,     91,   29,      34300,  ),
'22':(   22.0,    106,   34,      44100,  ),
'24':(   24.0,    115,   36,      53900,  ),
'27':(   27.0,    129,   40,      66150,  ),
'30':(   30.0,    144,   45,      83300,  ),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 250)
        Dialog.move(1000, 0)
        
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(240, 0, 200, 250))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('NominalDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 8, 100, 22))
        #パーツ　parts
        self.label_parts = QtGui.QLabel('Parts',Dialog)
        self.label_parts.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.label_parts.setStyleSheet("color: black;")
        self.comboBox_parts = QtGui.QComboBox(Dialog)
        self.comboBox_parts.setGeometry(QtCore.QRect(80, 35, 100, 22))
        #軸径　nominal diameter
        self.label_sdia = QtGui.QLabel('shaftDia',Dialog)
        self.label_sdia.setGeometry(QtCore.QRect(10, 63, 150, 12))
        self.label_sdia.setStyleSheet("color: black;")
        self.le_sdia = QtGui.QLineEdit('30',Dialog)
        self.le_sdia.setGeometry(QtCore.QRect(80, 61, 100, 22))

        #chainLength
        self.label_cL = QtGui.QLabel('chainLength',Dialog)
        self.label_cL.setGeometry(QtCore.QRect(10, 88, 150, 12))
        self.label_cL.setStyleSheet("color: black;")
        self.le_cL = QtGui.QLineEdit('2000',Dialog)
        self.le_cL.setGeometry(QtCore.QRect(80, 85, 100, 22))

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 135, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 160, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 185, 80, 22))

        self.comboBox_dia.addItems(CDia)
        self.comboBox_parts.addItems(parts)

        self.comboBox_parts.setCurrentIndex(1)
        self.comboBox_parts.currentIndexChanged[int].connect(self.onParts)
        self.comboBox_parts.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def onParts(self):
        if self.comboBox_parts.currentText()=='LinkChain':
            fname='LinkChain.png'
        elif self.comboBox_parts.currentText()=='Wheel':
            fname='LinkWheel.png'   
        elif self.comboBox_parts.currentText()=='LinkChainAssy':
            fname='LinkChainAssy.png'     

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Chain_data','LinkChain',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Link Chain", None))

    def read(self):
        global Wheel
        global shtWheel
        global shtLinkAssy
        global shtLink
        global sketch_m
        parts=self.comboBox_parts.currentText()
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label[:11] == "shtLinkAssy":
                         shtLinkAssy = obj
                     elif obj.Label[:8] == "shtWheel":
                         shtWheel = obj   
                     elif obj.Label[:7] == "shtLink":
                         shtLink = obj 
                     elif obj.Label[:5] == "Wheel":
                         Wheel = obj      
                     elif obj.Label[:8]=='sketch_m':
                         sketch_m=obj  

                         if parts=='LinkChain':
                             self.comboBox_dia.setCurrentText(shtLink.getContents('B2'))  
                             self.le_sdia.setText(shtLinkAssy.getContents('d0'))
                         elif parts=='LinkWheel':
                             self.comboBox_dia.setCurrentText(shtWheel.getContents('B2')) 
                             self.le_sdia.setText(shtWheel.getContents('d0'))
                         elif parts=='LinkChainAssy':
                             #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                             self.comboBox_dia.setCurrentText(shtLinkAssy.getContents('B2')) 
                             self.le_sdia.setText(shtWheel.getContents('d0'))  
                             self.le_cL.setText(shtWheel.getContents('d0'))   

                                 
 
    def update(self):
         global L
         global d
         # 選択したオブジェクトを取得
         parts=self.comboBox_parts.currentText()
         key=self.comboBox_dia.currentText()
         sa=CDim[key]
         d=sa[0]
         L=sa[1]
         Bi=sa[2]
         Load=sa[3]
         d0=self.le_sdia.text()
         cL=self.le_cL.text()
         if parts=='LinkChain':
             shtLink.set('B2',key)
             shtLink.set('d',str(d))
             shtLink.set('L',str(L))
             shtLink.set('Bi',str(Bi))
             shtLink.set('Load',str(Load))
         elif parts=='Wheel':
             shtWheel.set('B2',key)
             shtWheel.set('d',str(d))
             shtWheel.set('L',str(L))
             shtWheel.set('Bi',str(Bi))
             shtWheel.set('d0',d0)
         elif parts=='LinkChainAssy':
             shtLinkAssy.set('B2',key)
             shtLinkAssy.set('d',str(d))
             shtLinkAssy.set('L',str(L))
             shtLinkAssy.set('Bi',str(Bi))
             shtLinkAssy.set('d0',d0)    
             shtLinkAssy.set('C0',cL)   

         App.ActiveDocument.recompute()

    def create(self): 
         if self.comboBox_parts.currentText()=='LinkChain':
             fname='LChain.FCStd' 
         elif self.comboBox_parts.currentText()=='Wheel':
             fname='LinkWheel.FCStd' 
         elif self.comboBox_parts.currentText()=='LinkChainAssy':
             fname='LinkChainAssy.FCStd'     

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Chain_data','LinkChain',fname) 
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
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)             