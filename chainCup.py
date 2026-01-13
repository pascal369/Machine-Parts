# -*- coding: utf-8 -*-
import os
import sys
import Import
import string
#import shtChainCup
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore

# D,      Pich,        h0,     t0,         W0,        d,      d2,     h1      c0
RDim={
'40':(    12.700,     10.40,   1.50,       7.95,     3.97,    7.92,  12.00,  14.4 ),
'50':(    15.875,     13.00,   2.00,       9.53,     5.09,   10.16,  15.00,  18.1 ),
'60':(    19.050,     15.60,   2.40,      12.70,     5.96,   11.91,  18.10,  22.8 ),
'80':(    25.400,     20.80,   3.20,      15.88,     7.94,   15.88,  24.10,  29.3 ),
'100':(   31.750,     26.00,   4.00,      19.05,     9.54,   19.05,  30.10,  35.8 ),
'120':(   38.100,     31.20,   4.80,      25.40,    11.11,   22.23,  36.20,  45.4 ),
'160':(   50.800,     41.60,   6.40,      31.75,    14.29,   28.58,  48.20,  58.5 ),
}

mdl=['4012','4014','4016','5014','5016','5018',
     '6018','6022','8018','8022','10020','12018',
     '12022','16018','16022']

class Ui_Dialog(object):
    global column_list
    alphabet_list = list(string.ascii_uppercase)
    column_list=[]
    for i in range(0,26):
        column_list.append(alphabet_list[i])
    for i in range(0,26):
        for j in range(0,26):
            column_list.append(alphabet_list[i] + alphabet_list[j])

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 165)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(220, 10, 150, 100))
        self.label_6.setText("")
        
        #呼び径　model number
        self.label_mdl = QtGui.QLabel('ModelNumber',Dialog)
        self.label_mdl.setGeometry(QtCore.QRect(10, 10, 150, 22))
        self.label_mdl.setStyleSheet("color: black;")
        self.comboBox_mdl = QtGui.QComboBox(Dialog)
        self.comboBox_mdl.setGeometry(QtCore.QRect(80, 10, 110, 22))
        self.comboBox_mdl.setEditable(True)
        self.comboBox_mdl.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #穴径
        self.label_hl = QtGui.QLabel('     (1)             (2)',Dialog)
        self.label_hl.setGeometry(QtCore.QRect(80, 35, 100, 22))
        self.label_hl.setStyleSheet("color: black;")
        self.label_hl1 = QtGui.QLabel('HoleDia',Dialog)
        self.label_hl1.setGeometry(QtCore.QRect(10, 60, 100, 22))
        self.label_hl1.setStyleSheet("color: black;")
        self.le_hl1 = QtGui.QLineEdit('90',Dialog)
        self.le_hl1.setGeometry(QtCore.QRect(85, 60, 50, 22))
        self.le_hl1.setAlignment(QtCore.Qt.AlignCenter)
        #self.le_hl1.setReadOnly(True)
        self.le_hl2 = QtGui.QLineEdit('90',Dialog)
        self.le_hl2.setGeometry(QtCore.QRect(152, 60, 50, 22))
        self.le_hl2.setAlignment(QtCore.Qt.AlignCenter)
        #self.le_hl2.setReadOnly(True)
        self.label_hlm = QtGui.QLabel('',Dialog)
        self.label_hlm.setGeometry(QtCore.QRect(10, 38, 100, 22))
        self.label_hlm.setStyleSheet("color: black;")

        self.label_hole = QtGui.QLabel('',Dialog)
        self.label_hole.setGeometry(QtCore.QRect(10, 85, 200, 22))
        self.label_hole.setStyleSheet("color: black;")
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 100, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(115, 110, 50, 22))
        #Import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(10, 135, 195, 22))
       
        self.comboBox_mdl.addItems(mdl)
        self.comboBox_mdl.setCurrentIndex(1)
        self.comboBox_mdl.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_mdl.setCurrentIndex(0)

        
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.select_objects_by_multiple_labels)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.Import)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Chain Coupling", None))
    def on_type(self):
        pic='chainCup.png'    
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'joint_data','chainCup',pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        #self.comboBox_mdl.setCurrentText(shtChainCup.getContents('B1'))
        #self.le_hl1.text(shtChainCup.getContents())
        try:
            for j in range(2,14):
                modelNo=self.comboBox_mdl.currentText()
                modelNo2=shtChainCup.getContents(column_list[j]+'1')
                #print(modelNo,modelNo2)
                if modelNo2==modelNo:
                    break
            dhmax=shtChainCup.getContents(column_list[j]+str(13))      
            dhmin=shtChainCup.getContents(column_list[j]+str(14))  
            self.label_hole.setText('Hole Diameter Range='+dhmin+'～'+dhmax)
        except:
            pass
    def Import(self):
        self.comboBox_mdl.setCurrentText(shtChainCup.getContents('B1'))
        self.le_hl1.setText(shtChainCup.getContents('dh1'))
        self.le_hl2.setText(shtChainCup.getContents('dh2'))
        self.label_hole.setText('Hole Diameter Range='+shtChainCup.getContents('dhmin')+'～'+shtChainCup.getContents('dhmax'))
        
    def collect_objects_recursive(self,group, target_labels):
        global Spro1
        global Spro2
        global shtChainCup
        global shtOuter2
        global shtInner2
        matched = []
        for obj in getattr(group, "Group", []):
            #print(obj.Label)
            if obj.Label=='Spro1':
                Spro1=obj
            elif obj.Label=='Spro2':
                Spro2=obj  
            elif obj.Label=='shtChainCup':
                shtChainCup=obj  
            elif obj.Label=='shtOuter2':
                shtOuter2=obj  
            elif obj.Label=='shtInner2':
                shtInner2=obj        

             # 下位フォルダなら再帰的に探索
            if hasattr(obj, "Group"):
                matched.extend(self.collect_objects_recursive(obj, target_labels))
            else:
                # ラベルが完全一致するオブジェクトを追加
                if obj.Label == target_labels:
                    matched.append(obj)
        return matched   
    
    def select_objects_by_multiple_labels(self):
        """選択したフォルダ以下で、指定した複数ラベル名のオブジェクトを選択"""
        sel = Gui.Selection.getSelection()
        if not sel:
            App.Console.PrintError("まずフォルダを選択してください。\n")
            return     
        root = sel[0]
        if not hasattr(root, "Group"):
            App.Console.PrintError("選択されたオブジェクトはフォルダ（Groupなど）ではありません。\n")
            return
        target_labels =['Carrier', 'Return']
        matched_objects = self.collect_objects_recursive(root, target_labels)
        Gui.Selection.clearSelection()
        for obj in matched_objects:
            Gui.Selection.addSelection(obj)   

    def update(self):
         for j in range(2,14):
            modelNo=self.comboBox_mdl.currentText()
            modelNo2=shtChainCup.getContents(column_list[j]+'1')
            print(modelNo,modelNo2)
            if modelNo2==modelNo:
                break
         
         z=shtChainCup.getContents(column_list[j]+str(2))
         Pitch=shtChainCup.getContents(column_list[j]+str(3))
         dr=shtChainCup.getContents(column_list[j]+str(4))
         ref=shtChainCup.getContents(column_list[j]+str(5))
         t0=shtChainCup.getContents(column_list[j]+str(6))   
         sPitch=shtChainCup.getContents(column_list[j]+str(7))   
         DH=shtChainCup.getContents(column_list[j]+str(8))  
         DL=shtChainCup.getContents(column_list[j]+str(9))     
         BS=shtChainCup.getContents(column_list[j]+str(10))   
         dh1=self.le_hl1.text()  
         dh2=self.le_hl2.text() 
         dhmax=shtChainCup.getContents(column_list[j]+str(13))      
         dhmin=shtChainCup.getContents(column_list[j]+str(14))  
         cNo=shtChainCup.getContents(column_list[j]+str(16)) 
         alpha=shtChainCup.getContents(column_list[j]+str(17))  
         beta=shtChainCup.getContents(column_list[j]+str(18))  
         A0=shtChainCup.getContents(column_list[j]+str(19)) 
         B0=shtChainCup.getContents(column_list[j]+str(20)) 

         shtChainCup.set(column_list[1]+str(1),modelNo )  
         shtChainCup.set(column_list[1]+str(2),z )  
         shtChainCup.set(column_list[1]+str(3),Pitch )  
         shtChainCup.set(column_list[1]+str(4),dr )  
         shtChainCup.set(column_list[1]+str(5),ref)  
         shtChainCup.set(column_list[1]+str(6),t0 )
         shtChainCup.set(column_list[1]+str(7),sPitch )   
         shtChainCup.set(column_list[1]+str(8),DH) 
         shtChainCup.set(column_list[1]+str(9),DL)  
         shtChainCup.set(column_list[1]+str(10),BS)   
         shtChainCup.set(column_list[1]+str(11),dh1)   
         shtChainCup.set(column_list[1]+str(12),dh2) 
         shtChainCup.set(column_list[1]+str(13),dhmax)   
         shtChainCup.set(column_list[1]+str(14),dhmin) 
         shtChainCup.set(column_list[1]+str(16),cNo)
         shtChainCup.set(column_list[1]+str(17),alpha)
         shtChainCup.set(column_list[1]+str(18),beta)
         shtChainCup.set(column_list[1]+str(19),A0)
         shtChainCup.set(column_list[1]+str(20),B0)

         Spro1.SprocketReference=ref[1:]
         Spro2.SprocketReference=ref[1:]

         key2=shtChainCup.getContents('cNo')
         sa=RDim[key2]
         shtOuter2.set('B2',key2)
         shtOuter2.set('B3',str(sa[0]))#pitch
         shtOuter2.set('B4',str(sa[1]))#h0
         shtOuter2.set('B5',str(sa[2]))#t0
         shtOuter2.set('B6',str(sa[3]))#w0
         shtOuter2.set('B7',str(sa[4]))#d
         shtOuter2.set('B8',str(sa[5]))#d2
         shtOuter2.set('B9',str(sa[6]))#h1
         shtOuter2.set('B10',str(sa[7]))#c0

         shtInner2.set('B2',key2)
         shtInner2.set('B3',str(sa[0]))#pitch
         shtInner2.set('B4',str(sa[1]))#h0
         shtInner2.set('B5',str(sa[2]))#t0
         shtInner2.set('B6',str(sa[3]))#w0
         shtInner2.set('B7',str(sa[4]))#d
         shtInner2.set('B8',str(sa[5]))#d2
         shtInner2.set('B9',str(sa[6]))#h1
         shtInner2.set('B10',str(sa[7]))#c0

         self.label_hole.setText('Hole Diameter Range='+shtChainCup.getContents('dhmin')+'～'+shtChainCup.getContents('dhmax'))
         
         App.ActiveDocument.recompute()

    def create(self): 
         fname='chainCup2.FCStd'           
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','joint_data','chainCup',fname) 
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
        