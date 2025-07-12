# -*- coding: utf-8 -*-
import os
import sys
import csv
from tokenize import group
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi



# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 340)
        Dialog.move(1000, 0)
 
        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 10, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 10, 60, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 35, 180, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 60, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        fname='hypoCycloid.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))  
        #アニメーション
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 270, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(100, 270, 75, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.comboBox_ichi = QtGui.QComboBox(Dialog)
        self.comboBox_ichi.setGeometry(QtCore.QRect(180, 270, 50, 30))
        
        self.spinBox.valueChanged[int].connect(self.spinMove)
        self.comboBox_ichi.currentIndexChanged[int].connect(self.setIchi) 
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
       
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "hypocycloidGears", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def read_data(self):
     global spreadsheet
     global inputShaft
     global outputShaft
     global bearing
     global curvedPlate
     global curvedPlate2
     global Brg
     global plate
     global plate2
     
     doc = App.ActiveDocument
     objects = doc.Objects
     for obj in objects:
         #print(obj.Label)
         if obj.Label=='inputShaft':
             inputShaft=obj
         elif obj.Label=='outputShaft':
             outputShaft=obj    
         elif obj.Label=='bearing':
             bearing=obj 
         elif obj.Label=='curvedPlate':
             curvedPlate=obj    
         elif obj.Label=='curvedPlate2':
             curvedPlate2=obj 
         elif obj.Label=='Brg':
             Brg=obj  
         elif obj.Label=='plate':
            plate=obj  
         elif obj.Label=='plate2':
            plate2=obj          
         elif obj.Label[:7] =="shtHypo":
             spreadsheet = obj
    
    def setParts(self):
     return
     
    def setIchi(self):
        A=float(self.comboBox_ichi.currentText())
        self.spinBox.setValue(A)
        App.ActiveDocument.recompute()
    def spinMove(self):
         try:
             z1=float(spreadsheet.getContents('z1'))
             r1 = self.spinBox.value()*20
             curvedPlate.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
             plate.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1/z1-r1)
             curvedPlate2.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
             plate2.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1/z1-r1)
             outputShaft.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1/z1)
             inputShaft.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
         except:
             return
    def update(self):
        return
        mod=self.comboBox_mod.currentText()
        beta=self.le_beta.text()
        key2=self.comboBox_type.currentText()
        n=self.comboBox_N.currentText()
        spreadsheet.set('m0',mod)
        spreadsheet.set('beta',beta)
        spreadsheet.set('n',n)
        z=self.le_z.text()
        t=self.le_t.text()
        pcd=float(mod)*float(z)
        dia=self.le_dia.text()
        bb=self.le_BB.text()
        Bdia=self.le_Bdia.text()
        if key2=='sun': 
            spreadsheet.set('za',z)
            spreadsheet.set('ta',t)
            spreadsheet.set('pcda',str(pcd))
            spreadsheet.set('dia_a',dia)
            spreadsheet.set('bb_a',bb)
            spreadsheet.set('Bdia_a',Bdia)
        elif key2=='planetary':   
            spreadsheet.set('zb',z)
            spreadsheet.set('tb',t)
            spreadsheet.set('pcdb',str(pcd))
            spreadsheet.set('dia_b',dia)
            spreadsheet.set('bb_b',bb)
            spreadsheet.set('Bdia_b',Bdia)  
        elif key2=='internal':   
            spreadsheet.set('zc',z)
            spreadsheet.set('tc',t)
            spreadsheet.set('pcdc',str(pcd))
            spreadsheet.set('bb_b',bb)
            spreadsheet.set('Bdia_b',Bdia)    
        za=float(spreadsheet.getContents('za'))      
        zc=float(spreadsheet.getContents('zc'))   
        n0=(zc+za)/2  
        self.label_N0.setText('(za+zc)/2=' + str(n0))
    App.ActiveDocument.recompute()
    def create(self): 
         fname='hypoCycloid.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Gear_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         Gui.SendMsgToActiveView("ViewFit")   

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