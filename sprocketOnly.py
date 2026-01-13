# -*- coding: utf-8 -*-
from math import asin, sqrt
import os
import math
import sys
import string
import Part
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCAD
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

sprType=['ANSI25','ANSI35','ANSI40','ANSI50','ANSI60','ANSI80','ANSI100','ANSI120',
           'ANSI140','ANSI160','ANSI180','ANSI200','ANSI240',]
sprShape=['1B','1C','1A',]

sprTeeth=[i for i in range(9,75)]
string_list = [str(element) for element in sprTeeth]
sprTeeth=string_list

sprIchi=[i for i in range(1,100)]
string_list2 = [str(element) for element in sprIchi]
sprIchi=string_list2

# 画面を並べて表示する
class Ui_Dialog(object):
    global column_list
    alphabet_list = list(string.ascii_uppercase)
    column_list=[]
    for i in range(0,26):
        column_list.append(alphabet_list[i])
    for i in range(0,26):
        for j in range(0,26):
            column_list.append(alphabet_list[i] + alphabet_list[j])
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 350)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 10, 100, 20))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 9, 100, 20))
        self.comboBox_type.setEditable(True)
        self.comboBox_type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #形状
        self.label_shape = QtGui.QLabel('Shape',Dialog)
        self.label_shape.setGeometry(QtCore.QRect(10, 42, 100, 20))
        self.label_shape.setStyleSheet("color: black;")
        self.comboBox_shape = QtGui.QComboBox(Dialog)
        self.comboBox_shape.setGeometry(QtCore.QRect(110, 35, 100, 20))
        self.comboBox_shape.setEditable(True)
        self.comboBox_shape.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #歯数
        self.label_N = QtGui.QLabel('No of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 65, 100, 20))
        self.label_N.setStyleSheet("color: black;")
        self.comboBox_N = QtGui.QComboBox(Dialog)
        self.comboBox_N.setGeometry(QtCore.QRect(110, 61, 100, 20))
        self.comboBox_N.setEditable(True)
        self.comboBox_N.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #穴径
        self.label_dia = QtGui.QLabel('Hole Dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 87, 100, 20))
        self.label_dia.setStyleSheet("color: black;")
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(110, 88, 100, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(40, 115, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(135, 115, 55, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(40, 140, 185, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(25, 160, 200, 190))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        fname=''
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

        self.comboBox_type.addItems(sprType)
        self.comboBox_type.setEditable(True)
        self.comboBox_shape.addItems(sprShape)
        self.comboBox_shape.setEditable(True)
        self.comboBox_N.setEditable(True)
        self.comboBox_N.addItems(sprTeeth)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onType)
        #QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        #QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)

        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        
        self.comboBox_shape.setCurrentIndex(1)
        self.comboBox_shape.currentIndexChanged[int].connect(self.onShape)
        self.comboBox_shape.setCurrentIndex(0)

        self.comboBox_N.setCurrentText('30')

        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Sprocket", None))
    def onShape(self):
        pic=self.comboBox_shape.currentText()
        fname='Sprocket_' + pic + '.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

    def onType(self):
        global N_Lst
        global sx
        key=self.comboBox_shape.currentText()
        N0=self.comboBox_N.currentText()
        for k in range(2):
            try:
                if k==0:
                    shtSproB=shtSproB
            except:
                return         
            N_Lst=[]
            #タイプを選択
            for j in range(0,116):
                type3=shtSproB.getContents(column_list[j]+str('18'))
                type0=self.comboBox_type.currentText()
                if type0==type3[1:]:
                    break
            col_type=j 

            for s in range(col_type+1,col_type+4):
                if key=='1B':
                    sx=s-2
                elif key=='2B':
                    sx=s-1
                elif key=='1C':
                    sx=s
                elif key=='2C':
                    sx=s+1    
                elif key=='1A':
                    sx=s-2
                key2=shtSproB.getContents(column_list[sx]+str('20'))
                if key==key2[1:]: 
                   break
            col_shp=sx 
            #歯数を設定 
            for i in range(21,57):
                shp_cell=shtSproB.getContents(column_list[col_shp]+str(i))
                if shp_cell!='':
                    break
            col_N=i 
            N_Lst=[] 
            for i in range(col_N,57):
                N_cell=shtSproB.getContents(column_list[col_type]+str(i))
            string_list = [str(element) for element in N_Lst]
            N_Lst=string_list
            
            if k==0:
                 self.comboBox_N.clear()
                 self.comboBox_N.addItems(N_Lst)
            try:    
                self.comboBox_N.setCurrentText(shtSproB.getContents('B7'))
            except:
                return
    
    def read_data(self):
         global shtSproB
         selection = Gui.Selection.getSelection()
         if selection:
            selected_object = selection[0]
            if selected_object.TypeId == "App::Part":
                parts_group = selected_object
                for obj in parts_group.Group:
                    if obj.Label[:8]=='shtSproB':
                        shtSproB=obj 
                      
                self.comboBox_type.setCurrentText(shtSproB.getContents('A2')[1:])  
                self.comboBox_shape.setCurrentText(shtSproB.getContents('A1')[1:])
                self.le_dia.setText(shtSproB.getContents('dia'))
                N1=shtSproB.getContents('N0')
                self.comboBox_N.setCurrentText(N1)
                #pitch=shtSproB.getContents('p0')
                #pcd=shtSproB.getContents('pcd')

    def update(self):
         global b0
         global N0
         global row_N
         global col_type
         global col_shp
         global sx
         key=self.comboBox_shape.currentText()
         for k in range(2):
             if k==0:
                 N0=self.comboBox_N.currentText()
                 dia=self.le_dia.text()  
             for i in range(3,15):
                 type=self.comboBox_type.currentText()
                 type3=shtSproB.getContents('A'+str(i))
                 if type==type3[1:]:
                     break
             row_type=i 
             p0=shtSproB.getContents('B'+str(row_type))
             r0=shtSproB.getContents('C'+str(row_type))
             t0=shtSproB.getContents('D'+str(row_type))
             shtSproB.set('p0',p0)
             if shtSproB.Label=='shtSproB':
                 N1=N0
                 pcd1=int(float(p0)/(math.sin(3.142/float(N0))))
                 shtSproB.set('N0',N1)
             #タイプを選択
             for j in range(0,116):
                 type=self.comboBox_type.currentText()
                 type3=shtSproB.getContents(column_list[j]+str('18'))
                 if type==type3[1:]:
                     break
             col_type=j  
             for m in range(21,56):
                  N1=shtSproB.getContents(column_list[col_type]+str(m))
                  try:
                      if float(N0)<=float(N1) : 
                          break 
                  except:
                      pass    
             row_N=m  
             #D0 形状を選択 
             key2= self.comboBox_shape.currentText()
             for s in range(col_type,col_type+4):   
                 if key=='1B':
                     sx=s-2
                 elif key=='2B':
                     sx=s-2
                 elif key=='1C':
                     sx=s
                 elif key=='2C':
                     sx=s+1
                 elif key=='1A':
                    sx=s-2    
                 key2=shtSproB.getContents(column_list[s]+str('20'))
                 if key==key2[1:]: 
                    break
                 col_shp=sx 
             D0=shtSproB.getContents(column_list[sx]+str(m)) 
             if D0=='':
                 return
             else: 
                L0=shtSproB.getContents(column_list[sx+4]+str(m)) 
             shtSproB.set('A2',type)
             shtSproB.set('B2',p0)
             shtSproB.set('C2',r0)
             shtSproB.set('D2',t0)
             shtSproB.set('E2',N0)
             shtSproB.set('F2',D0)
             shtSproB.set('G2',L0)  
             shtSproB.set('H2',dia)  
             shtSproB.set('type',type)
             App.ActiveDocument.recompute() 

    def create(self): 
         shp=self.comboBox_shape.currentText()
         fname='Sprocket_'+shp+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Spro_data',fname) 
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
        