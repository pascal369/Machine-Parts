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

ton=['4t','10t',]


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 280)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 80, 200, 200))
        self.label_6.setText("aaa")
        
        #ton
        self.label_ton = QtGui.QLabel(Dialog)
        self.label_ton.setGeometry(QtCore.QRect(10, 13, 150, 22))
        self.label_ton.setStyleSheet("color: black;")
        self.comboBox_ton = QtGui.QComboBox(Dialog)
        self.comboBox_ton.setGeometry(QtCore.QRect(80, 8, 90, 22))
        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 35, 80, 22))
        #更新
        #self.pushButton2 = QtGui.QPushButton(Dialog)
        #self.pushButton2.setGeometry(QtCore.QRect(80, 60, 80, 22))
        #インポート
        #self.pushButton3 = QtGui.QPushButton(Dialog)
        #self.pushButton3.setGeometry(QtCore.QRect(80, 60, 80, 22))

        self.comboBox_ton.addItems(ton)

        self.comboBox_ton.setCurrentIndex(1)
        self.comboBox_ton.currentIndexChanged[int].connect(self.on_type)
        self.comboBox_ton.setCurrentIndex(0)

        #QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        #QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        #QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Handle", None))
        self.label_ton.setText(QtGui.QApplication.translate("Dialog", "Capacity", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        #self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "upDate", None))  
        #self.pushButton3.setText(QtGui.QApplication.translate("Dialog", "import", None))  
    def on_type(self):
        Capacity=self.comboBox_ton.currentText()
        if Capacity=='4t':
            pic='4tDump.png'
        elif Capacity=='10t':
            pic='10tDump.png'    
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'DumpCar_data',pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
    #def import_data(self):
    #    global spreadsheet
    #    
    #    selection = Gui.Selection.getSelection()
    #    if selection:
    #         selected_object = selection[0]
            #if selected_object.TypeId == "App::Part":
            #    parts_group = selected_object
            #    for obj in parts_group.Group:
            #       if obj.TypeId == "Spreadsheet::Sheet":
            #           spreadsheet = obj
    

    def create(self): 
         Capacity=self.comboBox_ton.currentText()
         if Capacity=='4t':
             fname='4tDump.FCStd'   
         else:
            fname='10tDump.FCStd'    

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'DumpCar_data',fname) 
         #doc=App.newDocument()
         #print(joined_path)
         Gui.ActiveDocument.mergeProject(joined_path)
        

         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)               