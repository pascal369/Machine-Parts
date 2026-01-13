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

type=['inlet','outlet','chute','chute3']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 450)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 240, 200, 200))
        self.label_6.setText("")
        

        #type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.label_type.setStyleSheet("color: black;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 130, 22))

        #W
        self.label_0 = QtGui.QLabel('    1                  2',Dialog)
        self.label_0.setGeometry(QtCore.QRect(80, 35, 150, 20))
        self.label_0.setStyleSheet("color: black;")
        self.label_W = QtGui.QLabel('W',Dialog)
        self.label_W.setGeometry(QtCore.QRect(10, 60, 100, 22))
        self.label_W.setStyleSheet("color: black;")
        self.le_W0 = QtGui.QLineEdit('300',Dialog)
        self.le_W0.setGeometry(QtCore.QRect(80, 60, 50, 20))
        self.le_W0.setAlignment(QtCore.Qt.AlignCenter)
        self.le_W1 = QtGui.QLineEdit('300',Dialog)
        self.le_W1.setGeometry(QtCore.QRect(160, 60, 50, 20))
        self.le_W1.setAlignment(QtCore.Qt.AlignCenter)

        #L
        self.label_L = QtGui.QLabel('L',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 85, 100, 22))
        self.label_L.setStyleSheet("color: black;")
        self.le_L0 = QtGui.QLineEdit('300',Dialog)
        self.le_L0.setGeometry(QtCore.QRect(80, 85, 50, 20))
        self.le_L0.setAlignment(QtCore.Qt.AlignCenter)
        self.le_L1 = QtGui.QLineEdit('300',Dialog)
        self.le_L1.setGeometry(QtCore.QRect(160, 85, 50, 20))
        self.le_L1.setAlignment(QtCore.Qt.AlignCenter)

        #Angle
        self.label_Angle = QtGui.QLabel('Angle',Dialog)
        self.label_Angle.setGeometry(QtCore.QRect(10, 110, 100, 22))
        self.label_Angle.setStyleSheet("color: black;")
        self.le_sita0 = QtGui.QLineEdit('0',Dialog)
        self.le_sita0.setGeometry(QtCore.QRect(80, 110, 50, 20))
        self.le_sita0.setAlignment(QtCore.Qt.AlignCenter)
        self.le_sita1 = QtGui.QLineEdit('0',Dialog)
        self.le_sita1.setGeometry(QtCore.QRect(160, 110, 50, 20))
        self.le_sita1.setAlignment(QtCore.Qt.AlignCenter)

        #full length
        self.label_FL = QtGui.QLabel('Full Length',Dialog)
        self.label_FL.setGeometry(QtCore.QRect(10, 135, 100, 22))
        self.label_FL.setStyleSheet("color: black;")
        self.le_FL = QtGui.QLineEdit('150',Dialog)
        self.le_FL.setGeometry(QtCore.QRect(80, 135, 130, 20))
        self.le_FL.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 175, 50, 22))
        #更新
        self.pushButton3 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(125, 175, 50, 22))
        #インポート
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(30, 200, 185, 22))

        self.comboBox_type.addItems(type)

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)

        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_type.setCurrentIndex(0)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Chute", None))

    def onType(self):
        if self.comboBox_type.currentText()=='chute':
            fname='chute.png'
        elif self.comboBox_type.currentText()=='inlet':
            fname='inlet.png'    
        elif self.comboBox_type.currentText()=='outlet':
            fname='outlet.png'    
        elif self.comboBox_type.currentText()=='chute3':
            fname='chute3.png'          

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'chute_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")
        return
    def import_data(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                    if obj.TypeId == "Spreadsheet::Sheet":
                        spreadsheet = obj
                    
                    
        self.comboBox_type.setCurrentText(spreadsheet.getContents('A1')[1:])

        if self.comboBox_type.currentText()=='inlet' :
            self.le_W0.setText(spreadsheet.getContents('w0')) 
            self.le_L0.setText(spreadsheet.getContents('l0'))  
            self.le_sita0.setText(spreadsheet.getContents('sita0')) 
            self.le_FL.setText(spreadsheet.getContents('h0')) 
            self.le_W1.setText('') 
            self.le_L1.setText('')  
            self.le_sita1.setText('') 
            
        elif self.comboBox_type.currentText()=='outlet' :
            self.le_W0.setText('') 
            self.le_L0.setText('')  
            self.le_sita0.setText('') 
            
            self.le_W1.setText(spreadsheet.getContents('w0')) 
            self.le_L1.setText(spreadsheet.getContents('l0'))  
            self.le_sita1.setText(spreadsheet.getContents('sita0')) 
            self.le_FL.setText(spreadsheet.getContents('h0'))     

        elif self.comboBox_type.currentText()=='chute':
            self.le_W0.setText(spreadsheet.getContents('w0'))   
            self.le_W1.setText(spreadsheet.getContents('w1'))  
            self.le_L0.setText(spreadsheet.getContents('l0'))  
            self.le_L1.setText(spreadsheet.getContents('l1')) 
            self.le_sita0.setText(spreadsheet.getContents('sita0')) 
            self.le_sita1.setText(spreadsheet.getContents('sita1')) 
            self.le_FL.setText(spreadsheet.getContents('FL')) 
        elif self.comboBox_type.currentText()=='chute3' :
            self.le_W0.setText(spreadsheet.getContents('w0')) 
            self.le_L0.setText(spreadsheet.getContents('l0'))  
            self.le_sita0.setText(spreadsheet.getContents('sita0')) 
            self.le_FL.setText(spreadsheet.getContents('h0')) 
            self.le_W1.setText('') 
            self.le_L1.setText('')  
            self.le_sita1.setText('')     

    def update(self):
         w0=self.le_W0.text()
         w1=self.le_W1.text()
         l0=self.le_L0.text()
         l1=self.le_L1.text()
         sita0=self.le_sita0.text()
         sita1=self.le_sita1.text()
         FL=self.le_FL.text()
         try:
             if self.comboBox_type.currentText()=='inlet':
                 #print('aaaaaaaaaaaaaaa')
                 spreadsheet.set('w0',w0)
                 spreadsheet.set('l0',l0)
                 spreadsheet.set('sita0',sita0)
                 spreadsheet.set('h0',FL)
             elif self.comboBox_type.currentText()=='outlet':
                 spreadsheet.set('w0',w1)
                 spreadsheet.set('l0',l1)
                 spreadsheet.set('sita0',sita1)
                 spreadsheet.set('h0',FL)
             elif self.comboBox_type.currentText()=='chute':
                 spreadsheet.set('w0',w0)
                 spreadsheet.set('w1',w1) 
                 spreadsheet.set('l0',l0)
                 spreadsheet.set('l1',l1)
                 spreadsheet.set('sita0',sita0)
                 spreadsheet.set('sita1',sita1)
                 spreadsheet.set('FL',FL)
             elif self.comboBox_type.currentText()=='chute3':
                 #print('aaaaaaaaaaaaaaa')
                 spreadsheet.set('w0',w0)
                 spreadsheet.set('l0',l0)
                 spreadsheet.set('sita0',sita0)
                 spreadsheet.set('h0',FL)    
         except:
             return 
         App.ActiveDocument.recompute()

    def create(self): 
         if self.comboBox_type.currentText()=='inlet':
             fname='inlet.FCStd'
         elif self.comboBox_type.currentText()=='outlet':
             fname='outlet.FCStd'    
         elif self.comboBox_type.currentText()=='chute':
             fname='chute.FCStd'
         elif self.comboBox_type.currentText()=='chute3':
             fname='chute3.FCStd'    

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','chute_data',fname) 
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
        