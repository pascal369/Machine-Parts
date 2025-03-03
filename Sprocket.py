# -*- coding: utf-8 -*-
#from curses import keyname
#from ast import Delete
from math import asin, sqrt
import os
#from pickle import TRUE
import sys
import string
#from tkinter.tix import ComboBox
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
from prt_data.CSnap_data import paramCSnap

sprType=['ANSI25','ANSI35','ANSI40','ANSI50','ANSI60','ANSI80','ANSI100','ANSI120',
           'ANSI140','ANSI160','ANSI180','ANSI200','ANSI240',]
sprType2=['ANSI50','ANSI60','ANSI80','ANSI100','ANSI120']
sprShape=['1B','2B','1C','2C','1A','Assy_1B_1B','Assy_1B_1C','Assy_1C_1C']

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
        Dialog.resize(250, 675)
        Dialog.move(1000, 0)
        #タイプ
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 22))
        #形状
        self.label_shape = QtGui.QLabel('Shape',Dialog)
        self.label_shape.setGeometry(QtCore.QRect(10, 42, 100, 12))
        self.comboBox_shape = QtGui.QComboBox(Dialog)
        self.comboBox_shape.setGeometry(QtCore.QRect(110, 35, 100, 22))
        #歯数
        self.label_N = QtGui.QLabel('No of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 68, 100, 12))
        self.comboBox_N = QtGui.QComboBox(Dialog)
        self.comboBox_N.setGeometry(QtCore.QRect(110, 60, 100, 22))
        #穴径
        self.label_dia = QtGui.QLabel('Hole Dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 88, 100, 22))
        self.le_dia = QtGui.QLineEdit('15',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(110, 85, 50, 20))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 110, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 110, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 135, 180, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(25, 170, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        #中心距離
        self.label_L1 = QtGui.QLabel('Plan',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(110, 375, 100, 22))
        self.label_L2 = QtGui.QLabel('Judge',Dialog)
        self.label_L2.setGeometry(QtCore.QRect(160, 375, 100, 22))
        self.label_L = QtGui.QLabel('centerDistance',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 400, 100, 22))
        self.le_Lp = QtGui.QLineEdit('315',Dialog)
        self.le_Lp.setGeometry(QtCore.QRect(110, 400, 40, 20))
        self.le_Lp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Lj = QtGui.QLabel('***',Dialog)
        self.label_Lj.setGeometry(QtCore.QRect(160, 400, 40, 20))
        self.label_Lj.setAlignment(QtCore.Qt.AlignCenter)
        #リンク数
        self.label_Link = QtGui.QLabel('No of Links',Dialog)
        self.label_Link.setGeometry(QtCore.QRect(10, 425, 100, 22))
        self.label_Linkp = QtGui.QLabel('***',Dialog)
        self.label_Linkp.setGeometry(QtCore.QRect(110, 425, 40, 20))
        self.label_Linkp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Linkj = QtGui.QLabel('***',Dialog)
        self.label_Linkj.setGeometry(QtCore.QRect(160, 425, 40, 20))
        self.label_Linkj.setAlignment(QtCore.Qt.AlignCenter)
        #歯数
        self.label_Teeth1 = QtGui.QLabel('No1',Dialog)
        self.label_Teeth1.setGeometry(QtCore.QRect(110, 450, 100, 22))
        self.label_Teeth2 = QtGui.QLabel('No2',Dialog)
        self.label_Teeth2.setGeometry(QtCore.QRect(160, 450, 100, 22))
        self.label_Teeth = QtGui.QLabel('No of Teeth',Dialog)
        self.label_Teeth.setGeometry(QtCore.QRect(10, 475, 100, 22))
        self.label_N1 = QtGui.QLabel('***',Dialog)
        self.label_N1.setGeometry(QtCore.QRect(110, 475, 40, 20))
        self.label_N1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_N2 = QtGui.QLabel('***',Dialog)
        self.label_N2.setGeometry(QtCore.QRect(160, 475, 40, 20))
        self.label_N2.setAlignment(QtCore.Qt.AlignCenter)
        #pitch
        self.label_pitch = QtGui.QLabel('chain pitch',Dialog)
        self.label_pitch.setGeometry(QtCore.QRect(10, 500, 100, 22))
        self.label_pitch1 = QtGui.QLabel('***',Dialog)
        self.label_pitch1.setGeometry(QtCore.QRect(110, 500, 90, 20))
        self.label_pitch1.setAlignment(QtCore.Qt.AlignCenter)
        #pcd
        self.label_pcd = QtGui.QLabel('pcd of Sprocket',Dialog)
        self.label_pcd.setGeometry(QtCore.QRect(10, 525, 100, 22))
        self.label_pcd1 = QtGui.QLabel('***',Dialog)
        self.label_pcd1.setGeometry(QtCore.QRect(110, 525, 40, 20))
        self.label_pcd1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pcd2 = QtGui.QLabel('***',Dialog)
        self.label_pcd2.setGeometry(QtCore.QRect(160, 525, 40, 20))
        self.label_pcd2.setAlignment(QtCore.Qt.AlignCenter)
        #Angle of Sprocket
        self.label_k = QtGui.QLabel('Angle of Sprocket',Dialog)
        self.label_k.setGeometry(QtCore.QRect(10, 550, 100, 22))
        self.label_k1 = QtGui.QLabel('***',Dialog)
        self.label_k1.setGeometry(QtCore.QRect(110, 550, 90, 20))
        self.label_k1.setAlignment(QtCore.Qt.AlignCenter)
        #spinBox
        self.label_spin=QtGui.QLabel('Animation',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 580, 150, 22))
        #spinBox
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(100, 580, 50, 50)
        self.spinBox.setMinimum(0.0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(100.0)  # 最大値を100.0に設定
        self.spinBox.setValue(100.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        #base
        self.label_kiten = QtGui.QLabel('Base',Dialog)
        self.label_kiten.setGeometry(QtCore.QRect(10, 640, 100, 22))
        self.le_kiten = QtGui.QLineEdit('100',Dialog)
        self.le_kiten.setGeometry(QtCore.QRect(110, 640, 100, 20))
        self.le_kiten.setAlignment(QtCore.Qt.AlignCenter)

        #ローラーチェン
        #self.pushButton4 = QtGui.QPushButton('ローラーチェン',Dialog)
        #self.pushButton4.setGeometry(QtCore.QRect(10, 640, 100, 22))
        #sprocket調節
        self.spinBox2=QtGui.QSpinBox(Dialog)
        self.spinBox2.setGeometry(170, 580, 50, 50)
        self.spinBox2.setMinimum(-100.0)  # 最小値を0.0に設定
        self.spinBox2.setMaximum(100.0)  # 最大値を100.0に設定
        self.spinBox2.setValue(0.0)
        self.spinBox2.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_type.addItems(sprType)
        self.comboBox_type.setEditable(True)
        self.comboBox_shape.addItems(sprShape)
        self.comboBox_shape.setEditable(True)
        self.comboBox_N.setEditable(True)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onType)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        #QtCore.QObject.connect(self.pushButton4, QtCore.SIGNAL("pressed()"), self.onChain)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)

        self.comboBox_shape.setCurrentIndex(0)
        self.comboBox_shape.currentIndexChanged[int].connect(self.onType)
        self.comboBox_shape.setCurrentIndex(5)

        self.spinBox.valueChanged[int].connect(self.spinMove)

        self.spinBox2.valueChanged[int].connect(self.setIchi) 

        self.le_kiten.textChanged.connect(self.update_kiten)

        
        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Sprocket", None))
        

    def onType(self):
        global N_Lst
        key=self.comboBox_shape.currentText()
        N0=self.comboBox_N.currentText()
        key2= self.comboBox_shape.currentText()
        fname='Sprocket_'+key2+'.png'
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 
        #print(joined_path)
        #return
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             parts_group = selected_object
             try:
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                             spreadsheet = obj
             except Exception as e:
                 print(f"エラーが発生しました: {e}")
                 #sys.exit(1)  # プログラムを終了する 
                 return  
             try:             
                 key3=spreadsheet.getContents('I2')
             except:
                 return
             if key!=key3[1:]:
                 return
             try:
                 pass
             except:
                 pass
             N_Lst=[]
             #タイプを選択
             for j in range(0,116):
                 type3=spreadsheet.getContents(column_list[j]+str('18'))
                 type0=self.comboBox_type.currentText()
                 if type0==type3[1:]:
                     break
             col_type=j 
             #D0 形状を選択 
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
                 key2=spreadsheet.getContents(column_list[sx]+str('20'))
                 if key==key2[1:]: 
                    break
             col_shp=sx 
             #歯数を設定 
             for i in range(21,57):
                 shp_cell=spreadsheet.getContents(column_list[col_shp]+str(i))
                 if shp_cell!='':
                     break
             col_N=i 
             N_Lst=[] 
             for i in range(col_N,57):
                 N_cell=spreadsheet.getContents(column_list[col_type]+str(i))
                 N_cell2=spreadsheet.getContents(column_list[col_shp]+str(i))
                 if N_cell2!='':
                     N_Lst.append(N_cell)
             string_list = [str(element) for element in N_Lst]
             N_Lst=string_list
             
             self.comboBox_N.clear()
             self.comboBox_N.addItems(N_Lst)
             if self.comboBox_shape.currentText=='2B' or self.comboBox_shape.setCurrentText=='2C':
                 self.comboBox_type.clear()
                 self.comboBox_type.addItems[sprType2]
             elif self.comboBox_shape.setCurrentText=='1C':
                 self.comboBox_type.clear()
                 self.comboBox_type.addItems[sprType[2:]]
             self.comboBox_N.setCurrentText(spreadsheet.getContents('E2'))
        
    def spinMove(self):
        #pass
         #try:
         Pitch=float(self.label_pitch1.text())
         A=self.spinBox.value()
         beta1=360/float(N1)
         beta2=360/float(N2)
         x=10
         #print(N1,N2,beta1)
         spro1.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A*beta1/x)
         spro2.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A*beta2/x)
         #print(A,Pitch,x)
         if A==0:
             return
         self.le_kiten.setText(str(round(A*Pitch/x,3)))
     #except:
     #   return

    def update_kiten(self):
        kiten=self.le_kiten.text()
        #print(kiten)
        #return
        try:
             shtAssy.set('kiten',kiten)
             App.ActiveDocument.recompute() 
        except:
             #Spreadsheet.set('kiten',kiten)
             #App.ActiveDocument.recompute() 
             pass
    def setIchi(self):
        #try:
         selection = Gui.Selection.getSelection()
         if selection:
                 selected_object = selection[0]
                 if selected_object.TypeId == "App::Part":
                     parts_group = selected_object
                     for obj in parts_group.Group:
                         if obj.TypeId == "Spreadsheet::Sheet":
                             spreadsheet = obj
