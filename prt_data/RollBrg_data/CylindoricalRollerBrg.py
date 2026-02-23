# -*- coding: utf-8 -*-
import os
import sys
import string
import Import
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from . import RollingBrg_Data

type=['Cylindorical Roller Bearings',]
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
        global fname
        global joined_path
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 350)
        Dialog.move(1000, 0)
        #和文
        self.pushButton_la = QtGui.QPushButton('JPN Text',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(10, 10, 30, 22))
        self.le_la = QtGui.QLineEdit('円筒ころ軸受',Dialog)
        self.le_la.setGeometry(QtCore.QRect(105, 10, 160, 22))
        self.le_la.setAlignment(QtCore.Qt.AlignLeft) 

        #シリーズ　Series
        self.label_ser = QtGui.QLabel('Series',Dialog)
        self.label_ser.setGeometry(QtCore.QRect(10, 35, 50, 22))
        self.label_ser.setAlignment(QtCore.Qt.AlignRight)
        self.label_ser.setStyleSheet("color: gray;")
        self.comboBox_ser = QtGui.QComboBox(Dialog)
        self.comboBox_ser.setGeometry(QtCore.QRect(80, 35, 80, 22))

        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 63, 60, 22))
        self.label_dia.setAlignment(QtCore.Qt.AlignRight)
        self.label_dia.setStyleSheet("color: gray;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 63, 80, 22))
        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 90, 185, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(145, 113, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(50,113,80,22))
        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 150, 200, 200))
        self.label_5.setAlignment(QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")
        pic='Cylindorical Roller Bearings.png'  
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

        self.comboBox_ser.addItems(RollingBrg_Data.CylSer)
        self.comboBox_dia.addItems(RollingBrg_Data.CylDia)
        self.comboBox_ser.currentIndexChanged[int].connect(self.onSer)
        self.comboBox_ser.currentIndexChanged[int].connect(self.onDia)
        
        self.comboBox_ser.setEditable(True)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia)
        self.comboBox_dia.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.readData)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "CylindoricalRollerBrg", None))
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
        global mySht
        selection = Gui.Selection.getSelection()
        if selection:
            selected_object = selection[0]
            if selected_object.TypeId == "App::Part":
                parts_group = selected_object
                for obj in parts_group.Group:
                    if obj.Label[:5] =="mySht":
                        mySht = obj
            self.comboBox_ser.setCurrentText(mySht.getContents('A1'))            
            self.comboBox_dia.setCurrentText(mySht.getContents('A3'))
         
    def onSer(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        key0=self.comboBox_ser.currentText()
        try:
            mySht.set('A1',key0)
        except:
            pass
    def onDia(self):
         global d
         global D
         global B
         global dr
         global Dr
         global r
         global r1
         global n
         key=self.comboBox_dia.currentText()
         listL=[]
         if self.comboBox_ser.currentText()=='20':
             a=3
             b=28
         elif self.comboBox_ser.currentText()=='30':
             a=29
             b=53  
         #mySht.set('A1',self.comboBox_ser.currentText())
         for i in range(a,b):
             try:
                 if key==mySht.getContents('A'+str(i)):
                     #print(i,key,mySht.getContents('A'+str(i)))
                     for i in range(a,b):
                         if key==mySht.getContents('A'+str(i)):
                             listL=[]
                             for j in range(0,8):
                                 listL.append(mySht.getContents(column_list[j]+str(i)))
                             d=listL[0]
                             D=listL[1]
                             B=listL[2]
                             dr=listL[3]
                             Dr=listL[4]
                             r=listL[5]
                             r1=listL[6]
                             n=listL[7]
             except:
                 pass
    def upDate(self):
        mySht.set('d',d)
        mySht.set('D',D)
        mySht.set('B',B)
        mySht.set('dr',dr)
        mySht.set('Dr',Dr)
        mySht.set('r',r)
        mySht.set('r1',r1)
        mySht.set('n',n)
        App.ActiveDocument.recompute()      

    def create(self):
         doc=App.ActiveDocument
         fname='CylindoricalRollerBrg_SingleRow20.FCStd'
         
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, fname) 
 
         # --- インポート前のオブジェクトリストを取得 ---
         old_obj_names = [o.Name for o in doc.Objects]
         
         # マージ実行
         Gui.ActiveDocument.mergeProject(joined_path)
         #doc.recompute() # 一旦再計算して内部IDを確定させる
         # --- インポート後に増えたオブジェクトを特定 ---
         new_objs = [o for o in doc.Objects if o.Name not in old_obj_names]
         
         if not new_objs:
             print("Error: オブジェクトが読み込まれませんでした。")
             return
         #latticeBeamというラベルを持つものを優先的に探す
         move_target = None
         for o in new_objs:
             if "CylindricalRollerBrg_SingleRow"  in o.Label[:30] or "CylindricalRollerBrg_SingleRow"  in o.Name[:30]:
                 move_target = o
         
         # 見つからなければ、新しく入ってきた最初のオブジェクトをターゲットにする
         if not move_target:
             move_target = new_objs[0]
         view = Gui.ActiveDocument.ActiveView
         callbacks = {}
         def move_cb(info):
             pos = info["Position"]
             # 重要：ビュー平面上の3D座標を取得
             p = view.getPoint(pos)
             if move_target:
                 move_target.Placement.Base = p
                 #view.softRedraw()
         def click_cb(info):
             if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                 # コールバック解除
                 view.removeEventCallback("SoLocation2Event", callbacks["move"])
                 view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
                 App.ActiveDocument.recompute()
                 print("Placed: " + move_target.Label)
         # イベント登録
         callbacks["move"] = view.addEventCallback("SoLocation2Event", move_cb)
         callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)


class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        