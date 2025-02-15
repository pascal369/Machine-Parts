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
from prt_data.BallBrg_data import ParamBallBrg
from prt_data.BallBrg_data import BearingData


class Ui_Dialog(object):
  
    def setupUi(self, Dialog):
        global fname
        global joined_path
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 300)
        Dialog.move(1000, 0)
        #タイプ　Type
        self.label_type = QtGui.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 200, 22))

        #シリーズ　Series
        self.label_ser = QtGui.QLabel(Dialog)
        self.label_ser.setGeometry(QtCore.QRect(10, 38, 120, 12))
        self.comboBox_ser = QtGui.QComboBox(Dialog)
        self.comboBox_ser.setGeometry(QtCore.QRect(80, 35, 80, 22))

        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 63, 150, 12))
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 60, 80, 22))
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 100, 200, 22))

        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 125, 200, 150))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.comboBox_type.addItems(BearingData.BType)
        self.comboBox_ser.addItems(BearingData.BSer)
        self.comboBox_dia.addItems(BearingData.BDia)
        
        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia)
        self.comboBox_dia.setCurrentIndex(0)

        self.comboBox_ser.setCurrentIndex(1)
        self.comboBox_ser.currentIndexChanged[int].connect(self.onSer)
        self.comboBox_ser.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "BallBearingLib", None))
        self.label_type.setText(QtGui.QApplication.translate("Dialog", "Type", None)) 
        self.label_ser.setText(QtGui.QApplication.translate("Dialog", "Series", None)) 
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "Nominal dia", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
    def onSer(self):
         
         return
         
    def onDia(self):
         global key0
         global series
         global label
         key0=self.comboBox_type.currentIndex()
         series=self.comboBox_ser.currentText()
         dia=self.comboBox_dia.currentText()
         #print(dia)
         if key0==0:
              label='単列深溝玉軸受'
         #print(dia4)
         pic=label+'.png'  
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, "BallBrg_data",'png_data',pic)
         #print(joined_path)
         self.label_5.setPixmap(QtGui.QPixmap(joined_path))

    def create(self): 
         return
         #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')   
         dia=self.comboBox_dia.currentText()
         series=self.comboBox_ser.currentText()
         key2=self.comboBox_dia.currentIndex()
         if key0==0:
              if series=='60': 
                   sa=BearingData.Bdim60[dia]
              elif series=='62':
                   sa=BearingData.Bdim62[dia]
                   
              #label='BallBearig_'+sa[5]
              label='Ballbearing'
              modelNo=sa[5]
              
              #print(series)   
                  
              doc=App.activeDocument()              
              #label=self.comboBox_type.currentText()+self.comboBox_dia.currentText()
              #print(label)
              try:
                 obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

              except:
                 doc=App.newDocument()
                 obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

              obj.addProperty("App::PropertyString",'modelNo','series').modelNo=modelNo  

              obj.addProperty("App::PropertyString",'series','series').series=series
              obj.series=series
              i=self.comboBox_ser.currentIndex()
              obj.series=series[i] 

              dia=BearingData.BDia
              obj.addProperty("App::PropertyEnumeration",'dia',label) 
              obj.dia=dia
              i=self.comboBox_dia.currentIndex()
              obj.dia=dia[i] 
           
              ParamBallBrg.BallBrg(obj)
              obj.ViewObject.Proxy=0
              App.ActiveDocument.recompute()  
              Gui.ActiveDocument.ActiveView.fitAll()    

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint) 
