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
#from prt_data.BallBrg_data import ParamBallBrg
#from prt_data.plainBrg_data import BearingData
type=['bushing_500SP',]
series500SP=['06x10','08x12','10x14','12x18','13x19','14x20','15x21','16x22','17x23','18x24',
             '19x26','20x28','20x30','22x32','25x33','25x35','28x38','30x38','30x40','31.5x40',
             '32x42','35x44','35x45','38x48','40x50','40x55','45x55','45x56','45x60',]

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
        global fname
        global joined_path
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 325)
        Dialog.move(1000, 0)
        #和文
        self.pushButton_la = QtGui.QPushButton('JPN Text',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(10, 10, 30, 22))
        self.le_la = QtGui.QLineEdit('すべり軸受',Dialog)
        self.le_la.setGeometry(QtCore.QRect(105, 10, 155, 22))
        self.le_la.setAlignment(QtCore.Qt.AlignCenter) 
        #タイプ　Type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 38, 120, 22))
        self.label_type.setStyleSheet("color: gray;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 35, 180, 22))
        self.comboBox_type.setEditable(True)
        self.comboBox_type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        #シリーズ　Series
        self.label_ser = QtGui.QLabel('Series(d*D)',Dialog)
        self.label_ser.setGeometry(QtCore.QRect(10, 63, 120, 12))
        self.label_ser.setStyleSheet("color: gray;")
        self.comboBox_ser = QtGui.QComboBox(Dialog)
        self.comboBox_ser.setGeometry(QtCore.QRect(80, 63, 80, 22))

        #長さ
        self.label_length = QtGui.QLabel('Length(L)',Dialog)
        self.label_length.setGeometry(QtCore.QRect(10, 90, 150, 12))
        self.label_length.setStyleSheet("color: gray;")
        self.comboBox_length = QtGui.QComboBox(Dialog)
        self.comboBox_length.setGeometry(QtCore.QRect(80, 90, 80, 22))
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 125, 205, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(115, 150, 140, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(50, 150, 60, 22))

        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 185, 200, 150))
        self.label_5.setAlignment(QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")
        pic='bushing_500SP.png'  
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'plainBrg_data',pic)
        print(joined_path)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

        self.comboBox_type.addItems(type)


        #self.comboBox_ser.setCurrentIndex(1)
        #self.comboBox_ser.currentIndexChanged[int].connect(self.onSeries)
        #self.comboBox_ser.setCurrentIndex(0)

        self.comboBox_ser.addItems(series500SP)
        self.comboBox_ser.setEditable(True)
        self.comboBox_length.setEditable(True)

        self.comboBox_ser.setCurrentIndex(1)
        self.comboBox_ser.currentIndexChanged[int].connect(self.onSeries)
        self.comboBox_ser.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.readData)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onSeries)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "plainBearing", None))
        self.label_type.setText(QtGui.QApplication.translate("Dialog", "Type", None)) 
        self.label_ser.setText(QtGui.QApplication.translate("Dialog", "Series(d*D)", None)) 
        self.label_length.setText(QtGui.QApplication.translate("Dialog", "Length(L)", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
    
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
        global spreadsheet_500SP
        global bushing500SP
        selection = Gui.Selection.getSelection()
        if selection:
            selected_object = selection[0]
            if selected_object.TypeId == "App::Part":
                parts_group = selected_object
                for obj in parts_group.Group:
                    print(obj.Label)
                    if obj.Label=='Spreadsheet_500SP':
                        spreadsheet_500SP=obj
                    elif obj.Label =="bushing500SP":
                        bushing500SP=obj
                        #print(spreadsheet.getContents('A2'))
                self.comboBox_ser.setCurrentText(spreadsheet_500SP.getContents('A2')[1:])
                self.comboBox_length.setCurrentText(spreadsheet_500SP.getContents('D2'))
         
    def onType(self):
        key0=self.comboBox_type.currentIndex()
        if key0==0:
            self.comboBox_ser.addItems(series500SP)
        
    def onSeries(self):
         global series
         global i
         global dia
         global outDia
         key=self.comboBox_ser.currentText()
         listL=[]
         for i in range(3,36):
             if key==spreadsheet_500SP.getContents('A'+str(i))[1:]:
                 print(i,key,spreadsheet_500SP.getContents('A'+str(i))[1:])
                 for i in range(3,36):
                     if key==spreadsheet_500SP.getContents('A'+str(i))[1:]:
                         listL=[]
                         for j in range(3,13):
                             listL.append(spreadsheet_500SP.getContents(column_list[j]+str(i)))

                         self.comboBox_length.clear()           
                         self.comboBox_length.addItems(listL)
                         series=self.comboBox_ser.currentText()

                         #dia=spreadsheet_500SP.getContents(column_list[1]+str(i))
                         #outDia=spreadsheet_500SP.getContents(column_list[2]+str(i))
                 dia=spreadsheet_500SP.getContents('dia')
                 outDia=spreadsheet_500SP.getContents('outDia')  

                 print(dia,outDia)       
                 
         
    def upDate(self):
        #c00 = Gui.Selection.getSelection()
        #if c00:
        #    obj = c00[0]
        length=self.comboBox_length.currentText()
        print('outDia=',outDia)
        spreadsheet_500SP.set('series',series)
        spreadsheet_500SP.set('dia',dia)
        spreadsheet_500SP.set('outDia',outDia)
        spreadsheet_500SP.set('length',length)
        App.ActiveDocument.recompute() 

        #JPN=self.le_la.text()
        #try:
        #    obj.addProperty("App::PropertyString", "JPN",'Base')
        #    obj.JPN=JPN
        #except:
        #    obj.JPN=JPN
       
        label='mass[kg]'
        g0=7.85
        g=bushing500SP.Shape.Volume*g0*1000/10**9  
        try:
            bushing500SP.addProperty("App::PropertyFloat", "mass",label)
            bushing500SP.mass=g
        except:
            pass
        Standard=self.comboBox_ser.currentText()
        try:
            bushing500SP.addProperty("App::PropertyString", "Standard",'Base')
            bushing500SP.Standard=Standard
        except:
            bushing500SP.Standard=Standard

    def create(self): 
        fname='bushing_500SP.FCStd'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'prt_data','plainBrg_data',fname) 
        try:
           Gui.ActiveDocument.mergeProject(joined_path)
        except:
           doc=App.newDocument()
           Gui.ActiveDocument.mergeProject(joined_path)
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
