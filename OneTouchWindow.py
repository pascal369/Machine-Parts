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

CDia=['130x200','200x300','350x500','500x600',]
CType=['Small','Large']
# D,            A,      B,    H,    
CDim={
'130x200': (    130,    200,   63),
'200x300': (    200,    300,   63),
'350x500': (    350,    500,   63),
'500x600': (    500,    600,   88),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 310)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 110, 200, 200))
        self.label_6.setText("aaa")

        #タイプ　type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 9, 90, 22))
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominalDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 35, 90, 22))
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 61, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 85, 80, 22))

        self.comboBox_type.addItems(CType)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_type.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "OneTouchWindow", None))
        
    
    def on_type(self):
        type=self.comboBox_type.currentText()
        self.comboBox_dia.clear()
        if type=='Small':
            pic='OneWindow(1).png'
            self.comboBox_dia.addItems(CDia[:3])
        elif type=='Large':
            pic='OneWindow(2).png'
            self.comboBox_dia.addItems(CDia[3:])
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'OneTouchWindow_data',pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

    def update(self):
         
         #spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         #Gui.Selection.clearSelection()
         #Gui.Selection.addSelection(spreadsheet)
         selection = Gui.Selection.getSelection()

         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         key=self.comboBox_dia.currentText()
                         sa=CDim[key]
                         spreadsheet.set('B1',key)
                         spreadsheet.set('B2',str(sa[0]))#A0
                         spreadsheet.set('B3',str(sa[1]))#B0
                         spreadsheet.set('B4',str(sa[2]))#H0
                         
                         App.ActiveDocument.recompute()

    def create(self): 
         doc=App.ActiveDocument
         #global fname
         key=self.comboBox_dia.currentText()
         if key=='130x200' or key=='200x300':
             fname='OneTouchWindow(1).FCStd'
         elif key=='350x500' or key=='500x600':
             fname='OneTouchWindow(2).FCStd'    

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','OneTouchWindow_data',fname) 
         
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
             if "OneTouchWindow"  in o.Label or "OneTouchWindow"  in o.Name:
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
        