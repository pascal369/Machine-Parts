# -*- coding: utf-8 -*-
import os
import sys
import Import
#import ImportGui as Gui
import Spreadsheet
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
#from prt_data.CSnap_data import paramCSnap


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 150)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(130, 0, 250, 120))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spring_data',"TensionSpring.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #線径　dia
        self.label_dia = QtGui.QLabel('Wire_dia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.label_dia.setStyleSheet("color: black;")
        self.lineEdit_dia = QtGui.QLineEdit('1.6',Dialog)
        self.lineEdit_dia.setGeometry(QtCore.QRect(80, 15, 50, 20))
        self.lineEdit_dia.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_dia.setObjectName("Wire_dia")
        
        #ピッチ Pitch
        self.label_Pitch = QtGui.QLabel('Pitch',Dialog)
        self.label_Pitch.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.label_Pitch.setStyleSheet("color: black;")
        self.lineEdit_Pitch = QtGui.QLineEdit('2.0',Dialog)
        self.lineEdit_Pitch.setGeometry(QtCore.QRect(80, 37, 50, 20))
        self.lineEdit_Pitch.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_Pitch.setObjectName("Pitch")
        #コイル径 Coildia
        self.label_coilDia = QtGui.QLabel('Coil_dia',Dialog)
        self.label_coilDia.setGeometry(QtCore.QRect(10, 63, 150, 12))
        self.label_coilDia.setStyleSheet("color: black;")
        self.lineEdit_coilDia = QtGui.QLineEdit('10.0',Dialog)
        self.lineEdit_coilDia.setGeometry(QtCore.QRect(80, 63, 50, 20))
        self.lineEdit_coilDia.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_coilDia.setObjectName("coilDia")
        #巻き数 turns
        self.label_Turns = QtGui.QLabel('Turns',Dialog)
        self.label_Turns.setGeometry(QtCore.QRect(10, 88, 150, 12))
        self.label_Turns.setStyleSheet("color: black;")
        self.lineEdit_Turns = QtGui.QLineEdit('10.0',Dialog)
        self.lineEdit_Turns.setGeometry(QtCore.QRect(80, 85, 50, 20))
        self.lineEdit_Turns.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_Turns.setObjectName("CoilHight")

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 120, 90, 22))
        #インポート
        self.pushButton4 = QtGui.QPushButton('Import',Dialog)
        self.pushButton4.setGeometry(QtCore.QRect(170, 120, 90, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(260, 120, 90, 22))
       


        
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        
        QtCore.QObject.connect(self.pushButton4, QtCore.SIGNAL("pressed()"), self.onImport)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "tensile coil spring", None))
        

    

    def onImport(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        # Partsグループが選択されているかチェック
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj

                         self.lineEdit_dia.setText(spreadsheet.getContents('Wire_dia'))  
                         self.lineEdit_Pitch.setText(spreadsheet.getContents('Pitch'))  
                         self.lineEdit_coilDia.setText(spreadsheet.getContents('Coil_dia'))  
                         self.lineEdit_Turns.setText(spreadsheet.getContents('Turns')) 
                         #print('bbbbbbbbbbbbbbbb')


    def update(self):

         dia=self.lineEdit_dia.text()
         Pitch=self.lineEdit_Pitch.text()
         Coil_dia=self.lineEdit_coilDia.text()
         Turns=self.lineEdit_Turns.text()
         
         try:
              
            spreadsheet.set('B2',dia)
            spreadsheet.set('B3',Pitch)
            spreadsheet.set('B4',Coil_dia)
            spreadsheet.set('B5',Turns)
            App.ActiveDocument.recompute()
         except:
            pass    

    def create(self): 
         doc=App.ActiveDocument
         fname='TensionCoilSpring.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Spring_data',fname) 
         
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
             if "Spring"  in o.Label or "Spring"  in o.Name:
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
        