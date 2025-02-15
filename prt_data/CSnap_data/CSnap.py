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
from prt_data import paramCSnapShaft
CType=['00_CSnap_shaft','01_CSnap_hole']
CDia=['10','12','14','15','16','17','18','20','22','25','28','30','32','35','40','45','50','55','60','65','70','75','80','85','90','95','100',]

class Ui_Dialog(object):
  
    def setupUi(self, Dialog):
        global fname
        global joined_path
        '''
        fname='CSnap_shaft.FCStd'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'prt_data','CSnap_data',fname) 
        try:
            Gui.ActiveDocument.mergeProject(joined_path)
        except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
        '''
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 100)
        Dialog.move(900, 0)
        #タイプ　nominal diameter
        self.label_type = QtGui.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 150, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(80, 10, 80, 22))

        #呼び径　nominal diameter
        self.label_dia = QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(10, 38, 150, 12))
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(80, 35, 80, 22))
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 50, 80, 22))

        self.comboBox_type.addItems(CType)
        self.comboBox_dia.addItems(CDia)
        
        self.comboBox_dia.setCurrentIndex(1)
        self.comboBox_dia.currentIndexChanged[int].connect(self.onDia)
        self.comboBox_dia.setCurrentIndex(0)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "軸用C形止め輪", None))
        self.label_dia.setText(QtGui.QApplication.translate("Dialog", "呼び径", None))    
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "実行", None))  

    def onDia(self):
         global key0
         global dia
         global label
         key0=self.comboBox_type.currentIndex()
         dia=self.comboBox_dia.currentText()
         if key0==0:
              label='CSnap_Shaft'
         #print(dia4)
         pass    

    def create(self):  
         #print(key0)
         #print(label)
         
         
         if key0==0:
              '''
              fname='CSnap_shaft.FCStd'
              base=os.path.dirname(os.path.abspath(__file__))
              joined_path = os.path.join(base, 'prt_data','CSnap_data',fname) 
              try:
                  Gui.ActiveDocument.mergeProject(joined_path)
              except:
                  doc=App.newDocument()
                  Gui.ActiveDocument.mergeProject(joined_path)
              #label=joined_path 
              '''
              label='CSnap_Shaft'
              obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
              dia=CDia
              obj.addProperty("App::PropertyEnumeration",'dia',label)
              obj.dia=dia
              i=self.comboBox_dia.currentIndex()
              obj.dia=dia[i] 
              paramCSnapShaft.CSnapShaft(obj)


class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.show()        