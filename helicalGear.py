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

sperType=['helical_A_B','helical_B_B','helical_B_C','helical_C_C']
sperMOD=['0.8','1','1.5','2','2.5','3','4','5','6','7','8','9','10']
sperIchi=['0','1','2','3','4','5','6','7','8']
helix=['right','left']

# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 725)
        Dialog.move(1000, 0)
        
        #形状
        self.label_type = QtGui.QLabel('Shape',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 110, 22))
        #モジュール
        self.label_mod = QtGui.QLabel('Module',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(110, 35, 110, 22))

        #ねじれ角 helixAngle
        self.label_beta = QtGui.QLabel('helixAngle[deg]',Dialog)
        self.label_beta.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_beta = QtGui.QLineEdit('21.5',Dialog)
        self.le_beta.setGeometry(QtCore.QRect(110, 60, 110, 22))
        self.le_beta.setAlignment(QtCore.Qt.AlignCenter)
        

        self.label00=QtGui.QLabel('Pinion　　　Gear',Dialog)
        self.label00.setGeometry(QtCore.QRect(65, 110, 200, 22))
        self.label00.setAlignment(QtCore.Qt.AlignCenter)
        #歯数
        self.label_N = QtGui.QLabel('Number of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.le_N = QtGui.QLineEdit('25',Dialog)
        self.le_N.setGeometry(QtCore.QRect(110,135, 50, 20))
        self.le_N.setAlignment(QtCore.Qt.AlignCenter)
        self.le_N2 = QtGui.QLineEdit('25',Dialog)
        self.le_N2.setGeometry(QtCore.QRect(160, 135, 50, 20))
        self.le_N2.setAlignment(QtCore.Qt.AlignCenter)

        #歯幅
        self.label_B = QtGui.QLabel('Teeth Width',Dialog)
        self.label_B.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_B = QtGui.QLineEdit('15',Dialog)
        self.le_B.setGeometry(QtCore.QRect(110,160, 50, 20))
        self.le_B.setAlignment(QtCore.Qt.AlignCenter)
        self.le_B2 = QtGui.QLineEdit('15',Dialog)
        self.le_B2.setGeometry(QtCore.QRect(160,160, 50, 20))
        self.le_B2.setAlignment(QtCore.Qt.AlignCenter)

        #穴径
        self.label_dia = QtGui.QLabel('Hole Diameter',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(110, 185, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        self.le_dia2 = QtGui.QLineEdit('15',Dialog)
        self.le_dia2.setGeometry(QtCore.QRect(160, 185, 50, 20))
        self.le_dia2.setAlignment(QtCore.Qt.AlignCenter)

        #ボス径
        self.label_Bdia = QtGui.QLabel('Boss Diameter',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 213, 100, 22))
        self.le_Bdia = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia.setGeometry(QtCore.QRect(110, 210, 50, 20))
        self.le_Bdia.setAlignment(QtCore.Qt.AlignCenter)
        self.le_Bdia2 = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia2.setGeometry(QtCore.QRect(160, 210, 50, 20))
        self.le_Bdia2.setAlignment(QtCore.Qt.AlignCenter)
        #ボス幅
        self.label_BB = QtGui.QLabel('Boss Width',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 238, 100, 22))
        self.le_BB = QtGui.QLineEdit('25',Dialog)
        self.le_BB.setGeometry(QtCore.QRect(110, 235, 50, 20))
        self.le_BB.setAlignment(QtCore.Qt.AlignCenter)
        self.le_BB2 = QtGui.QLineEdit('25',Dialog)
        self.le_BB2.setGeometry(QtCore.QRect(160, 235, 50, 20))
        self.le_BB2.setAlignment(QtCore.Qt.AlignCenter)

        

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 285, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(130, 285, 80, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 310, 170, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(60, 345, 150, 150))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        #ピニオン　ギア
        self.label_pg=QtGui.QLabel('Pinion　　　　　Gear',Dialog)
        self.label_pg.setGeometry(QtCore.QRect(45, 510, 200, 22))
        self.label_pg.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Mod=QtGui.QLabel('Modele',Dialog)
        self.label_Mod.setGeometry(QtCore.QRect(10, 535, 200, 22))
        self.label_M=QtGui.QLabel('***',Dialog)
        self.label_M.setGeometry(QtCore.QRect(50, 535, 200, 22))
        self.label_M.setAlignment(QtCore.Qt.AlignCenter)
        self.label_N=QtGui.QLabel('Number of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 560, 200, 22))
        self.label_N1=QtGui.QLabel('***',Dialog)
        self.label_N1.setGeometry(QtCore.QRect(90, 560, 50, 22))
        self.label_N1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_N2=QtGui.QLabel('***',Dialog)
        self.label_N2.setGeometry(QtCore.QRect(160, 560, 50, 22))
        self.label_N2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pcd=QtGui.QLabel('P.C.D',Dialog)
        self.label_pcd.setGeometry(QtCore.QRect(10, 585, 200, 22))
        self.label_pcd1=QtGui.QLabel('***',Dialog)
        self.label_pcd1.setGeometry(QtCore.QRect(90, 585, 50, 22))
        self.label_pcd1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pcd2=QtGui.QLabel('***',Dialog)
        self.label_pcd2.setGeometry(QtCore.QRect(160, 585, 50, 22))
        self.label_pcd2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_L=QtGui.QLabel('Center Distance',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 610, 200, 22))
        self.label_L1=QtGui.QLabel('***',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(50, 610, 200, 22))
        self.label_L1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 643, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(80, 640, 75, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)

        self.spinBox_Ichi=QtGui.QSpinBox(Dialog)
        self.spinBox_Ichi.setGeometry(160, 640, 50, 50)
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
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "helicalGear", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onShape(self):
        global key
        key=self.comboBox_type.currentText()
 
        fname=key+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    

    def read_data(self):
         global spreadsheet
         global Pinion
         global Gear
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
                     elif obj.TypeId =="Spreadsheet::Sheet":
                         spreadsheet = obj

                         
                         self.comboBox_type.setCurrentText(spreadsheet.getContents('A1'))
                         self.comboBox_mod.setCurrentText(spreadsheet.getContents('m0'))
                         self.le_N.setText(spreadsheet.getContents('z1'))
                         self.le_N2.setText(spreadsheet.getContents('z2'))
                         self.le_B.setText(spreadsheet.getContents('b1')) 
                         self.le_B2.setText(spreadsheet.getContents('b2'))   
                         self.le_dia.setText(spreadsheet.getContents('dia1'))  
                         self.le_dia2.setText(spreadsheet.getContents('dia2'))  
                         self.le_Bdia.setText(spreadsheet.getContents('Bdia1')) 
                         self.le_Bdia2.setText(spreadsheet.getContents('Bdia2'))  
                         self.le_BB.setText(spreadsheet.getContents('bb1')) 
                         self.le_BB2.setText(spreadsheet.getContents('bb2')) 
                         

                         self.label_M.setText(spreadsheet.getContents('m0'))
                         self.label_N1.setText(spreadsheet.getContents('z1'))
                         self.label_N2.setText(spreadsheet.getContents('z2'))
                         

            
    def setIchi(self):
        #global A
        N1=self.label_N1.text()
        A=self.spinBox_Ichi.value()
        Pinion.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A)
        #print(A)
        #self.spinBox.setValue(A)

        App.ActiveDocument.recompute()
    
    def spinMove(self):
         #try:
         N1=self.label_N1.text()
         if N1=='***':
             return
         N2=self.label_N2.text()
         A=self.spinBox_Ichi.value()
         r1 = self.spinBox.value()
         r2 =r1*float(N1)/float(N2)
        
         #A=float(N1)/360
         #print(r1,r2)
         Pinion.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1-A)
         Gear.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-r2)
         #except:
         #    return
    
    def update(self):
         m0=self.comboBox_mod.currentText()
         z1=self.le_N.text()
         z2=self.le_N2.text()
         beta=self.le_beta.text()
         b1=self.le_B.text()
         b2=self.le_B2.text()
         dia1=self.le_dia.text()
         dia2=self.le_dia2.text()
         L1=float(m0)*(float(z1)+float(z2))/2
         Bdia1=self.le_Bdia.text()
         Bdia2=self.le_Bdia2.text()
         bb1=self.le_BB.text()
         bb2=self.le_BB2.text()

         spreadsheet.set('beta',beta) 

         
         pcd1=float(m0)*float(z1)
         pcd2=float(m0)*float(z2)
         spreadsheet.set('m0',str(m0))
         spreadsheet.set('z1',str(z1))
         spreadsheet.set('z2',str(z2))
         spreadsheet.set('b1',str(b1))
         spreadsheet.set('b2',str(b2))
         spreadsheet.set('dia1',str(dia1))
         spreadsheet.set('dia2',str(dia2))
         spreadsheet.set('Bdia1',str(Bdia1))
         spreadsheet.set('Bdia2',str(Bdia2))
         spreadsheet.set('bb1',str(bb1))
         spreadsheet.set('bb2',str(bb2))
        
         self.label_M.setText(m0)
         self.label_N.setText(z1)
         self.label_N2.setText(z2)
         self.label_pcd1.setText(str(pcd1))
         self.label_pcd2.setText(str(pcd2))
         self.label_L1.setText(str(L1))
         
         
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