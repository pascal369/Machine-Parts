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
from ScrLib import ScrData
blt_size=['M8','M10','M12','M16','M20','M24']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 350)
        Dialog.move(1000, 0)
        
        #軸径　nominal diameter
        self.label_dia = QtGui.QLabel('shaftDia',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(50, 13, 150, 22))
        self.label_dia.setStyleSheet("color: black;")
        self.le_dia = QtGui.QLineEdit('100',Dialog)
        self.le_dia.setGeometry(QtCore.QRect(130, 10, 100, 22))
        self.le_dia.setAlignment(QtCore.Qt.AlignCenter)
        #ボルト径　bolt diameter
        self.label_blt = QtGui.QLabel('boltDia',Dialog)
        self.label_blt.setGeometry(QtCore.QRect(50, 38, 150, 22))
        self.label_blt.setStyleSheet("color: black;")
        self.combo_blt = QtGui.QComboBox(Dialog)
        self.combo_blt.setGeometry(QtCore.QRect(130, 35, 100, 22))
        self.combo_blt.setEditable(True)
        self.combo_blt.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #板厚　
        self.label_t = QtGui.QLabel('Plate thickness',Dialog)
        self.label_t.setGeometry(QtCore.QRect(50, 63, 150, 22))
        self.label_t.setStyleSheet("color: black;")
        self.le_t = QtGui.QLineEdit('10',Dialog)
        self.le_t.setGeometry(QtCore.QRect(130, 63, 100, 22))
        self.le_t.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(15, 95, 90, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(108, 95, 80, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(200, 95, 90, 22))

         #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 125, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'shft_data',"EndPlate.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.combo_blt.addItems(blt_size)


        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "EndPlate", None))
        
    def read_data(self):
         global washer
         global bolt
         global spreadsheet
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label[:21]=='Spring_washer_general':
                         washer=obj
                     elif obj.Label[:12]=='hexagon_bolt':
                         bolt=obj    
                     elif obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
    
                         self.le_dia.setText(spreadsheet.getContents('dia'))
                         self.combo_blt.setCurrentText(spreadsheet.getContents('size')[1:])
                         self.le_t.setText(spreadsheet.getContents('t0')) 
                         
    def update(self):
         
         selection = Gui.Selection.getSelection()
         '''
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object

                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj
        '''             
         dia=self.le_dia.text()
         t=self.le_t.text()
         size=self.combo_blt.currentText()
         D0=float(dia)+10.0
         for i in range(11,16):
              size_value = spreadsheet.getContents('A'+str(i))
              if size == size_value[1:]:
                break
         Db=spreadsheet.getContents('B'+str(i)) 
         l1=spreadsheet.getContents('C'+str(i))  
         l2=float(spreadsheet.getContents('C'+str(i))) *0.9

         sa=ScrData.p_washer[size]
         tw=sa[17]
         
         #tw=washer.t
         #print(tw)
         bolt.dia=size
         washer.dia = size  
         washer.t = tw
         bolt.dia = size  
         
         spreadsheet.set('dia',dia)    
         spreadsheet.set('t0',t)
         spreadsheet.set('size',size)
         spreadsheet.set('D0',str(D0))
         spreadsheet.set('Db',Db)
         spreadsheet.set('l1',l1)
         spreadsheet.set('l2',str(l2))
         spreadsheet.set('tw',str(tw))
                            
         App.ActiveDocument.recompute()

    def create(self): 
        
         fname='EndPlate.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'shft_data',fname) 
        
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
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            