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

ODia=['6','8','9','10','12','14','16','18','20','22',]
wireDia={'6':('6.3',),
         '8':('8',),
         '9':('9',),
         '10':('10',),
         '12':('12.5',),
         '14':('14',),
         '16':('16',),
         '18':('18',),
         '20':('20',),
         '22':('22.4')}

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 370)
        Dialog.move(1000, 0)
        #和文
        self.pushButton_la = QtGui.QPushButton('JPN Text',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(10, 10, 30, 22))
        self.le_la = QtGui.QLineEdit('シンブル',Dialog)
        self.le_la.setGeometry(QtCore.QRect(105, 10, 175, 22))
        self.le_la.setAlignment(QtCore.Qt.AlignLeft) 
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('nominal',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 38, 150, 22))
        self.label_dia.setStyleSheet("color: gray;")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(105, 35, 80, 22))
        #ワイヤー径
        self.label_wdia = QtGui.QLabel('WireDia',Dialog)
        self.label_wdia.setGeometry(QtCore.QRect(105, 63, 150, 22))
        self.label_wdia.setStyleSheet("color: gray;")
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 85, 45, 22))
        #更新
        self.pushButton3 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(102, 85, 45, 22))
        #インポート
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(194, 85, 45, 22))

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 125, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'WireRope',"Thimble.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.comboBox_dia.addItems(ODia)
        self.comboBox_dia.setEditable(True)

        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia) 
        self.comboBox_dia.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "シンブル", None))
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "呼び径", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "作成", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "更新", None))  
    def onDia(self):
        key=self.comboBox_dia.currentText()
        sa=wireDia[key]
        self.label_wdia.setText('wireDia(max)=  '+sa[0])
    
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

    def import_data(self):
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
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         key=spreadsheet.getContents('B14')
                         self.comboBox_dia.setCurrentText(key)
                         sa=wireDia[key]
                         self.label_wdia.setText('wireDia(max)=  '+sa[0])


    def update(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]

        key=self.comboBox_dia.currentText()
        for i in range(15,24):
            if key==spreadsheet.getContents('B'+str(i)):
                thd=spreadsheet.getContents('A'+str(i))
                thB0=spreadsheet.getContents('C'+str(i))
                thD0=spreadsheet.getContents('D'+str(i))
                thD1=spreadsheet.getContents('E'+str(i))
                thL=spreadsheet.getContents('F'+str(i))
                thL1=spreadsheet.getContents('G'+str(i))
                thR=spreadsheet.getContents('H'+str(i))
                thr=spreadsheet.getContents('I'+str(i))
                thr1=spreadsheet.getContents('J'+str(i))
                tht=spreadsheet.getContents('K'+str(i)) 
                tht1=spreadsheet.getContents('L'+str(i)) 
                spreadsheet.set('B14',key)
                spreadsheet.set('A14',str(thd))
                spreadsheet.set('C14',str(thB0))
                spreadsheet.set('D14',str(thD0))
                spreadsheet.set('E14',str(thD1))
                spreadsheet.set('F14',str(thL))
                spreadsheet.set('G14',str(thL1))
                spreadsheet.set('H14',str(thR))
                spreadsheet.set('I14',str(thr))
                spreadsheet.set('J14',str(thr1))
                spreadsheet.set('K14',str(tht))
                spreadsheet.set('L14',str(tht1))
        JPN=self.le_la.text()        
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN        
        App.ActiveDocument.recompute()

    def create(self): 
         doc=App.ActiveDocument
         dia=self.comboBox_dia.currentText()
         fname='WireThimble.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','WireRope',fname) 
         
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
             if "Thimble"  in o.Label or "Thimble"  in o.Name:
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
        