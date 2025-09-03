# -*- coding: utf-8 -*-
import os
import sys
import string
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from . import RollingBrg_Data

type=['DoubleRow',]
#series500SP=['06x10','08x12','10x14','12x18','13x19','14x20','15x21','16x22','17x23','18x24',
#             '19x26','20x28','20x30','22x32','25x33','25x35','28x38','30x38','30x40','31.5x40',
#             '32x42','35x44','35x45','38x48','40x50','40x55','45x55','45x56','45x60',]

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
        #global fname
        #global joined_path
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 350)
        Dialog.move(1000, 0)
        #和文
        self.pushButton_la = QtGui.QPushButton('JPN Text',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(10, 10, 30, 22))
        self.le_la = QtGui.QLineEdit('円錐ころ軸受',Dialog)
        self.le_la.setGeometry(QtCore.QRect(100, 10, 160, 20))
        self.le_la.setAlignment(QtCore.Qt.AlignLeft) 
        #タイプ　Type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 38, 120, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 35, 165, 22))

        #シリーズ　Series
        self.label_ser = QtGui.QLabel('Series',Dialog)
        self.label_ser.setGeometry(QtCore.QRect(10, 63, 50, 12))
        self.label_ser.setAlignment(QtCore.Qt.AlignRight)
        self.comboBox_ser = QtGui.QComboBox(Dialog)
        self.comboBox_ser.setGeometry(QtCore.QRect(80, 60, 80, 22))

        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 88, 50, 12))
        self.label_dia.setAlignment(QtCore.Qt.AlignRight)
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 85, 80, 22))
        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 110, 180, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(140, 135, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        #self.pushButton2.setGeometry(QtCore.QRect(80, 110, 40, 22))
        self.pushButton2.setGeometry(QtCore.QRect(50,135,80,22))
        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(80, 170, 250, 200))
        self.label_5.setAlignment(QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")
        pic='Tapered Roller Bearings.png'  
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,'png_data',pic)
        #print(joined_path,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

        self.comboBox_type.addItems(type)
        self.comboBox_ser.addItems(RollingBrg_Data.TprSer)
        self.comboBox_dia.addItems(RollingBrg_Data.TprDia)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_type.setCurrentIndex(0)
        
        #self.comboBox_ser.setEditable(True)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia)
        self.comboBox_dia.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        #QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.readData)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "TaperedRollerBrg", None))
    def japan(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label=obj.Label
        JPN=self.le_la.text()
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN
    def readData(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                JPN=obj.JPN
                self.le_la.setText(JPN)
            except:
                pass
        if selection:
            selected_object = selection[0]
            if selected_object.TypeId == "App::Part":
                parts_group = selected_object
                for obj in parts_group.Group:
                    #print(obj.Label)
                    if obj.TypeId =="Spreadsheet::Sheet":
                        spreadsheet = obj
            self.comboBox_type.setCurrentText(spreadsheet.getContents('B1'))                
            self.comboBox_ser.setCurrentText(spreadsheet.getContents('A1'))            
            self.comboBox_dia.setCurrentText(spreadsheet.getContents('A3'))
            #print(self.comBox_dia.CurrentText())
    #def onSereis(self):
    #    key0=self.comboBox_ser.currentTex()   
    #    if key0== '02': 
    
    def onType(self):
        #return
        key0=self.comboBox_type.currentIndex()
        if key0==0:
            self.le_la.setText('複列円錐ころ軸受')
            spreadsheet.set('B1','DoubleRow')
        elif key0==1:
            self.le_la.setText('単列円錐ころ軸受')  
            spreadsheet.set('B1','SingleRow')  
        
    def onDia(self):
         global d
         global D
         global T0
         global b
         global r
         global r1
         global n
         global x
         global z
         global l0
         global xk
         global yk
         global xi
         global d1
         global g
         #global listL
         key=self.comboBox_dia.currentText()
         key0=self.comboBox_ser.currentText()
         listL=[]
         if key0=='02':
             a=3
             b=27
         elif key0=='03':
             return  
         for i in range(a,b):
             if key==spreadsheet.getContents('A'+str(i)):
                 #print(i,key,spreadsheet.getContents('A'+str(i)))
                 for i in range(3,27):
                     if key==spreadsheet.getContents('A'+str(i)):
                         listL=[]
                         for j in range(0,17):
                             listL.append(spreadsheet.getContents(column_list[j]+str(i)))
                         d=listL[0]
                         D=listL[1]
                         T0=listL[2]
                         b=listL[3]
                         r=listL[4]
                         r1=listL[5]
                         n=listL[6]
                         x=listL[7]
                         z=listL[8]
                         l0=listL[9]
                         d1=listL[10]
                         #d2=listL[11]
                         xi=listL[12]
                         xk=listL[13]
                         yk=listL[14]
                         g=listL[16]
    def upDate(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        spreadsheet.set('d',d)
        spreadsheet.set('D',D)
        spreadsheet.set('T0',T0)
        spreadsheet.set('b',b)
        spreadsheet.set('r',r)
        spreadsheet.set('r1',r1)
        spreadsheet.set('n',n)
        spreadsheet.set('x',x)
        spreadsheet.set('z',z)
        spreadsheet.set('l0',l0)
        spreadsheet.set('d1',d1)
        spreadsheet.set('xi',xi)
        spreadsheet.set('xk',xk)
        spreadsheet.set('yk',yk)
        spreadsheet.set('g0',g)

        JPN=self.le_la.text()
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN
        try:
            #label='mass[kg]'
            print(g)
            obj.addProperty("App::PropertyString", "mass",'mass[kg]').mass=g
            print(g)
        except:
            obj.mass=g
            print('error')
            pass
    
        App.ActiveDocument.recompute()      

    def create(self):
        #print(key)
        key00=self.comboBox_type.currentText()
        key=self.comboBox_ser.currentIndex()
        if key00=='SingleRow':
            #print(key)
            if key==0:
                fname='TaperedRollerBrg_SingleRow02.FCStd'
            elif key==1:
                fname='TaperedRollerBrg_SingleRow03.FCStd'
        elif key00=='DoubleRow':
            #print(key)
            if key==0:
                fname='TaperedRollerBrg_DoubleRow02.FCStd'
            elif key==1:
                fname='TaperedRollerBrg_DoubleRow03.FCStd'        
        else:
            #return
            pass
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, fname) 
        print(joined_path)
        try:
           Gui.ActiveDocument.mergeProject(joined_path)
        except:
           doc=App.newDocument()
           Gui.ActiveDocument.mergeProject(joined_path)

        #obj.addProperty("App::PropertyString", "JPN",'Base')
        #obj.JPN=JPN
#
        #label='mass[kg]'
        #obj.addProperty("App::PropertyEnumeration", "mass",label)
        #obj.mass=g
        #print('aaaaaaaaaaaaaaaaaaaaaaa')
        return  

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
