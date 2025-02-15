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


BeltW=['400','450','500','600','700','750','800','900','1000',]
#       B0     b1     b2     t0    D0    d1   d2    Ls    h0
BDim={'400':( 145,   127.5,  10,  300,  260,  200,  500,  180,),	
      '450':( 165,   142.5,  10,  300,  260,  200,  500,  180,),
      '500':( 180,   160.0,  10,  300,  300,  200,  500,  180,),
      '600':( 210,   195.0,  10,  360,  300,  200,  500,  180,),
      '700':( 250,   225.0,  10,  360,  300,  200,  500,  180,),
      '750':( 265,   242.5,  10,  460,  390,  200,  500,  180,),
      '800':( 280,   260.0,  10,  460,  390,  200,  500,  180,),
      '900':( 315,   292.5,  10,  520,  440,  200,  500,  180,),
      '1000':(345,   327.5,  10,  520,  440,  200,  500,  180,),}
      
# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 350)
        Dialog.move(1500, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 115, 200, 200))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'prt_data','plainBrg_data',"bushing500SP.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        #ベルト幅
        self.label_B = QtGui.QLabel('BeltWidth',Dialog)
        self.label_B.setGeometry(QtCore.QRect(30, 13, 100, 22))
        self.comboBox_B = QtGui.QComboBox(Dialog)
        self.comboBox_B.setGeometry(QtCore.QRect(150, 13, 60, 22))
        self.comboBox_B.listIndex=11
        
        #機長
        self.label_C = QtGui.QLabel('CenterDistance[mm]',Dialog)
        self.label_C.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.le_C = QtGui.QLineEdit(Dialog)
        self.le_C.setGeometry(QtCore.QRect(150, 38, 60, 20))
        self.le_C.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 65, 60, 22))

        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(151, 65, 60, 22))


        #self.comboBox_parts.addItems(parts)
        self.comboBox_B.addItems(BeltW)

        self.comboBox_B.setCurrentIndex(1)
        self.comboBox_B.currentIndexChanged[int].connect(self.onWidth) 
        self.comboBox_B.setCurrentIndex(0)
        self.le_C.setText('5000')

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "3ローラートラフ型ベルト", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onWidth(self):
        return
        global L
        L=self.le_C.text()
   
    def update(self):
         # スプレッドシートを選択
         spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         Gui.Selection.clearSelection()
         Gui.Selection.addSelection(spreadsheet)
         selection = Gui.Selection.getSelection()
         
         # 選択したオブジェクトを取得
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
                         #Gui.Selection.clearSelection()
                         Gui.Selection.addSelection(spreadsheet)
         # 選択したスプレッドシートを取得
         if selection:
             for obj in selection:
                 if obj.TypeId == "Spreadsheet::Sheet":
                     # スプレッドシートが見つかった場合の処理
                     spreadsheet = obj
                     key=self.comboBox_B.currentText()
                     sa=BDim[key]
                     L=self.le_C.text()
                     spreadsheet.set('B2',L)
                     spreadsheet.set('B3',key)
                     spreadsheet.set('B4',str(sa[0]))#b1
                     spreadsheet.set('B5',str(sa[1]))#b2
                     spreadsheet.set('B6',str(sa[2]))#t0
                     spreadsheet.set('B7',str(sa[3]))#D0  
                     spreadsheet.set('B8',str(sa[4]))#d1 
                     spreadsheet.set('B9',str(sa[5]))#d2
                     spreadsheet.set('B10',str(sa[6]))#Ls
                     spreadsheet.set('B11',str(sa[7]))#h0
                     

                     App.ActiveDocument.recompute()

    def create(self): 
        
         fname='Belt0.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base,'Belt_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)

         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            