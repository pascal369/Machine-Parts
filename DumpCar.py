# -*- coding: utf-8 -*-
import os
import sys
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
#from prt_data.CSnap_data import paramCSnap

ton=['4t','10t',]


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 80, 200, 200))
        self.label_6.setText("aaa")
        
        #ton
        self.label_ton = QtGui.QLabel(Dialog)
        self.label_ton.setGeometry(QtCore.QRect(10, 13, 150, 22))
        self.label_ton.setStyleSheet("color: black;")
        self.comboBox_ton = QtGui.QComboBox(Dialog)
        self.comboBox_ton.setGeometry(QtCore.QRect(80, 8, 90, 22))
        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 35, 80, 22))
        #更新
        #self.pushButton2 = QtGui.QPushButton(Dialog)
        #self.pushButton2.setGeometry(QtCore.QRect(80, 60, 80, 22))
        #インポート
        #self.pushButton3 = QtGui.QPushButton(Dialog)
        #self.pushButton3.setGeometry(QtCore.QRect(80, 60, 80, 22))

        self.comboBox_ton.addItems(ton)

        self.comboBox_ton.setCurrentIndex(1)
        self.comboBox_ton.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_ton.setCurrentIndex(0)

        #QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        #QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        #QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Handle", None))
        self.label_ton.setText(QtGui.QApplication.translate("Dialog", "Capacity", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
 
    def on_type(self):
        Capacity=self.comboBox_ton.currentText()
        if Capacity=='4t':
            pic='4tDump.png'
        elif Capacity=='10t':
            pic='10tDump.png'    
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'DumpCar_data',pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

    def create(self): 
         doc=App.ActiveDocument
         Capacity=self.comboBox_ton.currentText()
         if Capacity=='4t':
             fname='4tDump.FCStd'   
         else:
            fname='10tDump.FCStd'    

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'DumpCar_data',fname) 
        
         # --- インポート前のオブジェクトリストを取得 ---
         old_obj_names = [o.Name for o in doc.Objects]
          # マージ実行
         Gui.ActiveDocument.mergeProject(joined_path)
         doc.recompute() # 一旦再計算して内部IDを確定させる
         # --- インポート後に増えたオブジェクトを特定 ---
         new_objs = [o for o in doc.Objects if o.Name not in old_obj_names]
         
         if not new_objs:
             print("Error: オブジェクトが読み込まれませんでした。")
             return
         #
         move_target = None
         for o in new_objs:
             if "Assembly_Dump"  in o.Label or "Assembly_Dump"  in o.Name:
                 move_target = o
                 break
             
             
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
                       