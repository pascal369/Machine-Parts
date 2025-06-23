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

sperType=['sun','planetary','internal']
sperMOD=['0.8','1','1.5','2','2.5','3','4','5','6','7','8','9','10']
sperIchi=['0','1','2','3','4','5','6','7','8']
helix=['right','left']
pN=['2','3','4','5']

# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 640)
        Dialog.move(1000, 0)
        
        #形状
        self.label_type = QtGui.QLabel('Shape',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(120, 10, 100, 22))
        #モジュール
        self.label_mod = QtGui.QLabel('Module',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(120, 35, 100, 22))
        #ねじれ角 helixAngle
        self.label_beta = QtGui.QLabel('helixAngle[deg]',Dialog)
        self.label_beta.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_beta = QtGui.QLineEdit('21.5',Dialog)
        self.le_beta.setGeometry(QtCore.QRect(120, 60, 100, 20))
        self.le_beta.setAlignment(QtCore.Qt.AlignCenter)
        #ねじれ方向
        self.label_betaK = QtGui.QLabel('helixDirection',Dialog)
        self.label_betaK.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.comboBox_betaK = QtGui.QComboBox(Dialog)
        self.comboBox_betaK.setGeometry(QtCore.QRect(120, 85, 100, 22))
        #歯数
        self.label_z = QtGui.QLabel('Number o of Teeth',Dialog)
        self.label_z.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_z = QtGui.QLineEdit('25',Dialog)
        self.le_z.setGeometry(QtCore.QRect(120, 110, 50, 20))
        self.le_z.setAlignment(QtCore.Qt.AlignCenter)
        #歯幅
        self.label_t = QtGui.QLabel('Tooth Width',Dialog)
        self.label_t.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.le_t = QtGui.QLineEdit('15',Dialog)
        self.le_t.setGeometry(QtCore.QRect(120, 135, 50, 20))
        self.le_t.setAlignment(QtCore.Qt.AlignCenter)
        #穴径
        self.label_dia = QtGui.QLabel('Hole Diameter',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(120, 160, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス径
        self.label_Bdia = QtGui.QLabel('Boss Diameter',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.le_Bdia = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia.setGeometry(QtCore.QRect(120, 185, 50, 20))
        self.le_Bdia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス幅
        self.label_BB = QtGui.QLabel('Boss Width',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 213, 100, 22))
        self.le_BB = QtGui.QLineEdit('25',Dialog)
        self.le_BB.setGeometry(QtCore.QRect(120, 210, 50, 20))
        self.le_BB.setAlignment(QtCore.Qt.AlignCenter)
        #遊星歯車個数
        self.label_N = QtGui.QLabel('number of planetary',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 238, 100, 22))
        self.comboBox_N = QtGui.QComboBox(Dialog)
        self.comboBox_N.setGeometry(QtCore.QRect(120, 235, 100, 22))
        self.label_N0 = QtGui.QLabel('(za+zc)/2=',Dialog)
        self.label_N0.setGeometry(QtCore.QRect(10, 260, 100, 22))
        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 283, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 285, 60, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 310, 180, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 350, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        #アニメーション
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 570, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(100, 570, 75, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.comboBox_ichi = QtGui.QComboBox(Dialog)
        self.comboBox_ichi.setGeometry(QtCore.QRect(180, 570, 50, 30))
        self.comboBox_type.addItems(sperType)
        self.comboBox_type.setEditable(True)
        self.comboBox_mod.addItems(sperMOD)
        self.comboBox_mod.setEditable(True)
        self.comboBox_ichi.addItems(sperIchi)
        self.comboBox_ichi.setEditable(True)
        self.comboBox_betaK.addItems(helix)
        self.comboBox_N.addItems(pN)
        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onShape) 
        self.comboBox_type.setCurrentIndex(0)
        self.spinBox.valueChanged[int].connect(self.spinMove)
        self.comboBox_ichi.currentIndexChanged[int].connect(self.setIchi) 
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onShape)
        self.comboBox_mod.setCurrentText('2')
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "hypocycloidGears", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onShape(self):
    
        fname='hypoCycloid.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    

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
             r1 = self.spinBox.value()*30
             curvedPlate.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
             plate.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1/z1-r1)
             curvedPlate2.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
             plate2.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1/z1-r1)
             outputShaft.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1/z1)
             inputShaft.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
         except:
             return
    def update(self):
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