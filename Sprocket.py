# -*- coding: utf-8 -*-
#from curses import keyname
#from ast import Delete
from math import asin, sqrt
import os
import math
#from pickle import TRUE
import sys
import string
import Part
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
#from prt_data.CSnap_data import paramCSnap

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
        #クリヤ
        self.pushButton4 = QtGui.QPushButton('Clear Data',Dialog)
        self.pushButton4.setGeometry(QtCore.QRect(50, 160, 180, 22))
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
        QtCore.QObject.connect(self.pushButton4, QtCore.SIGNAL("pressed()"), self.setClear)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onType)
        
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
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             parts_group = selected_object
             try:
                 for obj in parts_group.Group:
                     if obj.Label[:8] == "shtSproP" or obj.Label[8:]=='shtSproG':
                             sht_X = obj
             except Exception as e:
                 print(f"エラーが発生しました: {e}")
                 #sys.exit(1)  # プログラムを終了する 
                 return  
             try:             
                 key3=sht_X.getContents('I2')
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
                 type3=sht_X.getContents(column_list[j]+str('18'))
                 type0=self.comboBox_type.currentText()
                 if type0==type3[1:]:
                     break
             col_type=j 
             #print(col_type)
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
                 key2=sht_X.getContents(column_list[sx]+str('20'))
                 if key==key2[1:]: 
                    break
             col_shp=sx 
             #歯数を設定 
             for i in range(21,57):
                 shp_cell=sht_X.getContents(column_list[col_shp]+str(i))
                 if shp_cell!='':
                     break
             col_N=i 
             N_Lst=[] 
             for i in range(col_N,57):
                 N_cell=sht_X.getContents(column_list[col_type]+str(i))
                 N_cell2=sht_X.getContents(column_list[col_shp]+str(i))
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
             self.comboBox_N.setCurrentText(sht_X.getContents('E2'))
        
    def spinMove(self):
         try:
             Pitch=float(self.label_pitch1.text())
             A=self.spinBox.value()
             beta1=360/float(N1)
             beta2=360/float(N2)
             x=10
             #print(N1,N2,beta1)
             sproP.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A*beta1/x)
             sproG.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A*beta2/x)
             #print(A,Pitch,x)
             if A==0:
                 return
             self.le_kiten.setText(str(round(A*Pitch/x,3)))
         except:
             return

    def update_kiten(self):
        kiten=self.le_kiten.text()
        try:
             shtAssy.set('kiten',kiten)
             App.ActiveDocument.recompute() 
        except:
             pass
    def setIchi(self):
         selection = Gui.Selection.getSelection()
         if selection:
                 selected_object = selection[0]
                 if selected_object.TypeId == "App::Part":
                     parts_group = selected_object
                     for obj in parts_group.Group:
                         if obj.Label[:7]=='sP':
                             sP = obj
                         elif obj.Label[:7]=='sG':
                             sG = obj    

                     try:
                         #print('cccccccccccccccc')
                         if selected_object.Label=='sproP' :
                             A0=float(self.spinBox2.value())*0.5
                             sP.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A0)
                             shtAssy.set('spr1',str(A0))
                             App.ActiveDocument.recompute() 
                         elif selected_object.Label=='sproG' :
                             #print('cccccccccccccccc')
                             A1=float(self.spinBox2.value())*0.5
                             sG.Placement.Rotation=App.Rotation(App.Vector(0,1,0),A1)  
                             shtAssy.set('spr2',str(A1))  
                             App.ActiveDocument.recompute() 
                     except:
                        return        
                         
    #def setParts(self):
    # global sproP
    # global sproG 
    # global sP
    # global sG
    # global chainPath
    # global shtAssy
    # global shtsproP
    # global shtsproG
    # global shtLink
    # doc = FreeCAD.activeDocument()
    # if doc:
    #     group_names = []
    #     for obj in doc.Objects:
    #         if obj.Label[:5]=='sproP':
    #             sproP=obj
    #         elif obj.Label[:5]=='sproG':
    #             sproG=obj 
    #         elif obj.Label[:2]=='sP':
    #             sP=obj
    #         elif obj.Label[:2]=='sG':
    #             sG=obj        
    #         elif obj.Label[:9]=='chainPath':
    #             chainPath=obj
    #         elif obj.Label[:7]=='shtAssy':
    #             shtAssy=obj 
    #         elif obj.Label[:8]=='shtsproP':
    #             shtsproP=obj 
    #         elif obj.Label[:8]=='shtsproG':
    #             shtsproG=obj 
    #         elif obj.Label[:7]=='shtLink':
    #             shtLink=obj         
    def setClear(self):
        Gui.Selection.clearSelection()

    def read_data(self):
         #global type0
         global Lc
         global N1
         global N2
         global pitch
         global sht_X
         global shtAssy
         global shtSproP
         global shtSproG
         global sproP
         global sproG
         global sP
         global sG
         global Sketch_P
         global shtLink
         
         selection = Gui.Selection.getSelection()
         if selection:
            selected_object = selection[0]
            if selected_object.TypeId == "App::Part":
                parts_group = selected_object
                for obj in parts_group.Group:
                    #print(obj.Label)
                    if obj.Label[:5]=='sproP':
                        sproP=obj
                    elif obj.Label[:5]=='sproG':
                        sproG=obj 
                    elif obj.Label[:2]=='sP':
                        sP=obj
                    elif obj.Label[:2]=='sG':
                        sG=obj        
                    elif obj.Label[:8]=='Sketch_P':
                        Sketch_P=obj
                    elif obj.Label[:7]=='shtAssy':
                        shtAssy=obj 
                    elif obj.Label[:8]=='shtSproP':
                        shtSproP=obj 
                    elif obj.Label[:8]=='shtSproG':
                        shtSproG=obj 
                    elif obj.Label[:7]=='shtLink':
                        shtLink=obj  
                    elif obj.Label[:5]=='sht_X':
                        sht_X=obj      

                for i in range(6):
                    if  selected_object.Label[:8]!='sproAssy':
                        if selected_object.Label[:5]=='sproP':
                            sht_X=shtSproP
                        elif selected_object.Label[:5] =='sproG':
                            sht_X=shtSproG
                        else:
                            return
                    
                        self.comboBox_type.setCurrentText(sht_X.getContents('A2')[1:])  
                        self.comboBox_shape.setCurrentText(sht_X.getContents('I2')[1:])
                        self.comboBox_N.setCurrentText(sht_X.getContents('E2'))
                        self.le_dia.setText(sht_X.getContents('H2')) 
                        if i<5:
                            N0=self.comboBox_N.currentText()
                            pitch=sht_X.getContents('B2')
                            try:
                               pcd=round(float(N0)*float(pitch)/3.142,0)
                               self.onType
                            except:
                                pass

                        if selected_object.Label[:5]=='sproP':
                            self.comboBox_shape.addItems(sprShape[:5])
                            self.label_N1.setText(N0)
                            self.label_pitch1.setText(str(pitch))
                            self.label_pcd1.setText(str(pcd))
                        elif  selected_object.Label[:5]=='sproG':
                            self.comboBox_shape.addItems(sprShape[:5])
                            self.label_N2.setText(N0) 
                            self.label_pitch1.setText(str(pitch)) 
                            self.label_pcd2.setText(str(pcd))
                    elif selected_object.Label[:8]=='sproAssy':
                        self.comboBox_type.setCurrentText(shtAssy.getContents('B6')[1:])
                        Lc=shtAssy.getContents('CLp')
                        self.le_Lp.setText(Lc)
                        N1=shtAssy.getContents('Teeth1')
                        N2=shtAssy.getContents('Teeth2')
                        pitch=shtAssy.getContents('Pitch')
                        pcd1=shtAssy.getContents('pcd1')
                        pcd2=shtAssy.getContents('pcd2')
                        k1=shtAssy.getContents('alpha')
                        Lp=shtAssy.getContents('Linkp')
                        Lj=shtAssy.getContents('Linkj')
                        CLj=shtAssy.getContents('CLj')
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
                        self.comboBox_shape.setCurrentText(sht_X.getContents('I2')[1:])
                        self.comboBox_N.setCurrentText(sht_X.getContents('E2'))
                        self.le_dia.setText(sht_X.getContents('H2')) 
                        key2= self.comboBox_shape.currentText()
                        fname='Sprocket_'+key2+'.png'
                        base=os.path.dirname(os.path.abspath(__file__))
                        joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
                        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 

    def AssyCulc(self):
        #global Lcj
        global Lp
        global Lj
        global k1
        global pcd1
        global pcd2
        global pitch

        N1=self.label_N1.text()
        N2=self.label_N2.text()
        pitch=self.label_pitch1.text()
        Lc=self.le_Lp.text()
        shtAssy.set('CLp',Lc)
        shtAssy.set('Teeth1',N1)
        shtAssy.set('Teeth2',N2)
        shtAssy.set('Pitch',pitch)
        pcd1=self.label_pcd1.text()
        pcd2=self.label_pcd2.text()
        #print(pcd1,pcd2)
        k1=asin((float(pcd2)/2-float(pcd1)/2)/float(Lc))
        k1=round(180-2*k1*57.3,2)

        #pathLength
        total_length = 0.0
        edges = Sketch_P.Geometry  # スケッチ内のジオメトリリスト
        for edge in edges:
          #if isinstance(edge, (Part.Line, Part.LineSegment, Part.Circle, Part.ArcOfCircle, Part.Ellipse, Part.ArcOfEllipse)):  # エッジのみ対象
           if isinstance(edge, (Part.LineSegment, Part.ArcOfCircle )):  # エッジのみ対象 
              total_length += edge.length()
        Lp=total_length/float(pitch)
        Lp=round(Lp,2)
        Lj=int(Lp)

        self.label_Linkp.setText(str(Lp))
        self.label_Linkj.setText(str(Lj))
        self.label_Lj.setText(str(Lc))


        self.label_k1.setText(str(k1))
        shtAssy.set('CLp',Lc)
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
         
         key=self.comboBox_shape.currentText()
         
         if key!='sproAssy':
             N0=self.comboBox_N.currentText()
             dia=self.le_dia.text()  
             #p0 r0 t0 E0を検索
             for i in range(3,15):
                 type=self.comboBox_type.currentText()
                 type3=sht_X.getContents('A'+str(i))
                 
                 if type==type3[1:]:
                     break
             row_type=i 
             p0=sht_X.getContents('B'+str(row_type))
             r0=sht_X.getContents('C'+str(row_type))
             t0=sht_X.getContents('D'+str(row_type))
             #E0=sht_X.getContents('J'+str(row_type))
             if sht_X.Label=='shtSproP':
                 N1=N0
                 pcd1=int(float(p0)/(math.sin(3.142/float(N0))))
                 shtAssy.set('Teeth1',N1)
             elif sht_X.Label=='shtSproG':
                 N2=N0
                 pcd2=int(float(p0)/(math.sin(3.142/float(N0))))   
                 shtAssy.set('Teeth2',N2) 
             #タイプを選択
             for j in range(0,116):
                 type=self.comboBox_type.currentText()
                 type3=sht_X.getContents(column_list[j]+str('18'))
                 #print(type,type3)
                 if type==type3[1:]:
                     break
             col_type=j  
             for m in range(21,56):
                  N1=sht_X.getContents(column_list[col_type]+str(m))
                  try:
                      if float(N0)<=float(N1) : 
                          break 
                  except:
                      pass    
             row_N=m  

             #D0 形状を選択 
             for s in range(col_type+1,col_type+4):
                 #print(s)
                 if key=='1B':
                     sx=s-2
                 elif key=='2B':
                     sx=s-2
                 elif key=='1C':
                     sx=s
                 elif key=='2C':
                     sx=s+1
                 #elif key=='1A':
                 #    sx=s-2
                 key2=sht_X.getContents(column_list[s]+str('20'))
                 #print(sx,key,key2[1:])
                 if key==key2[1:]: 
                    #print(sx,key,key2[1:])
                    break
                 col_shp=sx 
             
             D0=sht_X.getContents(column_list[sx]+str(m)) 
             print(sx,m,D0)
             if D0=='':
                 return
             else: 
                 L0=sht_X.getContents(column_list[sx+4]+str(m)) 

             #print(D0,L0)
            
             sht_X.set('A2',type)
             sht_X.set('B2',p0)
             sht_X.set('C2',r0)
             sht_X.set('D2',t0)
             sht_X.set('E2',N0)
             sht_X.set('F2',D0)
             sht_X.set('G2',L0)  
             sht_X.set('H2',dia)  

             App.ActiveDocument.recompute()   

         elif key=='sproAssy':
             Lc=self.le_Lp.text()
             shtAssy.set('CLj',Lc)
             self.AssyCulc()
             
             #リンク型番変更
             type=self.comboBox_type.currentText()[4:]
             for i in range(2,14):
                 key2=shtLink.getContents(column_list[i]+str('2'))
                 #print(type,key2)
                 if type==key2:
                    #print(key,key2)
                    break
             shtAssy.set('Linkp',str(Lp))
             shtAssy.set('Linkj',str(Lj))     

         type=self.comboBox_type.currentText()                                
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
         shtAssy.set('Type',type)
         shtAssy.set('Pitch',pitch)

         try:
             if sht_X.Label=='shtSproP':
                 shtAssy.set('pcd1',str(pcd1))
             elif sht_X.Label=='shtSproG':    
                 shtAssy.set('pcd2',str(pcd2))
         except:
             pass

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
        # 閉じるボタンを無効にする
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
