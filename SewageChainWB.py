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
from prt_data.CSnap_data import paramCSnap
Series=['ACS19152W','ACS35152W','HighNotch','JAC6205S',]
ACS_Parts=['spro_key','spro_nokey','innerLink','outerLink','SF4','LA1','Y']
Hinotch_Parts=['hispro','hiwheel','hiLink','hiAttach']
JAC_Parts=['Jspro_key','Jspro_nokey','innerLink','outerLink','LpinAttach']
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
        elif key1 ==2:
            Parts=Hinotch_Parts
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
            print(joined_path)
            self.label_6.setPixmap(QtGui.QPixmap(joined_path))
            self.label_6.setAlignment(QtCore.Qt.AlignCenter)
            self.label_6.setObjectName("label_6")
        except:
            pass
        

    def create(self): 
         key1=self.comboBox_Series.currentIndex()
         key2=self.comboBox_Parts.currentIndex()
         name=str(Series[key1])+'_'+str(Parts[key2])
         fname=name+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Chain_data','SewageChain',fname) 
         print(name,fname,joined_path)
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            print('error!')
            return
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            