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

parts=['平歯車','はすば歯車','傘歯車','遊星歯車']

S_Width=['3','4','5','6','6.5','8','9.5','10','11','12.5','14.5',
      '16','19','20','22','25']
# D,      min,   max
S_Dim={
'3':(    3,      12, ),
'4':(    4,      20, ),
'5':(    5,      25, ),
'6':(    8,      28, ),
'6.5':(  8,      28, ),
'8':(   12,      50, ),
'9.5':( 18,      70, ),
'10':(  18,      70, ),
'11':(  18,      70, ),
'12.5':(32,     125, ),
'14.5':(32,     125, ),
'16':(  56,     180, ),
'19':(  90,     250, ),
'20':( 125,     250, ),
'22':( 125,     250, ),
'25':( 125,     250, ),
 }

# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 350)
        Dialog.move(1000, 0)


        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 165, 200, 200))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Gear_data',"gear01.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #種類
        self.label_type = QtGui.QLabel('種類',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 10, 100, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 100, 22))
        #形状
        self.label_shap = QtGui.QLabel('形状',Dialog)
        self.label_shap.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_shap = QtGui.QComboBox(Dialog)
        self.comboBox_shap.setGeometry(QtCore.QRect(110, 35, 100, 22))
        #モジュール
        self.label_mod = QtGui.QLabel('モジュール',Dialog)
        self.label_mod.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.comboBox_mod = QtGui.QComboBox(Dialog)
        self.comboBox_mod.setGeometry(QtCore.QRect(110, 60, 100, 22))
        #穴径
        self.label_dia = QtGui.QLabel('穴径',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 88, 100, 12))
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(110, 85, 100, 22))
        
        #ボス径
        self.label_bossD = QtGui.QLabel('ボス径',Dialog)
        self.label_bossD.setGeometry(QtCore.QRect(10, 113, 100, 22))
        self.comboBox_bossD = QtGui.QComboBox(Dialog)
        self.comboBox_bossD.setGeometry(QtCore.QRect(110, 110, 100, 22))
        
        #ボス幅
        self.label_bossD = QtGui.QLabel('ボス幅',Dialog)
        self.label_bossD.setGeometry(QtCore.QRect(10, 138, 100, 22))
        self.comboBox_bossD = QtGui.QComboBox(Dialog)
        self.comboBox_bossD.setGeometry(QtCore.QRect(110, 135, 100, 22))

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 160, 60, 22))

        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 160, 60, 22))



        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Gear", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "作成", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "更新", None))  

    def onWidth(self):
        #return
        global dmin
        global dmax
        global S0
        S0=self.comboBox_S.currentText()
        sa=S_Dim[S0]
        dmin=sa[0]
        dmax=sa[1]
        appDia='適用軸径'+str(dmin)+'～'+str(dmax)
        self.label_shaftdia.setText(appDia)
        #print(appDia)
        self.le_dia.setText(str(dmin))
        return    
    
    def update(self):
         # スプレッドシートを選択
         spreadsheet = App.ActiveDocument.getObject("Spreadsheet")
         Gui.Selection.clearSelection()
         Gui.Selection.addSelection(spreadsheet)
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
                     dia=self.le_dia.text()
                     #spreadsheet.set('B2',str(S0))
                     spreadsheet.set('B3',dia)
                     App.ActiveDocument.recompute()

    def create(self): 

         fname=''
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','GlandP_data',fname) 
         #print(joined_path)
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)

         # アクティブなドキュメントを取得する
         doc = App.ActiveDocument

         # アクティブなスプレッドシートを取得する
         sheet = doc.getSpreadsheet()    
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            