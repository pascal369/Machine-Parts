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
from prt_data.RollBrg_data import ParamBallBrg
from prt_data.RollBrg_data import ParamAngulaBallBrg
from prt_data.RollBrg_data import RollingBrg_Data


class Ui_Dialog(object):
  
    def setupUi(self, Dialog):
        global fname
        global joined_path
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 350)
        Dialog.move(1000, 0)
        #和文
        self.pushButton_la = QtGui.QPushButton('JPN Text',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(10, 10, 30, 22))
        self.le_la = QtGui.QLineEdit(Dialog)
        self.le_la.setGeometry(QtCore.QRect(105, 10, 175, 22))
        self.le_la.setAlignment(QtCore.Qt.AlignLeft) 
        #タイプ　Type
        self.label_type = QtGui.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 35, 150, 22))
        self.label_type.setStyleSheet("color: gray;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 35, 200, 22))

        #シリーズ　Series
        self.label_ser = QtGui.QLabel(Dialog)
        self.label_ser.setGeometry(QtCore.QRect(10, 63, 120, 22))
        self.label_ser.setStyleSheet("color: gray;")
        self.comboBox_ser = QtGui.QComboBox(Dialog)
        self.comboBox_ser.setGeometry(QtCore.QRect(80, 63, 80, 22))

        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 90, 150, 12))
        self.label_dia.setStyleSheet("color: gray;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 90, 80, 22))
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 120, 200, 22))

        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 145, 200, 200))
        self.label_5.setAlignment(QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")

        self.comboBox_type.addItems(RollingBrg_Data.BType)
        self.comboBox_ser.addItems(RollingBrg_Data.BSer)
        self.comboBox_dia.addItems(RollingBrg_Data.BDia)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_type.setCurrentIndex(0)
        
        self.comboBox_ser.setCurrentIndex(1)
        self.comboBox_ser.currentIndexChanged[int].connect(self.onSer)
        self.comboBox_ser.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "RollingBearingLib", None))
        self.label_type.setText(QtGui.QApplication.translate("Dialog", "Type", None)) 
        self.label_ser.setText(QtGui.QApplication.translate("Dialog", "Series", None)) 
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "Nominal dia", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None)) 
         
    def japan(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label=obj.Label
        JPN=self.le_la.text()
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN

    def onType(self):
         global type
         type=self.comboBox_type.currentText()
         i=self.comboBox_type.currentIndex()
         self.comboBox_ser.clear()
         if type=='Ball Bearings':
             self.comboBox_ser.addItems(RollingBrg_Data.BSer)
             self.comboBox_ser.show()  
             self.comboBox_dia.show()
         elif type=='Angular Ball Bearings':
             self.comboBox_ser.addItems(RollingBrg_Data.ASer)    
         elif type=='Tapered roller bearings': 
             self.comboBox_ser.hide()  
             self.comboBox_dia.hide()
             #self.comboBox_ser.addItems(RollingBrg_Data.TprSer)
             #return
         #elif type=='Roller Bearings': 
         #    self.comboBox_ser.hide()  
         #    self.comboBox_dia.hide()
         #    self.comboBox_ser.addItems(RollingBrg_Data.CylSer)
         elif type=='Cylindorical Roller Bearings':  
              self.comboBox_ser.hide()  
              self.comboBox_dia.hide()
              self.comboBox_ser.addItems(RollingBrg_Data.CylSer)

         self.le_la.setText(RollingBrg_Data.BType_jpn[i])

         label=type
         pic=label+'.png'  
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data',"RollBrg_data",'png_data',pic)
         self.label_5.setPixmap(QtGui.QPixmap(joined_path))
         print(joined_path)
             
    
    def onSer(self):
         ser=self.comboBox_ser.currentText()
         self.comboBox_dia.clear()
         if type=='Ball Bearings' or type=='Angular Ball Bearings':
             self.comboBox_dia.addItems(RollingBrg_Data.BDia)
         elif type=='Tapered roller bearings': 
             self.comboBox_dia.addItems(RollingBrg_Data.TRDia)
         elif type=='Roller Bearings': 
             self.comboBox_dia.addItems(RollingBrg_Data.ADia)
         elif type=='Cylindorical Roller Bearings':
              self.comboBox_dia.addItems(RollingBrg_Data.CylDia)    
        

    def create(self):  
         key0=self.comboBox_type.currentText()
         dia=self.comboBox_dia.currentText()
         series=self.comboBox_ser.currentText()
         key2=self.comboBox_dia.currentIndex()
         if key0=='Ball Bearings':
              if series=='60': 
                   sa=RollingBrg_Data.Bdim60[dia]
              elif series=='62':
                   sa=RollingBrg_Data.Bdim62[dia]
              elif series=='63':
                   sa=RollingBrg_Data.Bdim63[dia]     
                  
              label='Ballbearing'
              modelNo=sa[5]
              D=sa[1]
              B=sa[2]
              r=sa[3]
              doc=App.activeDocument()              
              try:
                 obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
              except:
                  doc=App.newDocument()
                  obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
              
              obj.addProperty("App::PropertyString",'modelNo','series').modelNo=modelNo  
              obj.addProperty("App::PropertyString",'series','series').series=series
              dia=RollingBrg_Data.BDia
              obj.addProperty("App::PropertyEnumeration",'dia',label).dia=dia 
              
              obj.addProperty("App::PropertyFloat",'D',label).D=D
              obj.addProperty("App::PropertyFloat",'B',label).B=B
              obj.addProperty("App::PropertyFloat",'r',label).r=r
              
              obj.dia=dia[key2] 
              ParamBallBrg.BallBrg(obj)
              obj.ViewObject.Proxy=0
              App.ActiveDocument.recompute()  
              Gui.ActiveDocument.ActiveView.fitAll() 
              return
         elif key0=='Angular Ball Bearings':
              if series=='70': 
                   sa=RollingBrg_Data.Adim70[dia]
              elif series=='72':
                   sa=RollingBrg_Data.Adim72[dia]
              elif series=='73':
                   sa=RollingBrg_Data.Adim73[dia]     

                   
              label='Angular Ball bearing'
              modelNo=sa[5]
              D=sa[1]
              B=sa[2]
              r=sa[3]
              doc=App.activeDocument()              
              try:
                 obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
              except:
                  doc=App.newDocument()
                  obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
              
              obj.addProperty("App::PropertyString",'modelNo','series').modelNo=modelNo  
              obj.addProperty("App::PropertyString",'series','series').series=series
              dia=RollingBrg_Data.BDia
              obj.addProperty("App::PropertyEnumeration",'dia',label).dia=dia 
              
              obj.addProperty("App::PropertyFloat",'D',label).D=D
              obj.addProperty("App::PropertyFloat",'B',label).B=B
              obj.addProperty("App::PropertyFloat",'r',label).r=r
              
              obj.dia=dia[key2] 
              ParamAngulaBallBrg.BallBrg(obj)
              obj.ViewObject.Proxy=0
              App.ActiveDocument.recompute()  
              Gui.ActiveDocument.ActiveView.fitAll() 
              return
         #elif key0=='Roller Bearings' :   
         #     if series=='double-rowoutward':
         #          sa=RollingBrg_Data.TRDia
         #     elif series=='Self-aligning' :
         #          sa=RollingBrg_Data.ADia 
         elif key0=='Tapered roller bearings':
              from prt_data.RollBrg_data import TaperedRollerBrg
              TaperedRollerBrg
                        
         elif key0=='Cylindorical Roller Bearings':
              #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
              from prt_data.RollBrg_data import CylindoricalRollerBrg
              CylindoricalRollerBrg
              return

                  

         fname=series+key0+str(dia)+'.FCStd' 
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','RollBrg_data',fname) 
         try:
             doc=App.activeDocument()
             Gui.ActiveDocument.mergeProject(joined_path)
         except:
             doc=App.newDocument()
             Gui.ActiveDocument.mergeProject(joined_path)    
         App.ActiveDocument.recompute()  
         Gui.ActiveDocument.ActiveView.fitAll()  

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # スクリプトのウィンドウを取得
        #script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint) 
