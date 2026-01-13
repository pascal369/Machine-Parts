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

sperType=['wormAssy_A','wormAssy_B',]
sperMOD=['0.8','1','1.5','2','2.5','3','4','4.5','5','6','7','8','9','10']
sperIchi=['0','1','2','3','4','5','6','7','8']
helix=['right','left']
diaQ={
    '1.0':(16.00),
    '2.0':(12.50),
    '4.0':(11.25),
    '8.0':(10.00),
    '16.0':(8.75),
    '25.0':(8.00)
}
# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 775)
        Dialog.move(1000, 0)
        
        #形状
        self.label_type = QtGui.QLabel('Shape',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 22))
        self.label_type.setStyleSheet("color: black;")

        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 22))
        #モジュール
        self.label_mod = QtGui.QLabel('Module',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.label_mod.setStyleSheet("color: black;")
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(110, 38, 100, 22))
        self.comboBox_mod.setEditable(True)
        self.comboBox_mod.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        #条数 歯数 Number of articles　or teeth
        self.label_N = QtGui.QLabel('numberOfArticles',Dialog)
        self.label_N.setGeometry(QtCore.QRect(30, 68, 100, 12))
        self.label_N.setStyleSheet("color: black;")
        self.le_N = QtGui.QLineEdit('1',Dialog)
        self.le_N.setGeometry(QtCore.QRect(50, 90, 50, 20))
        self.le_N.setAlignment(QtCore.Qt.AlignCenter)

        self.label_N2 = QtGui.QLabel('numberOfTeeth',Dialog)
        self.label_N2.setGeometry(QtCore.QRect(135, 68, 100, 12))
        self.label_N2.setStyleSheet("color: black;")
        self.le_N2 = QtGui.QLineEdit('30',Dialog)
        self.le_N2.setGeometry(QtCore.QRect(150, 90, 50, 20))
        self.le_N2.setAlignment(QtCore.Qt.AlignCenter)

        #進み角 leadxAngle
        self.label_beta = QtGui.QLabel('leadAngle[deg]',Dialog)
        self.label_beta.setGeometry(QtCore.QRect(10, 118, 100, 22))
        self.label_beta.setStyleSheet("color: black;")
        self.le_beta = QtGui.QLineEdit('3.9',Dialog)
        self.le_beta.setGeometry(QtCore.QRect(110, 115, 100, 20))
        self.le_beta.setAlignment(QtCore.Qt.AlignCenter)
        self.le_beta.setReadOnly(True)
        #ねじれ方向
        self.label_betaK = QtGui.QLabel('helix Direction',Dialog)
        self.label_betaK.setGeometry(QtCore.QRect(10, 143, 100, 22))
        self.label_betaK.setStyleSheet("color: black;")
        self.comboBox_betaK = QtGui.QComboBox(Dialog)
        self.comboBox_betaK.setGeometry(QtCore.QRect(110, 140, 100, 22))
        #中心距離 a
        self.label_a = QtGui.QLabel('center Distance',Dialog)
        self.label_a.setGeometry(QtCore.QRect(10, 168, 100, 22))
        self.label_a.setStyleSheet("color: black;")
        self.le_a = QtGui.QLineEdit(Dialog)
        self.le_a.setGeometry(QtCore.QRect(110, 168, 100, 22))
        self.le_a.setAlignment(QtCore.Qt.AlignCenter)

        #Q値
        self.label_Q = QtGui.QLabel('Qvalue(reference)',Dialog)
        self.label_Q.setGeometry(QtCore.QRect(10, 193, 100, 22))
        self.label_Q.setStyleSheet("color: black;")
        self.le_Q = QtGui.QLineEdit('10',Dialog)
        self.le_Q.setGeometry(QtCore.QRect(110, 193, 50, 20))
        self.le_Q.setAlignment(QtCore.Qt.AlignCenter)
        
        #ウオーム長さ　ホイール厚
        self.label_B = QtGui.QLabel('Length or Width',Dialog)
        self.label_B.setGeometry(QtCore.QRect(10, 218, 100, 22))
        self.label_B.setStyleSheet("color: black;")
        self.le_B = QtGui.QLineEdit('15',Dialog)
        self.le_B.setGeometry(QtCore.QRect(110, 218, 50, 20))
        self.le_B.setAlignment(QtCore.Qt.AlignCenter)
        
        self.le_Bw = QtGui.QLineEdit(Dialog)
        self.le_Bw.setGeometry(QtCore.QRect(170, 215, 50, 20))
        self.le_Bw.setAlignment(QtCore.Qt.AlignCenter)

        #軸径
        self.label_dia = QtGui.QLabel('shaft Diameter',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 243, 100, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(110, 240, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)

        self.le_dia2 = QtGui.QLineEdit('15',Dialog)
        self.le_dia2.setGeometry(QtCore.QRect(170, 240, 50, 20))
        self.le_dia2.setAlignment(QtCore.Qt.AlignCenter)

        #ボス径
        self.label_Bdia = QtGui.QLabel('Boss Diameter',Dialog)
        self.label_Bdia.setGeometry(QtCore.QRect(10, 268, 100, 22))
        self.label_Bdia.setStyleSheet("color: black;")
        self.le_Bdia = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia.setGeometry(QtCore.QRect(110, 265, 50, 20))
        self.le_Bdia.setAlignment(QtCore.Qt.AlignCenter)
        
        self.le_Bdia2 = QtGui.QLineEdit('60',Dialog)
        self.le_Bdia2.setGeometry(QtCore.QRect(170, 265, 50, 20))
        self.le_Bdia2.setAlignment(QtCore.Qt.AlignCenter)

        #ボス幅
        self.label_BB = QtGui.QLabel('Boss Width',Dialog)
        self.label_BB.setGeometry(QtCore.QRect(10, 293, 100, 22))
        self.label_BB.setStyleSheet("color: black;")
        self.le_BB = QtGui.QLineEdit('25',Dialog)
        self.le_BB.setGeometry(QtCore.QRect(110, 290, 50, 20))
        self.le_BB.setAlignment(QtCore.Qt.AlignCenter)
         #ウエブ厚
        self.label_WB = QtGui.QLabel('WebThickness',Dialog)
        self.label_WB.setGeometry(QtCore.QRect(10, 318, 100, 22))
        self.label_WB.setStyleSheet("color: black;")
        self.le_WB = QtGui.QLineEdit('9',Dialog)
        self.le_WB.setGeometry(QtCore.QRect(110, 315, 50, 20))
        self.le_WB.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(40, 340, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(135, 340, 80, 22))
        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(40, 365, 185, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 385, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        #worm wheel
        self.label_pg=QtGui.QLabel('worm　　　　　wheel',Dialog)
        self.label_pg.setGeometry(QtCore.QRect(45, 585, 200, 22))
        self.label_pg.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pg.setStyleSheet("color: black;")

        self.label_Mod=QtGui.QLabel('Module',Dialog)
        self.label_Mod.setGeometry(QtCore.QRect(10, 610, 200, 22))
        self.label_Mod.setStyleSheet("color: black;")

        self.label_M=QtGui.QLabel('***',Dialog)
        self.label_M.setGeometry(QtCore.QRect(50, 610, 200, 22))
        self.label_M.setAlignment(QtCore.Qt.AlignCenter)
        self.label_M.setStyleSheet("color: black;")

        self.label_N=QtGui.QLabel('Number of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 635, 200, 22))
        self.label_N.setStyleSheet("color: black;")

        self.label_N1=QtGui.QLabel('***',Dialog)
        self.label_N1.setGeometry(QtCore.QRect(90, 635, 50, 22))
        self.label_N1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_N1.setStyleSheet("color: black;")

        self.label_N2=QtGui.QLabel('***',Dialog)
        self.label_N2.setGeometry(QtCore.QRect(160, 635, 50, 22))
        self.label_N2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_N2.setStyleSheet("color: black;")

        self.label_pcd=QtGui.QLabel('P.C.D',Dialog)
        self.label_pcd.setGeometry(QtCore.QRect(10, 660, 200, 22))
        self.label_pcd.setStyleSheet("color: black;")

        self.label_pcd1=QtGui.QLabel('***',Dialog)
        self.label_pcd1.setGeometry(QtCore.QRect(90, 660, 50, 22))
        self.label_pcd1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pcd1.setStyleSheet("color: black;")

        self.label_pcd2=QtGui.QLabel('***',Dialog)
        self.label_pcd2.setGeometry(QtCore.QRect(160, 660, 50, 22))
        self.label_pcd2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pcd2.setStyleSheet("color: black;")

        self.label_L=QtGui.QLabel('Center Distance',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 685, 200, 22))
        self.label_L.setStyleSheet("color: black;")

        self.label_L1=QtGui.QLabel('***',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(50, 685, 200, 22))
        self.label_L1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_L1.setStyleSheet("color: black;")
        
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 710, 150, 22))
        self.label_spin.setStyleSheet("color: black;")

        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(75, 710, 100, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_ichi=QtGui.QSpinBox(Dialog)
        self.spinBox_ichi.setGeometry(180, 710, 50, 50)
        self.spinBox_ichi.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox_ichi.setMaximum(360.0)  # 最大値を100.0に設定
        self.spinBox_ichi.setValue(0.0)
        self.spinBox_ichi.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_type.addItems(sperType)
        self.comboBox_type.setEditable(True)
        self.comboBox_mod.addItems(sperMOD)
        self.comboBox_mod.setEditable(True)
        self.comboBox_betaK.addItems(helix)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onShape) 
        self.comboBox_type.setCurrentIndex(0)

        self.spinBox.valueChanged[int].connect(self.spinMove)
        self.spinBox_ichi.valueChanged[int].connect(self.setIchi)
        
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onShape)
        
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "wormGear", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onShape(self):
        global key
        key=self.comboBox_type.currentText()
        d0=self.le_Bdia.text()
        t0=self.le_Bdia.text()
        M=self.comboBox_mod.currentText()
        sa=diaQ

        if float(M)<=1.00:
            q1=16.00
        elif float(M)<=2.00:
            q1=12.50
        elif float(M)<=4.00:
            q1=11.25
        elif float(M)<=8.00:
            q1=10.00
        elif float(M)<=16.00:
            q1=8.75
        elif float(M)>16.00:
            q1=8.00                    
        
        fname=key+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))    

    def read_data(self):
          global spreadsheet
          global worm
          global wheel
          global key2
          selection = Gui.Selection.getSelection()
          if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.Label[:4]=='worm':
                         worm=obj
                     elif obj.Label[:5]=='wheel':
                         wheel=obj    

                     elif obj.Label[:10] =="SprshtAssy":
                         spreadsheet = obj
                         key2= spreadsheet.getContents('A1') 

                         fname=key2+'.png'
                         base=os.path.dirname(os.path.abspath(__file__))
                         joined_path = os.path.join(base, "prt_data",'Gear_data',fname)
                         self.label_6.setPixmap(QtGui.QPixmap(joined_path))              
                         self.comboBox_type.setCurrentText(key2[1:])
                         N1=float(spreadsheet.getContents('z1'))
                         N2=float(spreadsheet.getContents('z2'))
                         M=float(spreadsheet.getContents('m0')) 
                         a=float(spreadsheet.getContents('a'))
                         pcd2=N2 * M
                         pcd1=(a - pcd2 / 2) * 2

                         Qv=pcd1 / M
                         L0=round(M * 3.142 * (4.5 + 0.02 * pcd2),1)
                         self.le_B.setText(str(L0))
                         self.le_B.setReadOnly(True)

                         w0=round(2*M*(Qv+1)**0.5+1.5*M,1)
                         self.le_Bw.setText(str(w0)) 
                         #self.le_Bw.setReadOnly(True)
                         self.le_Bdia.setText(spreadsheet.getContents('Bdia'))  
                         self.le_BB.setText(spreadsheet.getContents('BB')) 
                         self.le_a.setText(spreadsheet.getContents('a')) 
                         self.le_WB.setText(spreadsheet.getContents('WB')) 
                         Bdia=float(self.le_Bdia.text())
                         dia1=float(self.le_dia.text())
                         if dia1>Bdia:
                             dia1=Bdia
                         self.le_dia.setText(spreadsheet.getContents('dia1'))
                         self.le_dia2.setText(spreadsheet.getContents('dia2'))
                         self.comboBox_mod.setCurrentText(str(M))
                         self.le_N.setText(spreadsheet.getContents('z1'))
                         self.le_N2.setText(spreadsheet.getContents('z2'))
                         self.label_M.setText(str(M))
                         self.label_N1.setText(str(N1))
                         self.label_N2.setText(str(N2))
                         self.label_pcd1.setText(str(pcd1))
                         self.label_pcd2.setText(str(pcd2))
                         self.label_L1.setText(str(a))
    
    def setIchi(self):

        r1 = self.spinBox_ichi.value()
        worm.Placement.Rotation=App.Rotation(App.Vector(1,0,0),10*r1)
        App.ActiveDocument.recompute()
    
    def spinMove(self):
         print(key2)
         N1=self.label_N1.text()
         N2=self.label_N2.text()
         r1 = self.spinBox.value()
         r2 =r1*float(N1)/float(N2)
         A=self.spinBox_ichi.value()
         x=10
         worm.Placement.Rotation=App.Rotation(App.Vector(1,0,0),x*(r1+A))
         if key2[1:]=='wormAssy_B':
              wheel.Placement.Rotation=App.Rotation(App.Vector(0,1,0),x*r2)
         else:
              wheel.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-x*r2)
    def update(self):
              mod=float(self.comboBox_mod.currentText()) #モジュール
              spreadsheet.set('m0',str(mod))
              N1=float(self.le_N.text())
              N2=float(self.le_N2.text())
              ganmaK=self.comboBox_betaK.currentText()
              a=float(self.le_a.text())
              d2=mod*N2
              d1=(a - d2 / 2) * 2
              Qv=d1 / mod
              ganma=round(math.atan(mod * N1 / d1)*57.3,3)
              spreadsheet.set('z1',str(N1))
              spreadsheet.set('z2',str(N2))
              spreadsheet.set('ganma',str(ganma))
              self.comboBox_betaK.setCurrentText(spreadsheet.getContents('ganmaK'))#ねじれ角   
              spreadsheet.set('ganmaK',ganmaK)
              spreadsheet.set('a',str(a))
              spreadsheet.set('dia1',str(a))
              Bdia=float(self.le_Bdia.text())
              dia1=float(self.le_dia.text())
              da1=d1 + 2 * mod
              h0=2.25*mod
              df1=da1 - 2 * h0
              if dia1>df1:
                  dia1=df1-1
              spreadsheet.set('dia1',str(dia1) ) 
              dia2=float(self.le_dia2.text())
              spreadsheet.set('dia2',str(dia2) ) 
              spreadsheet.set('Bdia',str(Bdia)) 
              BB=float(self.le_BB.text())   
              spreadsheet.set('BB',str(BB))  
              WB=float(self.le_WB.text())  
              spreadsheet.set('WB',str(WB))  
              self.le_Q.setText(str(Qv))
              w0=float(self.le_Bw.text())
              spreadsheet.set('w0',str(w0))  
              self.label_M.setText(str(mod))
              self.label_N1.setText(str(N1))
              self.label_N2.setText(str(N2))
              self.label_pcd1.setText(str(d1))
              self.label_pcd2.setText(str(d2))
              self.le_a.setText(str(a))
              App.ActiveDocument.recompute()
   
    def create(self): 
         fname=key+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Gear_data',fname) 
         Gui.ActiveDocument.mergeProject(joined_path)

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        