#
                             try:
                                 if selected_object.Label=='spro1' :
                                     A0=float(self.spinBox2.value())*0.5
                                     SP1.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A0)
                                     spreadsheet.set('spr1',str(A0))
                                     App.ActiveDocument.recompute() 
                                 elif selected_object.Label=='spro2' :
                                     A1=float(self.spinBox2.value())*0.5
                                     SP2.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A1)  
                                     spreadsheet.set('spr2',str(A1))  
                                     App.ActiveDocument.recompute() 
                             except:
                                return        
       
                         
    def setParts(self):
     global spro1
     global spro2 
     global SP1
     global SP2
     global chainPath
     global shtAssy
     global shtSpro1
     global shtSpro2
     global shtLink
     doc = FreeCAD.activeDocument()
     if doc:
         group_names = []
         for obj in doc.Objects:
             print(obj.Label)
             if obj.Label=='spro1':
                 spro1=obj
             elif obj.Label=='spro2':
                 spro2=obj 
             elif obj.Label=='SP1':
                 SP1=obj
             elif obj.Label=='SP2':
                 SP2=obj        
             elif obj.Label=='chainPath':
                 chainPath=obj
             elif obj.Label=='shtAssy':
                 shtAssy=obj 
             elif obj.Label=='shtSpro1':
                 shtSpro1=obj 
             elif obj.Label=='shtSpro1':
                 shtSpro2=obj 
             elif obj.Label=='shtLink':
                 shtLink=obj         

     else:  
         return
     
    def read_data(self):
         global type0
         global Lc
         global N1
         global N2
         global pitch
         global Spreadsheet
         try:
             selection = Gui.Selection.getSelection()
         except:
             return
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId =="Spreadsheet::Sheet":
                         spreadsheet = obj
                         
                         if selected_object.Label=='sproAssy':
                             self.comboBox_type.setCurrentText(spreadsheet.getContents('B6')[1:])
                             pass
                         else: 
                             try:
                                 self.comboBox_type.setCurrentText(spreadsheet.getContents('A2')[1:])
                                 type0=self.comboBox_type.currentText()
                             except:
                                 pass 
                             
                             self.comboBox_shape.setCurrentText(spreadsheet.getContents('I2')[1:])
                             myShape=shtAssy.getContents('A1')[1:]
                             self.comboBox_N.setCurrentText(spreadsheet.getContents('E2'))
                             self.le_dia.setText(spreadsheet.getContents('H2')) 
                             key2= self.comboBox_shape.currentText()
                             fname='Sprocket_'+key2+'.png'
                             base=os.path.dirname(os.path.abspath(__file__))
                             joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
                             self.label_6.setPixmap(QtGui.QPixmap(joined_path))  
                         
                         if selected_object.TypeId=='App::Part': 
                                 sht=[]
                                 sht=['spro1','spro2','sproAssy']
                                 for i in range(6):
                                     if  selected_object.Label!='sproAssy':
                                         if i<5:
                                             N0=self.comboBox_N.currentText()
                                             pitch=spreadsheet.getContents('B2')
                                             try:
                                                pcd=round(float(N0)*float(pitch)/3.142,3)
                                                self.onType
                                             except:
                                                 pass
                                 
                                 if selected_object.Label=='spro1':
                                     self.comboBox_shape.setCurrentText(myShape[5:7])
                                     self.label_N1.setText(N0)
                                     self.label_pitch1.setText(str(pitch))
                                     self.label_pcd1.setText(str(pcd))
                                 elif  selected_object.Label=='spro2':
                                     self.comboBox_shape.setCurrentText(myShape[8:10])
                                     self.label_N2.setText(N0) 
                                     self.label_pitch1.setText(str(pitch)) 
                                     self.label_pcd2.setText(str(pcd))
                                 elif selected_object.Label=='sproAssy':
                                     self.comboBox_type.setCurrentText(spreadsheet.getContents('B6')[1:])
                                     Lc=spreadsheet.getContents('CLp')
                                     self.le_Lp.setText(Lc)
                                     N1=spreadsheet.getContents('Teeth1')
                                     N2=spreadsheet.getContents('Teeth2')
                                     pitch=spreadsheet.getContents('Pitch')
                                     pcd1=spreadsheet.getContents('pcd1')
                                     pcd2=spreadsheet.getContents('pcd2')
                                     k1=spreadsheet.getContents('alpha')
                                     Lp=spreadsheet.getContents('Linkp')
                                     Lj=spreadsheet.getContents('Linkj')
                                     CLj=spreadsheet.getContents('CLj')
                                     self.label_N1.setText(N1)
                                     self.label_N2.setText(N2)
                                     self.label_pitch1.setText(pitch)
                                     self.label_pcd1.setText(pcd1)
                                     self.label_pcd2.setText(pcd2)
                                     self.AssyCulc
                                     self.label_k1.setText(k1)
                                     self.label_Linkp.setText(Lp)
                                     self.label_Linkj.setText(Lj)
                                     self.label_Lj.setText(CLj)
                                     
                                     
                                     try:
                                         k1=asin((float(pcd2)/2-float(pcd1)/2)/float(Lc))
                                         k1=round(180-2*k1*57.3,2)
                                         Lp=(float(N1)+float(N2))/2+2*float(Lc)/float(pitch)+\
                                            ((float(N2)-float(N1))/6.28)**2/(float(Lc)/float(pitch))
                                         Lp=round(Lp,2)
                                     except:
                                         return
                                     Lj=int(Lp)
                                     Lcj=(float(pitch)/8)*(2*float(Lp)-float(N1)-float(N2)+\
                                         sqrt((2*float(Lp)-float(N1)-float(N2))**2-(8/9.86)*(float(N2)-float(N1))**2))
                                     Lcj=round(Lcj,2)
                                     self.label_Linkp.setText(str(Lp))
                                     self.label_Linkj.setText(str(Lj))
                                     self.label_Lj.setText(str(Lcj))
                                     self.label_N1.setText(N1)
                                     self.label_N2.setText(N2)
                                     self.label_pitch1.setText(pitch)
                                     self.label_pcd1.setText(pcd1)
                                     self.label_pcd2.setText(pcd2)
                                     self.label_k1.setText(str(k1)+'°')
                                     self.comboBox_shape.setCurrentText('sproAssy')
                                     key2= self.comboBox_shape.currentText()
                                     fname='Sprocket_'+key2+'.png'
                                     base=os.path.dirname(os.path.abspath(__file__))
                                     joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
                                     self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 
                                 else:
                                     self.comboBox_shape.setCurrentText(spreadsheet.getContents('I2')[1:])
                                     self.comboBox_N.setCurrentText(spreadsheet.getContents('E2'))
                                     self.le_dia.setText(spreadsheet.getContents('H2')) 
                                     key2= self.comboBox_shape.currentText()
                                     fname='Sprocket_'+key2+'.png'
                                     base=os.path.dirname(os.path.abspath(__file__))
                                     joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
                                     self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

    def AssyCulc(self):
        global Lcj
        global Lp
        global Lj
        global k1
        global pcd1
        global pcd2
        global pitch
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         N1=self.label_N1.text()
                         N2=self.label_N2.text()
                         pitch=self.label_pitch1.text()
                         Lc=self.le_Lp.text()
                         spreadsheet.set('CLp',Lc)
                         spreadsheet.set('Teeth1',N1)
                         spreadsheet.set('Teeth2',N2)
                         spreadsheet.set('Pitch',pitch)
                         pcd1=self.label_pcd1.text()
                         pcd2=self.label_pcd2.text()

                         k1=asin((float(pcd2)/2-float(pcd1)/2)/float(Lc))
                         k1=round(180-2*k1*57.3,2)
                         Lp=(float(N1)+float(N2))/2+2*float(Lc)/float(pitch)+\
                            ((float(N2)-float(N1))/6.28)**2/(float(Lc)/float(pitch))

                         Lp=round(Lp,2)
                         Lj=int(Lp)
                         Lcj=(float(pitch)/8)*(2*float(Lp)-float(N1)-float(N2)+\
                             sqrt((2*float(Lp)-float(N1)-float(N2))**2-(8/9.86)*(float(N2)-float(N1))**2))
                         Lcj=round(Lcj,2)
                         self.label_Linkp.setText(str(Lp))
                         self.label_Linkj.setText(str(Lj))
                         self.label_Lj.setText(str(Lcj))
                         self.label_k1.setText(str(k1))
                         spreadsheet.set('CLp',Lc)
                         self.comboBox_shape.setCurrentText('sproAssy')
                         key2= self.comboBox_shape.currentText()
                         fname='Sprocket_'+key2+'.png'
                         base=os.path.dirname(os.path.abspath(__file__))
                         joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
                         self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

    def update(self):
         global N0
         global row_N
         global col_type
         global col_shp
         
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         #print(obj.Label)

                         key=self.comboBox_shape.currentText()
                         if selected_object.Label!='sproAssy':
                             key3=spreadsheet.getContents('I2')[1:]
                             if key!=key3:
                                 return
                         
                         if selected_object.Label!='sproAssy':

                            N0=self.comboBox_N.currentText()
                            dia=self.le_dia.text()  
                            #p0 r0 t0 E0を検索
                            for i in range(3,15):
                                type=self.comboBox_type.currentText()
                                type3=spreadsheet.getContents('A'+str(i))
                                
                                if type==type3[1:]:
                                    break
                            row_type=i 
                            p0=spreadsheet.getContents('B'+str(row_type))
                            r0=spreadsheet.getContents('C'+str(row_type))
                            t0=spreadsheet.getContents('D'+str(row_type))
                            E0=spreadsheet.getContents('J'+str(row_type))
                             #タイプを選択
                            for j in range(0,116):
                                type=self.comboBox_type.currentText()
                                type3=spreadsheet.getContents(column_list[j]+str('18'))
                                if type==type3[1:]:
                                    break
                            col_type=j  
                            for m in range(21,56):
                                 N1=spreadsheet.getContents(column_list[col_type]+str(m))
                                 try:
                                     if float(N0)<=float(N1) : 
                                         break 
                                 except:
                                     pass    
                            row_N=m  
                            
                            #D0 形状を選択 
                            for s in range(col_type+1,col_type+4):
                                #print(key)
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
                                key2=spreadsheet.getContents(column_list[sx]+str('20'))
                                if key==key2: 
                                   break
                            col_shp=sx 
                            
                            D0=spreadsheet.getContents(column_list[col_shp]+str(row_N)) 
                            if D0=='':
                                return
                            else: 
                                L0=spreadsheet.getContents(column_list[col_shp+4]+str(row_N)) 

                            spreadsheet.set('A2',type)
                            spreadsheet.set('B2',p0)
                            spreadsheet.set('C2',r0)
                            spreadsheet.set('D2',t0)
                            spreadsheet.set('E2',N0)
                            spreadsheet.set('F2',D0)
                            spreadsheet.set('G2',L0)  
                            spreadsheet.set('H2',dia)  
                            spreadsheet.set('J2',E0) 

                            
                         elif selected_object.Label=='sproAssy':
                             Lc=self.le_Lp.text()
                             spreadsheet.set('CLp',Lc)
                             self.AssyCulc()
                             
                             #リンク型番変更
                             key=self.comboBox_type.currentText()[4:]
                             for i in range(2,14):
                                 key2=shtLink.getContents(column_list[i]+str('2'))
                                 if key==key2:
                                    #print(key,key2)
                                    break
                                                          
                             picth=shtLink.getContents(column_list[i]+str(3))
                             h0=shtLink.getContents(column_list[i]+str(4))
                             t0=shtLink.getContents(column_list[i]+str(5))
                             W0=shtLink.getContents(column_list[i]+str(6))
                             d=shtLink.getContents(column_list[i]+str(7))
                             d2=shtLink.getContents(column_list[i]+str(8))
                             h1=shtLink.getContents(column_list[i]+str(9))

                             shtLink.set(column_list[1]+str(2),key2)
                             shtLink.set(column_list[1]+str(3),picth)
                             shtLink.set(column_list[1]+str(4),h0)
                             shtLink.set(column_list[1]+str(5),t0)
                             shtLink.set(column_list[1]+str(6),W0)
                             shtLink.set(column_list[1]+str(7),d)
                             shtLink.set(column_list[1]+str(8),d2)
                             shtLink.set(column_list[1]+str(9),h1)

                             shtAssy.set('Type','ANSI'+str(key))
                             shtAssy.set('CLj',str(Lcj))
                             shtAssy.set('Linkp',str(Lp))
                             shtAssy.set('Linkj',str(Lj))
                             shtAssy.set('CLp',Lc)
                             shtAssy.set('CLj',str(Lcj))
                             shtAssy.set('alpha',str(k1))
                             shtAssy.set('pcd1',str(pcd1))
                             shtAssy.set('pcd2',str(pcd2))
                             shtAssy.set('alpha',str(k1))

                         App.ActiveDocument.recompute() 
                         return
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
        # 閉じるボタンを無効にする
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
