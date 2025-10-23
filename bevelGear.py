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

sperType=['bevelAssy',]
sperMOD=['0.8','1','1.5','2','2.5','3','4','5','6','7','8','9','10']
sperIchi=['0','1','2','3','4','5','6','7','8']
helix=['right','left']

# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")          
        Dialog.resize(250, 640)
        Dialog.move(1000, 0)
        #形状
        self.label_type = QtGui.QLabel('Shape',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 22))
        self.comboBox_type.setEditable(True)
        self.comboBox_type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        #軸角 axialAngle
        self.label_ax = QtGui.QLabel('axialAngle[deg]',Dialog)
        self.label_ax.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.label_ax.setStyleSheet("color: black;")
        self.le_ax = QtGui.QLineEdit('90',Dialog)
        self.le_ax.setGeometry(QtCore.QRect(110, 38, 100, 22))
        self.le_ax.setAlignment(QtCore.Qt.AlignCenter)
        self.le_ax.setReadOnly(True)
        
        #モジュール
        self.label_mod = QtGui.QLabel('Module',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.label_mod.setStyleSheet("color: black;")
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(110, 63, 100, 22))
        self.comboBox_mod.setEditable(True)
        self.comboBox_mod.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        #基準圧力角
        self.label_alpha = QtGui.QLabel('pressureAngle[deg]',Dialog)
        self.label_alpha.setGeometry(QtCore.QRect(10, 90, 100, 22))
        self.label_alpha.setStyleSheet("color: black;")
        self.le_alpha = QtGui.QLineEdit('20',Dialog)
        self.le_alpha.setGeometry(QtCore.QRect(110, 90, 100, 22))
        self.le_alpha.setAlignment(QtCore.Qt.AlignCenter)
        #ねじれ角
        self.label_beta = QtGui.QLabel('helixAngle[deg]',Dialog)
        self.label_beta.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.label_beta.setStyleSheet("color: black;")
        self.le_beta = QtGui.QLineEdit('0',Dialog)
        self.le_beta.setGeometry(QtCore.QRect(110, 113, 100, 22))
        self.le_beta.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label_pg1=QtGui.QLabel('Pinion　　　Gear',Dialog)
        self.label_pg1.setGeometry(QtCore.QRect(60, 135, 200, 22))
        self.label_pg1.setStyleSheet("color: black;")
        self.label_pg1.setAlignment(QtCore.Qt.AlignCenter)

        #歯数
        self.label_z = QtGui.QLabel('Number o of Teeth',Dialog)
        self.label_z.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.label_z.setStyleSheet("color: black;")
        self.le_z1 = QtGui.QLineEdit('20',Dialog)
        self.le_z1.setGeometry(QtCore.QRect(110, 160, 45, 22))
        self.le_z1.setAlignment(QtCore.Qt.AlignCenter)
        self.le_z2 = QtGui.QLineEdit('40',Dialog)
        self.le_z2.setGeometry(QtCore.QRect(165, 160, 45, 22))
        self.le_z2.setAlignment(QtCore.Qt.AlignCenter)
        

        #歯幅
        self.label_B = QtGui.QLabel('Tooth Width',Dialog)
        self.label_B.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.label_B.setStyleSheet("color: black;")
        self.le_B = QtGui.QLineEdit('22',Dialog)
        self.le_B.setGeometry(QtCore.QRect(110, 185, 100, 22))
        self.le_B.setAlignment(QtCore.Qt.AlignCenter)
        

        #穴径
        self.label_dia = QtGui.QLabel('Hole Diameter',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 213, 100, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.le_dia1 = QtGui.QLineEdit('15',Dialog)
        self.le_dia1.setGeometry(QtCore.QRect(110, 210, 45, 20))
        self.le_dia1.setAlignment(QtCore.Qt.AlignCenter)
        self.le_dia2 = QtGui.QLineEdit('15',Dialog)
        self.le_dia2.setGeometry(QtCore.QRect(165, 210, 45, 20))
        self.le_dia2.setAlignment(QtCore.Qt.AlignCenter)

        #ボス径
        self.label_Bdia = QtGui.QLabel('Boss Diameter',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 238, 100, 22))
        self.label_Bdia.setStyleSheet("color: black;")
        self.le_Bdia1 = QtGui.QLineEdit('45',Dialog)
        self.le_Bdia1.setGeometry(QtCore.QRect(110, 235, 45, 20))
        self.le_Bdia1.setAlignment(QtCore.Qt.AlignCenter)
        self.le_Bdia2 = QtGui.QLineEdit('45',Dialog)
        self.le_Bdia2.setGeometry(QtCore.QRect(165, 235, 45, 20))
        self.le_Bdia2.setAlignment(QtCore.Qt.AlignCenter)

        #ボス幅
        self.label_BB = QtGui.QLabel('Boss Width',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 263, 100, 22))
        self.label_BB.setStyleSheet("color: black;")
        self.le_BB1 = QtGui.QLineEdit('16',Dialog)
        self.le_BB1.setGeometry(QtCore.QRect(110, 260, 45, 20))
        self.le_BB1.setAlignment(QtCore.Qt.AlignCenter)
        self.le_BB2 = QtGui.QLineEdit('16',Dialog)
        self.le_BB2.setGeometry(QtCore.QRect(165, 260, 45, 20))
        self.le_BB2.setAlignment(QtCore.Qt.AlignCenter)


        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(45, 288, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 288, 60, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(45, 313, 185, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 350, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 560, 150, 22))
        self.label_spin.setStyleSheet("color: black;")
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(80, 560, 75, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)

        
        self.spinBox_Ichi=QtGui.QSpinBox(Dialog)
        self.spinBox_Ichi.setGeometry(160, 560, 50, 50)
        self.spinBox_Ichi.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox_Ichi.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox_Ichi.setValue(0.0)
        self.spinBox_Ichi.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_type.addItems(sperType)
        self.comboBox_type.setEditable(True)
        self.comboBox_mod.addItems(sperMOD)
        self.comboBox_mod.setEditable(True)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onShape) 
        self.comboBox_type.setCurrentIndex(0)

        self.spinBox.valueChanged[int].connect(self.spinMove)
        self.spinBox_Ichi.valueChanged[int].connect(self.setIchi) 
        
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)

        self.comboBox_mod.setCurrentText('2')
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "bevelGear", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onShape(self):
        #return
        global key
        
        key=self.comboBox_type.currentText()

        fname=key+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    
    
    def setParts(self):
     global Pinion
     global Gear  
     global spreadsheet  
     #global key
     selection = Gui.Selection.getSelection()
     if selection:
         selected_object = selection[0]
         if selected_object.TypeId == "App::Part":
             parts_group = selected_object
             for obj in parts_group.Group:
                 #print(obj.Label)
                 if obj.Label[:6]=='Pinion':
                     Pinion=obj
                 elif obj.Label[:4]=='Gear':
                     Gear=obj    

                 elif obj.Label[:16] =="shtBevelGearAssy":
                     spreadsheet = obj
                 elif obj.Label [:22]=="shtSpiralBevelGearAssy":
                     spreadsheet = obj    
             #key=spreadsheet.getContents('A2')
             self.comboBox_type.setCurrentText(key)
             fname=key+'.png'
             base=os.path.dirname(os.path.abspath(__file__))
             joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
             self.label_6.setPixmap(QtGui.QPixmap(joined_path))              
             self.comboBox_type.setCurrentText(key)
             #self.le_ax.setText(spreadsheet.getContents('sigma'))
             self.comboBox_mod.setCurrentText(spreadsheet.getContents('m0'))
             self.le_alpha.setText(spreadsheet.getContents('alphan'))
             #if key=='spiralBevelAssy':
             self.le_beta.setText(spreadsheet.getContents('beta'))
                 #self.comboBox_betaK.setCurrentText(spreadsheet.getContents('betaK'))

             self.le_z1.setText(spreadsheet.getContents('z1'))
             self.le_z2.setText(spreadsheet.getContents('z2'))
             self.le_B.setText(spreadsheet.getContents('b'))   
             self.le_dia1.setText(spreadsheet.getContents('dia1'))  
             self.le_dia2.setText(spreadsheet.getContents('dia2'))  
             self.le_Bdia1.setText(spreadsheet.getContents('Bdia1'))  
             self.le_Bdia2.setText(spreadsheet.getContents('Bdia2'))
             self.le_BB1.setText(spreadsheet.getContents('bb1')) 
             self.le_BB2.setText(spreadsheet.getContents('bb2'))   
             self.le_beta.setText(spreadsheet.getContents('beta'))   
             fname=key+'.png'
             base=os.path.dirname(os.path.abspath(__file__))
             joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
             self.label_6.setPixmap(QtGui.QPixmap(joined_path))   


     else:
         return
    def setIchi(self):
        #global A
        A=float(self.spinBox_Ichi.value())
        Pinion.Placement.Rotation=App.Rotation(App.Vector(1,0,0),A)
        self.spinBox.setValue(A)

        App.ActiveDocument.recompute()
    
    def spinMove(self):
         N1=self.le_z1.text()
         if N1=='***':
             return
         N2=self.le_z2.text()
         r1 = self.spinBox.value()
         r2 =r1*float(N1)/float(N2)
         A=-float(self.spinBox_Ichi.value())
         Pinion.Placement.Rotation=App.Rotation(App.Vector(1,0,0),3*(r1+A))
         Gear.Placement.Rotation=App.Rotation(App.Vector(0,0,1),-3*r2)
                 

    
    def update(self):
        sigma=90 #軸角
        m0=float(self.comboBox_mod.currentText())#モジュール   
        alphan=float(self.le_alpha.text())

        beta=float(self.le_beta.text())
        #betaK=self.comboBox_betaK.currentText()

        z1=float(self.le_z1.text())#歯数              
        z2=float(self.le_z2.text())#歯数  
        alphat=math.atan(math.tan(alphan/57.3)/math.cos(beta/57.3))*57.3
        pcd1=m0*z1
        pcd2=m0*z2
        delta1=math.atan(math.sin(sigma/57.3)/(z2/z1+math.cos(sigma/57.3)))*57.3
        delta2=sigma-delta1
        R=pcd2/(2*math.sin(delta2/57.3))
        b=float(self.le_B.text())#歯幅
        #if key=='spiralBevelAssy':
        #    ha2=0.46*m0+0.39*m0/(z2*math.cos(delta1/57.3)/(z1*math.cos(delta2/57.3)))
        #    ha1=1.7*m0-ha2
        #    hf1=1.888*m0-ha1
        #    hf2=1.888*m0-ha2
        #    sita_f1=math.atan(hf1/R)*57.3
        #    sita_f2=math.atan(hf2/R)*57.3
        #    sita_a1=sita_f2
        #    sita_a2=sita_f1
        #    delta_a1=delta1+sita_a1
        #    delta_a2=delta2+sita_a2
        #    delta_f1=delta1-sita_f1
        #    delta_f2=delta2-sita_f2
        #    da1=pcd1+2*ha1*math.cos(delta1/57.3)
        #    da2=pcd2+2*ha2*math.cos(delta2/57.3)
        #    x1=R*math.cos(delta1/57.3)-ha1*math.sin(delta1/57.3)
        #    x2=R*math.cos(delta2/57.3)-ha2*math.sin(delta2/57.3)
        #    xb1=b*math.cos(delta_a1/57.3)/math.cos(sita_a1/57.3)
        #    xb2=b*math.cos(delta_a2/57.3)/math.cos(sita_a2/57.3)
        #    di1=da1-2*b*math.sin(delta_a1/57.3)/math.cos(sita_a1/57.3)
        #    di2=da2-2*b*math.sin(delta_a2/57.3)/math.cos(sita_a2/57.3)


        #elif key=='bevelAssy':
        ha1=m0    
        hf1=1.25*m0
        sita_f1=math.atan(hf1/R)*57.3
        sita_a1=math.atan(ha1/R)*57.3
        delta_a1=delta1+sita_a1
        delta_a2=delta2+sita_a1
        delta_f1=delta1-sita_f1
        delta_f2=delta2-sita_f1
        da1=pcd1+2*ha1*math.cos(delta1/57.3)
        da2=pcd2+2*ha1*math.cos(delta2/57.3)
        x1=R*math.cos(delta1/57.3)-ha1*math.sin(delta1/57.3)
        x2=R*math.cos(delta2/57.3)-ha1*math.sin(delta2/57.3)
        xb1=b*math.cos(delta_a1/57.3)/math.cos(sita_a1/57.3)
        xb2=b*math.cos(delta_a2/57.3)/math.cos(sita_a1/57.3)
        di1=da1-2*b*math.sin(delta_a1/57.3)/math.cos(sita_a1/57.3)
        di2=da2-2*b*math.sin(delta_a2/57.3)/math.cos(sita_a1/57.3)

        dia1=self.le_dia1.text()#軸径1
        dia2=self.le_dia2.text()#軸径2
        Bdia1=float(self.le_Bdia1.text())#ボス径1  
        Bdia2=float(self.le_Bdia2.text())#ボス径2
        BB1=float(self.le_BB1.text())#ボス幅1 
        BB2=float(self.le_BB2.text())#ボス幅2

        #spreadsheet.set('sigma',str(sigma))
        spreadsheet.set('m0',str(m0))
        spreadsheet.set('alphan',str(alphan))
        #if key=='spiralBevelAssy':
        spreadsheet.set('beta',str(beta))
        #    spreadsheet.set('betaK',str(betaK))
        #    spreadsheet.set('alphat',str(alphat))

        spreadsheet.set('z1',str(z1))
        spreadsheet.set('z2',str(z2))
        
        spreadsheet.set('pcd1',str(pcd1))
        spreadsheet.set('pcd2',str(pcd2))
        spreadsheet.set('delta1',str(delta1))
        spreadsheet.set('delta2',str(delta2))
        spreadsheet.set('R',str(R))
        spreadsheet.set('b',str(b))
        #if key=='spiralBevelAssy':
