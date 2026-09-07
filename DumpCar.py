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
doc=App.ActiveDocument
ton=['4t','10t',]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(220, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 110, 200, 200))
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
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(85, 60, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('setData',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(10, 60, 80, 22))
        #mainFrame up/down
        self.label_frame = QtGui.QLabel('mainFram up/down',Dialog)
        self.label_frame.setGeometry(QtCore.QRect(10, 85, 100, 22))
        self.label_frame.setStyleSheet("color: black;")
        self.spinFrame=QtGui.QSpinBox(Dialog)
        self.spinFrame.setGeometry(105, 85, 100, 22)
        self.spinFrame.setMinimum(-9999)  # 最小値
        self.spinFrame.setMaximum(9999)  # 最大値
        self.spinFrame.setSingleStep(10) #step
        self.spinFrame.setAlignment(QtCore.Qt.AlignCenter)
        #cover
        self.label_cover = QtGui.QLabel('cover open/close',Dialog)
        self.label_cover.setGeometry(QtCore.QRect(10, 110, 100, 22))
        self.label_cover.setStyleSheet("color: black;")
        self.spinCover=QtGui.QSpinBox(Dialog)
        self.spinCover.setGeometry(105, 110, 100, 22)
        self.spinCover.setMinimum(0)  # 最小値
        self.spinCover.setMaximum(150)  # 最大値
        self.spinCover.setSingleStep(1) #step
        self.spinCover.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_ton.addItems(ton)

        self.comboBox_ton.setCurrentIndex(1)
        self.comboBox_ton.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_ton.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        self.spinFrame.valueChanged[int].connect(self.moveRod)
        self.spinCover.valueChanged[int].connect(self.moveCover)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        #QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Handle", None))
        self.label_ton.setText(QtGui.QApplication.translate("Dialog", "Capacity", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  

    def moveRod(self):
        self.spinFrame.blockSignals(True)
        cylinder_rod.Placement.Base.z=self.spinFrame.value()
        doc.recompute()
        self.spinFrame.blockSignals(False)
    def moveCover(self):
        self.spinCover.blockSignals(True)
        angle=self.spinCover.value()
        CoverAssyL.Placement.Rotation=App.Rotation(
            App.Vector(1,0,0),
            angle)
        CoverAssyR.Placement.Rotation=App.Rotation(
            App.Vector(1,0,0),
            -angle)
        doc.recompute()
        self.spinCover.blockSignals(False)

    def setParts(self):
        global cylinder_rod
        global CoverAssyL
        global CoverAssyR
        global mainFrame
        global GateAssy
        selected = Gui.Selection.getSelection()
        for obj in selected:
#            print(obj.Label)
            # Assemblyコンテナなら子を取得
            if hasattr(obj, "Group") and len(obj.Group) > 0:
                targets = obj.Group
            else:
                targets = selected
#        parts_dict = {}        
        for obj in targets:
            if obj.Label=='cylinder_rod':
                cylinder_rod=obj
            elif obj.Label=='CoverAssyL':
                CoverAssyL=obj  
            elif obj.Label=='CoverAssyR':
                CoverAssyR=obj     
            elif obj.Label=='mainFrame':
                mainFrame=obj  
            #elif obj.Label=='GateAssy':
            #    GateAssy=obj            
        self.spinFrame.setValue(cylinder_rod.Placement.Base.z) 
        #self.spinCover.setValue(CoverAssyL.Placement.Rotation) 
        #GateAssy.Placement.Rotation=App.Rotation(
        #    App.Vector(0,1,0),
        #    0
        #)
        Gui.activateWorkbench("AssemblyWorkbench")
 
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
             fname='4tDumpA.FCStd'   
         else:
            fname='10tDumpA.FCStd'    

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'DumpCar_data',fname) 
        
#         # --- インポート前のオブジェクトリストを取得 ---
         old_obj_names = [o.Name for o in doc.Objects]
#          # マージ実行
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
                       