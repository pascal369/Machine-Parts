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
#Type=['外リンク','内リンク','オフセットリンク','スプロケットA','スプロケットB','スプロケットC']
CDia=['7','8','9.5','11','13','16','19','22','24','27','30',]
# No,      d,       L,     Bi,     Load[N],       
CDim={
'7':(     7.0,     36,   10,       3430,  ),
'8':(     8.0,     40,   12,       4900,  ),
'9.5':(   9.5,     46,   14,       7350,  ),
'11':(   11.0,     53,   17,       9800,  ),
'13':(   13.0,     62,   20,      14700,  ),
'16':(   16.0,     77,   24,      24500,  ),
'19':(   19.0,     91,   29,      34300,  ),
'22':(   22.0,    106,   34,      44100,  ),
'24':(   24.0,    115,   36,      53900,  ),
'27':(   27.0,    129,   40,      66150,  ),
'30':(   30.0,    144,   45,      83300,  ),
       }

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 145)
        Dialog.move(900, 0)
        
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(180, 10, 150, 100))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Chain_data','LinkChain','LinkChain.png')
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel('NominalDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 10, 110, 22))

        #作成
        self.pushButton = QtGui.QPushButton('作成',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 60, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('更新',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 85, 80, 22))

        self.comboBox_dia.addItems(nominalDia)

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "リンクチェン", None))

    def update(self):
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
                     key=self.comboBox_dia.currentText()
                     sa=RDim[key]
                     spreadsheet.set('B2',key)
                     spreadsheet.set('B3',str(sa[0]))#d
                     spreadsheet.set('B4',str(sa[1]))#L
                     spreadsheet.set('B5',str(sa[2]))#Bi
                     spreadsheet.set('B6',str(sa[3]))#Load
                     

                     App.ActiveDocument.recompute()

    def create(self): 

         fname='LChain.FCStd' 
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Chain_data','LinkChain',fname) 

         try:
            doc=App.activeDocument()
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
        try:
           # スクリプトのウィンドウを取得
           script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
           # 閉じるボタンを無効にする
           script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)  
        except:
            pass  