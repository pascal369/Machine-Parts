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

sperType=['helicalA','helicalB','helicalC','helical_A_B','helical_B_B','helical_B_C','helical_C_C']
sperMOD=['0.8','1','1.5','2','2.5','3','4','5','6','7','8','9','10']
sperIchi=['0','1','2','3','4','5','6','7','8']
helix=['right','left']

# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 700)
        Dialog.move(1000, 0)
        
        #形状
        self.label_type = QtGui.QLabel('Shape',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 22))
        #モジュール
        self.label_mod = QtGui.QLabel('Module',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(110, 35, 100, 22))

        #ねじれ角 helixAngle
        self.label_beta = QtGui.QLabel('helixAngle[deg]',Dialog)
        self.label_beta.setGeometry(QtCore.QRect(10, 63, 100, 22))
        self.le_beta = QtGui.QLineEdit('21.5',Dialog)
        self.le_beta.setGeometry(QtCore.QRect(110, 60, 100, 20))
        self.le_beta.setAlignment(QtCore.Qt.AlignCenter)
        #ねじれ方向
        self.label_betaK = QtGui.QLabel('helixDirection',Dialog)
        self.label_betaK.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.comboBox_betaK = QtGui.QComboBox(Dialog)
        self.comboBox_betaK.setGeometry(QtCore.QRect(110, 85, 100, 22))
        #歯数
        self.label_N = QtGui.QLabel('Number o of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.le_N = QtGui.QLineEdit('25',Dialog)
        self.le_N.setGeometry(QtCore.QRect(110, 110, 50, 20))
        self.le_N.setAlignment(QtCore.Qt.AlignCenter)
        #歯幅
        self.label_B = QtGui.QLabel('Tooth Width',Dialog)
        self.label_B.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.le_B = QtGui.QLineEdit('15',Dialog)
        self.le_B.setGeometry(QtCore.QRect(110, 135, 50, 20))
        self.le_B.setAlignment(QtCore.Qt.AlignCenter)
        #穴径
        self.label_dia = QtGui.QLabel('Hole Diameter',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 163, 100, 22))
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(110, 160, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス径
        self.label_Bdia = QtGui.QLabel('Boss Diameter',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 188, 100, 22))
        self.le_Bdia = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia.setGeometry(QtCore.QRect(110, 185, 50, 20))
        self.le_Bdia.setAlignment(QtCore.Qt.AlignCenter)
        #ボス幅
        self.label_BB = QtGui.QLabel('Boss Width',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 213, 100, 22))
        self.le_BB = QtGui.QLineEdit('25',Dialog)
        self.le_BB.setGeometry(QtCore.QRect(110, 210, 50, 20))
        self.le_BB.setAlignment(QtCore.Qt.AlignCenter)
         #ウエブ厚
        self.label_WB = QtGui.QLabel('Web Thickness',Dialog)
        self.label_WB.setGeometry(QtCore.QRect(10, 238, 100, 22))
        self.le_WB = QtGui.QLineEdit('9',Dialog)
        self.le_WB.setGeometry(QtCore.QRect(110, 235, 50, 20))
        self.le_WB.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 263, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(130, 263, 80, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 285, 160, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 310, 200, 200))
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
        self.spinBox.setGeometry(100, 640, 75, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_ichi = QtGui.QComboBox(Dialog)
        self.comboBox_ichi.setGeometry(QtCore.QRect(180, 640, 50, 30))

        self.comboBox_type.addItems(sperType)
        self.comboBox_type.setEditable(True)
        self.comboBox_mod.addItems(sperMOD)
        self.comboBox_mod.setEditable(True)
        self.comboBox_ichi.addItems(sperIchi)
        self.comboBox_ichi.setEditable(True)
        self.comboBox_betaK.addItems(helix)

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
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)

        self.comboBox_mod.setCurrentText('2')
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "helicalGear", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onShape(self):
        global key
        key=self.comboBox_type.currentText()
        d0=self.le_Bdia.text()
        t0=self.le_Bdia.text()
        if key=='helicalA':
            self.le_Bdia.hide()
            self.le_BB.hide()
            self.le_WB.hide()
        elif key=='helicalB' :
            self.le_Bdia.show()
            self.le_BB.show()
            self.le_WB.hide()
        elif key=='helicalC' :
            self.le_Bdia.show()
            self.le_BB.show()
            self.le_WB.show() 


        fname=key+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    

    def read_data(self):
         global outputShaft
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label=='outputShaft':
                         outputShaft=obj
                     if obj.TypeId =="Spreadsheet::Sheet":
                         spreadsheet = obj
                        
                         if selected_object.Label!='helicalAssy':
                             try:
                                 key2= spreadsheet.getContents('A2') 
                             except:
                                 pass

                             fname=key2+'.png'
                             base=os.path.dirname(os.path.abspath(__file__))
                             joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
                             self.label_6.setPixmap(QtGui.QPixmap(joined_path))              
    
                             self.comboBox_type.setCurrentText(key2[1:])
    
                             self.comboBox_mod.setCurrentText(spreadsheet.getContents('m0'))

                             self.le_N.setText(spreadsheet.getContents('B2'))
                             self.le_B.setText(spreadsheet.getContents('D2'))   
                             self.le_dia.setText(spreadsheet.getContents('E2'))  
                             self.le_Bdia.setText(spreadsheet.getContents('F2'))  
                             self.le_BB.setText(spreadsheet.getContents('G2')) 
                             self.le_WB.setText(spreadsheet.getContents('H2')) 
                             self.le_beta.setText(spreadsheet.getContents('J2'))
                             M=self.comboBox_mod.currentText()
                             N=self.le_N.text()
                             K=self.le_beta.text()
                             #print(K)
                             pcd=round(float(M)/(math.cos(float(K)/57.3))*float(N),2)
                             
                             self.label_M.setText(self.comboBox_mod.currentText()) 

                             if selected_object.Label=='Pinion':
                                 self.label_N1.setText(self.le_N.text())
                                 self.label_pcd1.setText(str(pcd))
                                 pcd1=pcd
                             elif selected_object.Label=='Gear':
                                 self.label_N2.setText(self.le_N.text()) 
                                 self.label_pcd2.setText(str(pcd))
                                 pcd2=pcd
                             else:
                                 self.label_N1.setText(self.le_N.text())
                                 self.label_pcd1.setText(str(pcd))
                                 pcd1=pcd
                                 #print(pcd1)    
                             try:
                                 L=round((pcd1+pcd2)/2,2)
                                 self.label_L1.setText(str(L))  
                             except:
                                 pass
                         elif selected_object.Label=='helicalAssy':
                             
                             key=spreadsheet.getContents('A2')[1:]
                             
                             self.comboBox_type.setCurrentText(key)
                             
                             fname=key+'.png'
                             base=os.path.dirname(os.path.abspath(__file__))
                             joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
                             self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 
                             
                             M=self.label_M.text()
                             N1=spreadsheet.getContents('n1')
                             N2=spreadsheet.getContents('n2')

                             #N2=spreadsheet.getContents('n2')
                             pcd1=spreadsheet.getContents('pcd1')
                             pcd2=spreadsheet.getContents('pcd2')
                             L=spreadsheet.getContents('Lc')

                             #self.label_M.setText(M)
                             spreadsheet.set('m0',M)
                             self.label_N1.setText(N1)
                             self.label_N2.setText(N2)
                             self.label_pcd1.setText(pcd1)
                             self.label_pcd2.setText(pcd2)
                             self.label_L1.setText(L)
                             return    
    
    def setParts(self):
     global Pinion
     global Gear    
     doc = FreeCAD.activeDocument()
     if doc:
         group_names = []
         for obj in doc.Objects:
             if hasattr(obj, 'Group'):
                 group_name = obj.Group
                 if group_name not in group_names:
                     group_names.append(group_name)
         for group_name in group_names:
             group_objects = [obj for obj in doc.Objects if hasattr(obj, 'Group') and obj.Group == group_name]
             for obj in group_objects:
                if obj.Label=='Pinion':
                    Pinion=obj
                elif obj.Label=='Gear':
                    Gear=obj    
     else:
         return
    def setIchi(self):
        #global A
        A=float(self.comboBox_ichi.currentText())
        Pinion.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A)
        self.spinBox.setValue(A)

        App.ActiveDocument.recompute()
    
    def spinMove(self):
         try:
             N1=self.label_N1.text()
             if N1=='***':
                 return
             N2=self.label_N2.text()
             r1 = self.spinBox.value()
             r2 =r1*float(N1)/float(N2)
             A=-float(self.comboBox_ichi.currentText())
             #A=0
             Pinion.Placement.Rotation=App.Rotation(App.Vector(0,1,0),3*(r1+A))
             Gear.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-3*r2)
             outputShaft.Placement.Rotation=App.Rotation(App.Vector(0,1,0),3*(r2*21/83+A))
         except:
             return
    
    def update(self):
         
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         if selected_object.Label!='helicalAssy':  
                             if selected_object.Label=='Pinion' or selected_object=='Gear':
                                 if selected_object.Label=='Pinion':
                                     N1=self.le_N.text()
                                 elif selected_object.Label=='Gear':    
                                     N2=self.le_N.text()
                             else:
                                 N=self.le_N.text()        
                                 
                             try:
                                 
                                 pcd1=self.label_pcd1.text()
                                 pcd2=self.label_pcd2.text()
                             except:
                                 pass    
                             
                             beta=self.le_beta.text()#ねじれ角       
                             mod=float(self.comboBox_mod.currentText())/math.cos(float(beta)/57.3) #モジュール

                             N=self.le_N.text()#歯数
                             t=self.le_B.text()#歯幅
                             dia=self.le_dia.text()#軸穴径   
                             Bdia=self.le_Bdia.text()#ボス径  
                             BB=self.le_BB.text()#ボス幅 
                             WB=self.le_WB.text()#ウエブ厚 
                             beta=self.le_beta.text()#ねじれ角
                             betaK=self.comboBox_betaK.currentText()#ねじれ方向
                             pcd=round(float(mod)*float(N),2)#pcd
                             print(pcd,mod)

                             self.label_pcd1.setText(str(pcd))
                             D=pcd+2*float(mod) #歯先円径
                             r=D/2 #歯先円半径
                             L=float(t)*math.tan(float(beta)/57.297)
                             sita=L*57.297/r
                             #print(selected_object.Label)
                             #if selected_object.Label=='Pinion' or selected_object.Label=='Gear':
                             M=self.comboBox_mod.currentText()
                             spreadsheet.set('B2',N)
                             spreadsheet.set('C2',M)
                             print(mod)
                             spreadsheet.set('D2',t)
                             spreadsheet.set('E2',dia)
                             spreadsheet.set('F2',Bdia)
                             spreadsheet.set('G2',BB)
                             spreadsheet.set('H2',WB)
                             spreadsheet.set('I2',str(pcd))
                             spreadsheet.set('J2',str(beta))
                             spreadsheet.set('K2',str(betaK))
                             spreadsheet.set('L2',str(sita))
                             App.ActiveDocument.recompute()


                             if selected_object.Label=='Pinion':
                                 N1=N
                                 pcd1=str(pcd)
                                 #L1=round((float(pcd1)+float(pcd2))/2 ,2)
                             elif  selected_object.Label=='Gear': 
                                 N2=N
                                 pcd2=str(pcd)
                                 #L1=round((float(pcd1)+float(pcd2))/2 ,2)
                             #try:
                                 #L1=round((float(pcd1)+float(pcd2))/2 ,2)
                             #except:
                             #    return
                             
                             if selected_object=='Pinon' or selected_object=='Gear':
                                 self.label_L1.setText(str(L1)) 
                                 self.label_pcd1.setText(pcd1)  
                                 self.label_pcd2.setText(pcd2) 
                                 self.label_N1.setText(N1) 
                                 self.label_N2.setText(N2) 
                             else:
                               
                                 #self.label_L1.setText(str(L1)) 
                                 self.label_pcd1.setText(str(pcd))  
                                 
                                 #print(N1)

                             App.ActiveDocument.recompute() 
                         elif selected_object.Label=='helicalAssy':
                             mod=self.label_M.text()
                             N1=self.label_N1.text()
                             N2=self.label_N2.text()
                             pcd1=self.label_pcd1.text()
                             pcd2=self.label_pcd2.text()
                             L=(float(pcd1)+float(pcd2))/2

                             #L=spreadsheet.getContents('Lc')

                             spreadsheet.set('m0',mod)
                             spreadsheet.set('n1',N1)
                             spreadsheet.set('n2',N2)
                             spreadsheet.set('pcd1',pcd1)
                             spreadsheet.set('pcd2',pcd2)
                             spreadsheet.set('Lc',str(L))
                             self.label_L1.setText(str(L))

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