#
        #    spreadsheet.set('ha2',str(ha2))
        #    spreadsheet.set('ha1',str(ha1))
        #    spreadsheet.set('hf1',str(hf1)) 
        #    spreadsheet.set('hf2',str(hf2)) 
        #    spreadsheet.set('sita_f1',str(sita_f1))
        #    spreadsheet.set('sita_f2',str(sita_f2))
        #    spreadsheet.set('sita_a1',str(sita_a1))
        #    spreadsheet.set('sita_a2',str(sita_a2))
        #elif key=='bevelAssy':  
        spreadsheet.set('ha',str(ha1))
        spreadsheet.set('hf',str(hf1))
        spreadsheet.set('sita_f',str(sita_f1))
        spreadsheet.set('sita_a',str(sita_a1))

        spreadsheet.set('delta_a1',str(delta_a1))
        spreadsheet.set('delta_a2',str(delta_a2))
        spreadsheet.set('delta_f1',str(delta_f1))
        spreadsheet.set('delta_f2',str(delta_f2))
        spreadsheet.set('da1',str(da1))
        spreadsheet.set('da2',str(da2))
        spreadsheet.set('x1',str(x1))
        spreadsheet.set('x2',str(x2))
        spreadsheet.set('xb1',str(xb1))
        spreadsheet.set('xb2',str(xb2))
        spreadsheet.set('di1',str(di1))
        spreadsheet.set('di2',str(di2))
        spreadsheet.set('dia1',dia1)
        spreadsheet.set('dia2',dia2)
        spreadsheet.set('Bdia1',str(Bdia1))
        spreadsheet.set('Bdia2',str(Bdia2))
        spreadsheet.set('bb1',str(BB1))
        spreadsheet.set('bb2',str(BB2))

        
        #円錐頂点からボス端まで
        xc1=R/math.cos(delta1/57.3)-(Bdia1/2)*math.tan(delta1/57.3)+BB1
        xc2=R/math.cos(delta2/57.3)-(Bdia2/2)*math.tan(delta2/57.3)+BB2
        spreadsheet.set('xc1',str(xc1))
        spreadsheet.set('xc2',str(xc2))
        #歯車位置
        pL11=x1-xb1
        pL21=R/math.cos(delta1/57.3)
        pL12=x2-xb2
        pL22=R/math.cos(delta2/57.3)
        spreadsheet.set('pL11',str(pL11))
        spreadsheet.set('pL12',str(pL12))
        spreadsheet.set('pL21',str(pL21))
        spreadsheet.set('pL22',str(pL22))
        #内端歯先からボス端まで
        xd1=xc1-pL11
        xd2=xc2-pL12
        spreadsheet.set('xd1',str(xd1))
        spreadsheet.set('xd2',str(xd2))
        #外端歯先円からボス端まで
        xe1=xc1-x1
        xe2=xc2-x2
        spreadsheet.set('xe1',str(xe1))
        spreadsheet.set('xe2',str(xe2))
        
        App.ActiveDocument.recompute() 
    
    
   
    def create(self): 
         fname=key+'.FCStd'
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