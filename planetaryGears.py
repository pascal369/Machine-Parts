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
        Dialog.resize(270, 690)
        Dialog.move(1000, 0)
        
        #形状
        self.label_type = QtGui.QLabel('Shape',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 8, 100, 12))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(120, 8, 100, 22))
        self.comboBox_type.setEditable(True)
        self.comboBox_type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #モジュール
        self.label_mod = QtGui.QLabel('Module',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.label_mod.setStyleSheet("color: black;")
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(120, 35, 100, 22))
        self.comboBox_mod.setEditable(True)
        self.comboBox_mod.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #ねじれ角 helixAngle
        self.label_beta = QtGui.QLabel('helixAngle[deg]',Dialog)
        self.label_beta.setGeometry(QtCore.QRect(10, 62, 100, 22))
        self.label_beta.setStyleSheet("color: black;")
        self.le_beta = QtGui.QLineEdit('21.5',Dialog)
        self.le_beta.setGeometry(QtCore.QRect(120, 62, 100, 22))
        self.le_beta.setAlignment(QtCore.Qt.AlignCenter)
        #ねじれ方向
        self.label_betaK = QtGui.QLabel('helixDirection',Dialog)
        self.label_betaK.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.label_betaK.setStyleSheet("color: black;")
        self.comboBox_betaK = QtGui.QComboBox(Dialog)
        self.comboBox_betaK.setGeometry(QtCore.QRect(120, 85, 100, 22))
        self.comboBox_betaK.setEditable(True)
        self.comboBox_betaK.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #歯数
        self.label_z = QtGui.QLabel('Number o of Teeth',Dialog)
        self.label_z.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.label_z.setStyleSheet("color: black;")
        self.le_z = QtGui.QLineEdit('25',Dialog)
        self.le_z.setGeometry(QtCore.QRect(120, 112, 100, 22))
        self.le_z.setAlignment(QtCore.Qt.AlignCenter)
        #歯幅
        self.label_t = QtGui.QLabel('Tooth Width',Dialog)
        self.label_t.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.label_t.setStyleSheet("color: black;")
        self.le_t = QtGui.QLineEdit('15',Dialog)
        self.le_t.setGeometry(QtCore.QRect(120, 135, 100, 22))
        self.le_t.setAlignment(QtCore.Qt.AlignCenter)
        #穴径
        self.label_dia = QtGui.QLabel('Hole Diameter',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(120, 160, 100, 22))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス径
        self.label_Bdia = QtGui.QLabel('Boss Diameter',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.label_Bdia.setStyleSheet("color: black;")
        self.le_Bdia = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia.setGeometry(QtCore.QRect(120, 185, 100, 22))
        self.le_Bdia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス幅
        self.label_BB = QtGui.QLabel('Boss Width',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 213, 100, 22))
        self.label_BB.setStyleSheet("color: black;")
        self.le_BB = QtGui.QLineEdit('25',Dialog)
        self.le_BB.setGeometry(QtCore.QRect(120, 210, 100, 22))
        self.le_BB.setAlignment(QtCore.Qt.AlignCenter)
        #遊星歯車個数
        self.label_N = QtGui.QLabel('number of planetary',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 238, 105, 22))
        self.label_N.setStyleSheet("color: black;")
        self.comboBox_N = QtGui.QComboBox(Dialog)
        self.comboBox_N.setGeometry(QtCore.QRect(120, 235, 100, 22))
        self.comboBox_N.setEditable(True)
        self.comboBox_N.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #条件設定
        self.pushButton_cd = QtGui.QPushButton('Condition setting',Dialog)
        self.pushButton_cd.setGeometry(QtCore.QRect(45, 265, 185, 22))
        self.label_N0 = QtGui.QLabel('(Zs+Zi)/N=',Dialog)
        self.label_N0.setGeometry(QtCore.QRect(10, 285, 250, 22))
        self.label_N0.setStyleSheet("color: black;")
        self.label_N02 = QtGui.QLabel('Zi-(Zs+2*Zp)=',Dialog)
        self.label_N02.setGeometry(QtCore.QRect(10, 305, 250, 22))
        self.label_N02.setStyleSheet("color: black;")

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(45, 335, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 335, 60, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(45, 360, 185, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 395, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #rotation
        self.label_spin=QtGui.QLabel('Rotation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 605, 150, 22))
        self.label_spin.setStyleSheet("color: black;")

        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(10, 630, 75, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        #Sun
        self.label_spin2=QtGui.QLabel('Sun Set',Dialog)
        self.label_spin2.setGeometry(QtCore.QRect(95, 605, 150, 22))
        self.label_spin2.setStyleSheet("color: black;")
        self.spinBox2=QtGui.QSpinBox(Dialog)
        self.spinBox2.setGeometry(95, 630, 75, 50)
        self.spinBox2.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox2.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox2.setValue(0.0)
        self.spinBox2.setAlignment(QtCore.Qt.AlignCenter)
        #Internal
        self.label_spin3=QtGui.QLabel('Internal Set',Dialog)
        self.label_spin3.setGeometry(QtCore.QRect(180, 605, 150, 22))
        self.label_spin3.setStyleSheet("color: black;")
        self.spinBox3=QtGui.QSpinBox(Dialog)
        self.spinBox3.setGeometry(180, 630, 75, 50)
        self.spinBox3.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox3.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox3.setValue(0.0)
        self.spinBox3.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_type.addItems(sperType)
        self.comboBox_type.setEditable(True)
        self.comboBox_mod.addItems(sperMOD)
        self.comboBox_mod.setEditable(True)
        self.comboBox_betaK.addItems(helix)
        self.comboBox_N.addItems(pN)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onShape) 
        self.comboBox_type.setCurrentIndex(0)

        self.spinBox.valueChanged[int].connect(self.spinMove)
        self.spinBox2.valueChanged[int].connect(self.setIchi)
        self.spinBox3.valueChanged[int].connect(self.setIchi2)
                
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.onCondition)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setIchi)
        QtCore.QObject.connect(self.pushButton_cd, QtCore.SIGNAL("pressed()"), self.onCondition)
        
        self.comboBox_mod.setCurrentText('2')
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "planetaryGears", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onShape(self):
    
        fname='planetaryGears.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    

    def read_data(self):
         global spreadsheet
         global planetary
         global planetary001
         global planetary002
         global planetary003
         global sun
         global carrier
         global internal
         doc = App.ActiveDocument
         objects = doc.Objects
         for obj in objects:
             #print(obj.Label)
             if obj.Label=='planetary':
                 planetary=obj
             elif obj.Label=='planetary001':
                 planetary001=obj 
             elif obj.Label=='planetary002':
                 planetary002=obj    
             elif obj.Label=='planetary003':
                 planetary003=obj 
             elif obj.Label=='sun':
                 sun=obj  
             elif obj.Label=='carrier':
                 carrier=obj  
             elif obj.Label=='internal':
                 internal=obj          
             elif obj.Label[:6] =="shtPln":
                 spreadsheet = obj

                 key2=self.comboBox_type.currentText()
                 self.comboBox_mod.setCurrentText(spreadsheet.getContents('m0'))
                 self.le_beta.setText(spreadsheet.getContents('beta'))
                 self.comboBox_betaK.setCurrentText(spreadsheet.getContents('betaK'))
                 self.comboBox_N.setCurrentText(spreadsheet.getContents('n'))
                 if key2=='sun':
                     self.le_z.setText(spreadsheet.getContents('za'))
                     self.le_t.setText(spreadsheet.getContents('ta'))   
                     self.le_dia.setText(spreadsheet.getContents('dia_a'))  
                     self.le_Bdia.setText(spreadsheet.getContents('Bdia_a'))  
                     self.le_BB.setText(spreadsheet.getContents('bb_a')) 
                 elif key2=='planetary':
                     zc=float(spreadsheet.getContents('zc'))
                     za=float(spreadsheet.getContents('za'))
                     zb=(zc-za)/2
                     self.le_z.setText(str(zb))
                     self.le_t.setText(spreadsheet.getContents('tb'))   
                     self.le_dia.setText(spreadsheet.getContents('dia_b'))  
                     self.le_Bdia.setText(spreadsheet.getContents('Bdia_b'))  
                     self.le_BB.setText(spreadsheet.getContents('bb_b')) 
                 elif key2=='internal':
                     self.le_z.setText(spreadsheet.getContents('zc'))
                     self.le_t.setText(spreadsheet.getContents('tc'))  


     
    def setParts(self):
     global sun
     global sun01
     global planetary
     global planetary001
     global planetary002
     global planetary003
     global internal
     global carrier
     global spreadsheet
     
     doc = FreeCAD.activeDocument()
     if doc:
         group_names = []
         for obj in doc.Objects:
             if obj.TypeId =="Spreadsheet::Sheet":
                    spreadsheet = obj  
             if hasattr(obj, 'Group'):
                 group_name = obj.Group
                 if group_name not in group_names:
                     group_names.append(group_name)
         for group_name in group_names:
             group_objects = [obj for obj in doc.Objects if hasattr(obj, 'Group') and obj.Group == group_name]
             for obj in group_objects:
                print(obj.Label)
                if obj.Label=='sun':
                    sun=obj
                elif obj.Label=='sun01':
                    sun01=obj      
                elif obj.Label=='internal':
                    internal=obj  
                elif obj.Label=='carrier':
                    carrier=obj  
                elif obj.Label=='planetary':
                    planetary=obj 
                elif obj.Label=='planetary001':
                    planetary001=obj   
                elif obj.Label=='planetary002':
                    planetary002=obj    
                elif obj.Label=='planetary003':
                    planetary003=obj        
                elif obj.TypeId =="Spreadsheet::Sheet":
                    spreadsheet = obj  

                key2=self.comboBox_type.currentText()
                         
                self.comboBox_mod.setCurrentText(spreadsheet.getContents('m0'))
                self.le_beta.setText(spreadsheet.getContents('beta'))
                self.comboBox_betaK.setCurrentText(spreadsheet.getContents('betaK'))
                self.comboBox_N.setCurrentText(spreadsheet.getContents('n'))
                if key2=='sun':
                    self.le_z.setText(spreadsheet.getContents('za'))
                    self.le_t.setText(spreadsheet.getContents('ta'))   
                    self.le_dia.setText(spreadsheet.getContents('dia_a'))  
                    self.le_Bdia.setText(spreadsheet.getContents('Bdia_a'))  
                    self.le_BB.setText(spreadsheet.getContents('bb_a')) 
                    
                elif key2=='planetary':
                    zc=float(spreadsheet.getContents('zc'))
                    za=float(spreadsheet.getContents('za'))
                    zb=(zc-za)/2
                    self.le_z.setText(str(zb))
                    self.le_t.setText(spreadsheet.getContents('tb'))   
                    self.le_dia.setText(spreadsheet.getContents('dia_b'))  
                    self.le_Bdia.setText(spreadsheet.getContents('Bdia_b'))  
                    self.le_BB.setText(spreadsheet.getContents('bb_b')) 
                elif key2=='internal':
                    self.le_z.setText(spreadsheet.getContents('zc'))
                    self.le_t.setText(spreadsheet.getContents('tc'))            
     else:
         return
     
    def setIchi(self):
        global A
        A=self.spinBox2.value()
        sun.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A)
        App.ActiveDocument.recompute()

    def setIchi2(self):
        global B
        B=self.spinBox3.value()
        internal.Placement.Rotation=App.Rotation(App.Vector(0,1,0),B)
        App.ActiveDocument.recompute()

    
    def spinMove(self):
         za=float(spreadsheet.getContents('za'))
         zc=float(spreadsheet.getContents('zc'))
         zb=(zc-za)/2
         r1 = self.spinBox.value()*5
         sun.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1*(1+za/zc)+A)
         carrier.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1*za/zc)
         planetary.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r1*(za/zb))
         App.ActiveDocument.recompute()
    
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

        App.ActiveDocument.recompute()
    
    def onCondition(self):
        Zs=float(spreadsheet.getContents('za'))      
        Zi=float(spreadsheet.getContents('zc')) 
        Zp=float(spreadsheet.getContents('zb'))
        n=float(spreadsheet.getContents('n')) 
        n02=Zi-(Zs+2*Zp)
        n0=(Zs+Zi)/n
        self.label_N0.setText('(Zs+Zi)/n=(' + str(Zs) + '+' + str(Zi) + ')/' + str(n) + '=' + str(n0) + '  must integer')
        self.label_N02.setText('Zi-(Zs+2*Zp)=' + str(Zi) + '-' + '(' + str(Zs) + '+' + '2*' + str(Zp)+')' + '=' + str(n02)+'  must 0')

    def create(self): 
         fname='planetaryGears.FCStd'
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
        