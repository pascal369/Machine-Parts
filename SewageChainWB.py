# -*- coding: utf-8 -*-
import os
import sys
import Import
import Spreadsheet
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

Series=['ACS19152W','ACS35152W','HighNotch','JAC6205S',]
ACS_Parts=['spro_key','spro_nokey','innerLink','outerLink','SF4','LA1']
Hinotch_Parts=['hispro','hiwheel','hiLink','hiAttach']
JAC_Parts=['spro_key','spro_nokey','innerLink','outerLink','Y']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 120)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(200, 10, 150, 100))
        self.label_6.setText("")
        
        #シリーズ Series
        self.label_Series = QtGui.QLabel('Series',Dialog)
        self.label_Series.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.label_Series.setStyleSheet("color: black;")
        self.comboBox_Series = QtGui.QComboBox(Dialog)
        self.comboBox_Series.setGeometry(QtCore.QRect(80, 9, 110, 22))
        #パーツ　Parts
        self.label_Parts = QtGui.QLabel('Parts',Dialog)
        self.label_Parts.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.label_Parts.setStyleSheet("color: black;")
        self.comboBox_Parts = QtGui.QComboBox(Dialog)
        self.comboBox_Parts.setGeometry(QtCore.QRect(80, 35, 110, 22))

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 65, 80, 22))
        #更新
        

        self.comboBox_Series.addItems(Series)
        self.comboBox_Parts.addItems(ACS_Parts)
        self.comboBox_Series.setCurrentIndex(1)
        self.comboBox_Series.currentIndexChanged[int].connect(self.on_Series)
        self.comboBox_Series.setCurrentIndex(0)
        self.comboBox_Parts.setCurrentIndex(1)
        self.comboBox_Parts.currentIndexChanged[int].connect(self.on_Parts)
        self.comboBox_Parts.setCurrentIndex(0)

        #QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "waterTreatmentChain", None))
    
    def on_Series(self):
        global fname
        global pic
        global key2
        global Parts
        key1=self.comboBox_Series.currentIndex()
        key2=self.comboBox_Parts.currentIndex()
        if key1<=1:
            Parts=ACS_Parts
        elif key1 <=2:
            Parts=Hinotch_Parts
        elif key1==3:
            Parts= JAC_Parts   
        self.comboBox_Parts.clear()    
        self.comboBox_Parts.addItems(Parts)
        #print(key1)
        #print(key2)
        name=str(Series[key1])+'_'+str(Parts[key2])
        fname=name+'.FCStd'
        
        #print(pic)
        #print(fname)
    def on_Parts(self):  
        key2=self.comboBox_Parts.currentIndex()
        pic=str(Parts[key2])+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        try:
            joined_path = os.path.join(base, "prt_data",'Chain_data','SewageChain',pic)
            #print(joined_path)
            self.label_6.setPixmap(QtGui.QPixmap(joined_path))
            self.label_6.setAlignment(QtCore.Qt.AlignCenter)
            self.label_6.setObjectName("label_6")
        except:
            pass
        

    def create(self): 
         doc=App.ActiveDocument
         key1=self.comboBox_Series.currentIndex()
         key2=self.comboBox_Parts.currentIndex()
         name=str(Series[key1])+'_'+str(Parts[key2])
         fname=name+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Chain_data','SewageChain',fname) 
         
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
         #latticeBeamというラベルを持つものを優先的に探す
         move_target = None
         for o in new_objs:
             if "ACS19152W_Key"  in o.Label or "ACS19152W_key"  in o.Name:
                 move_target = o
                 break
             elif "ACS19152W_noKey"  in o.Label or "ACS19152W_noKey"  in o.Name:
                 move_target = o
                 break
             elif "ACS19152W_SF4"  in o.Label or "ACS19152W_SF4"  in o.Name:
                 move_target = o
             elif "ACS19152W_LA1"  in o.Label or "ACS19152W_LA1"  in o.Name:
                 move_target = o    
             elif "OuterLink"  in o.Label or "OuterLink"  in o.Name:
                 move_target = o
                 break
             elif "InnerLink"  in o.Label or "InnerLink"  in o.Name:
                 move_target = o
                 break
             elif "ACS35152W_Key"  in o.Label or "ACS35152W_Key"  in o.Name:
                 move_target = o
                 break
             elif "ACS35152W_Nokey"  in o.Label or "ACS35152W_Nokey"  in o.Name:
                 move_target = o
                 break
             elif "ACS35152W_SF4"  in o.Label or "ACS35152W_SF4"  in o.Name:
                 move_target = o
                 break
             elif "ACS35152W_LA1"  in o.Label or "ACS35152W_LA1"  in o.Name:
                 move_target = o
             elif "ACS35152W_outerlink"  in o.Label or "ACS35152W_outerlink"  in o.Name:
                 move_target = o
                 break
             elif "ACS35152W_innerlink"  in o.Label or "ACS35152W_innerlink"  in o.Name:
                 move_target = o
                 break
             elif 'HighNotch_Spro' in o.Label or 'HighNotch_Spro' in o.Name:
                 move_target=o
                 break
             elif "HighNotch_wheel"  in o.Label or "HighNotch_wheel"  in o.Name:
               move_target = o
               break               
             elif "HighNotch_attach"  in o.Label or "HighNotch_attach"  in o.Name:
                 move_target = o
                 break
             elif "HighNotch_attach"  in o.Label or "HighNotch_attach"  in o.Name:
                 move_target = o    
             elif "ハイノッチチェン"  in o.Label or "ハイノッチチェン"  in o.Name:
                 move_target = o 
                 break 
             elif "Y"  in o.Label or "Y"  in o.Name:
                 move_target = o 
                 break
             elif "JAC6205S_innerLink"  in o.Label or "JAC6205S_innerLink"  in o.Name:
                 move_target = o 
                 break 
             elif "JAC6205S_outerLink"  in o.Label or "JAC6205S_outerLink"  in o.Name:
                 move_target = o 
                 break            
             elif "JAC6205S_Key"  in o.Label or "JAC6205S_Key"  in o.Name:
                 move_target = o 
                 break 
             elif "JAC6205S_noKey"  in o.Label or "JAC6205S_noKey"  in o.Name:
                 move_target = o
                 break
             elif "JAC6205S_Y"  in o.Label or "JAC6205S_Y"  in o.Name:
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
        