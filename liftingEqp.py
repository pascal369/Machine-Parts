# -*- coding: utf-8 -*-
import os
import sys
import Import
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
parts=['chainBlock','erectricChainBlock','GantryCrane','GearedTrolley','JibCrane','PlainTrolley']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 250)
        Dialog.move(1000, 0)
        
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(240, 0, 200, 250))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #パーツ　parts
        self.label_parts = QtGui.QLabel('Parts',Dialog)
        self.label_parts.setGeometry(QtCore.QRect(10, 0, 150, 12))
        self.label_parts.setStyleSheet("color: black;")
        self.comboBox_parts = QtGui.QComboBox(Dialog)
        self.comboBox_parts.setGeometry(QtCore.QRect(80, 0, 100, 22))

        #hook_Lifting
        self.label_hp = QtGui.QLabel('hookLifting',Dialog)
        self.label_hp.setGeometry(QtCore.QRect(10, 25, 150, 12))
        self.label_hp.setStyleSheet("color: black;")
        self.le_hp = QtGui.QLineEdit('800',Dialog)
        self.le_hp.setGeometry(QtCore.QRect(80, 25, 80, 22))
        self.le_hp.setAlignment(QtCore.Qt.AlignCenter)
        self.spinch=QtGui.QSpinBox(Dialog)
        self.spinch.setGeometry(160, 25, 80, 22)
        self.spinch.setMinimum(-9999)  # 最小値
        self.spinch.setMaximum(9999)  # 最大値
        self.spinch.setSingleStep(10) #step
        self.spinch.setAlignment(QtCore.Qt.AlignCenter)
        #running
        self.label_run = QtGui.QLabel('running',Dialog)
        self.label_run.setGeometry(QtCore.QRect(10, 50, 150, 12))
        self.label_run.setStyleSheet("color: black;")
        self.le_run = QtGui.QLineEdit('1000',Dialog)
        self.le_run.setGeometry(QtCore.QRect(80, 50, 80, 22))
        self.le_run.setAlignment(QtCore.Qt.AlignCenter)
        self.spinrun=QtGui.QSpinBox(Dialog)
        self.spinrun.setGeometry(160, 50, 80, 22)
        self.spinrun.setMinimum(-99999)  # 最小値
        self.spinrun.setMaximum(99999)  # 最大値
        self.spinrun.setSingleStep(100) #step
        self.spinrun.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 100, 80, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 125, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 150, 80, 22))

        self.comboBox_parts.addItems(parts)

        self.comboBox_parts.setCurrentIndex(1)
        self.comboBox_parts.currentIndexChanged[int].connect(self.onParts)
        self.comboBox_parts.setCurrentIndex(0)

        self.spinch.valueChanged[int].connect(self.update)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def onParts(self):
        if self.comboBox_parts.currentText()=='ChainBlock':
                    fname='ChainBlockAssy.png'
        elif self.comboBox_parts.currentText()=='erectricChainBlock':
            fname='erectricChainBlock.png'
        elif self.comboBox_parts.currentText()=='GantryCrane':
                    fname='gantryCrane.png'
        elif self.comboBox_parts.currentText()=='GearedTrolley':
                            fname='gearedTrolley.png' 
        elif self.comboBox_parts.currentText()=='JibCrane':
                            fname='jibCrane.png'  
        elif self.comboBox_parts.currentText()=='PlainTrolley':
                            fname='plainTrolley.png'                                                 

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'LiftingEquipment','image',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "LiftingEquipment", None))

    def read(self):
        global ChenBlock_Hook_1t
        global sht
        selected = Gui.Selection.getSelection()
        for obj in selected:
             print(obj.Label)
            # Assemblyコンテナなら子を取得
             if hasattr(obj, "Group") and len(obj.Group) > 0:
                 targets = obj.Group
             else:
                targets = selected
    
        for obj in targets:
            print(obj.Label)
            if obj.Label=='ChenBlock_Hook_1t':
                ChenBlock_Hook_1t=obj
            elif obj.Label=='Spreadsheet002':
                sht=obj    
        self.le_hp.setText(str(ChenBlock_Hook_1t.Placement.Base.z))               
        self.spinch.setValue(ChenBlock_Hook_1t.Placement.Base.z)                 
                                 
 
    def update(self):
        
        #ChenBlock_Hook_1t.Placement.Base.z=self.le_hp.text()
        H0=self.spinch.value()
        sht.set('lft',str(H0))
        self.le_hp.setText(str(H0))
        ChenBlock_Hook_1t.Placement.Base.z=float(H0-123)
        App.ActiveDocument.recompute()

    def create(self): 
         doc=App.ActiveDocument
         if self.comboBox_parts.currentText()=='ChainBlock':
             mypath='erectricChainBlock'
             fname='electricChainBlockAssy.FCStd' 
         elif self.comboBox_parts.currentText()=='GantryCrane':
             mypath='GantryCrane'
             fname='GantryCrane.FCStd' 
         elif self.comboBox_parts.currentText()=='GearedTrolley':
             mypath='Gearedtrolley'
             fname='gearedTrolley.FCStd' 
         elif self.comboBox_parts.currentText()=='JibCrane':
             mypath='jibCrane'
             fname='jibCrane.FCStd'    
         elif self.comboBox_parts.currentText()=='PlainTrolley':
             mypath='Plaintrolley'
             fname='plainTrolley.FCStd'                                                       


         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','LiftingEquipment',mypath,fname) 
         #print(joined_path)
           # --- インポート前のオブジェクトリストを取得 ---
         old_obj_names = [o.Name for o in doc.Objects]
         
         # マージ実行
         Gui.ActiveDocument.mergeProject(joined_path)
         doc.recompute() # 一旦再計算して内部IDを確定させる

         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)             