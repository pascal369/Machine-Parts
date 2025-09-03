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
from shft_data import paramShaftBasic
from shft_data import paramShaftKeyway
from shft_data import paramShaftKey_2
from shft_data import paramShaftKey
from shft_data import paramShaftSnap
from shft_data import paramShaftSnapKey
from shft_data import paramShaftBrgNut
from shft_data import paramShaftLockNut
from shft_data import paramShaftTube
from shft_data import paramShaftKeywayBoss
from shft_data import paramShaftMeter
from shft_data import paramShaftBothMeter
from shft_data import ShaftData

DEBUG = True # set to True to show debug messages
#JIS B 1181
class ViewProvider:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
        return

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 460)
        Dialog.move(1000, 0)
        #shape type
        self.shape = QtGui.QLabel('ShapeType',Dialog)
        self.shape.setGeometry(QtCore.QRect(30, 15, 50, 12))
        self.combo_shape = QtGui.QComboBox(Dialog)
        self.combo_shape.setGeometry(QtCore.QRect(100, 10, 159, 22))
        #screw dia
        self.screw_dia = QtGui.QLabel('Screw dia',Dialog)
        self.screw_dia.setGeometry(QtCore.QRect(30, 40, 50, 12))
        self.combo_sc_dia = QtGui.QComboBox(Dialog)
        self.combo_sc_dia.setGeometry(QtCore.QRect(100, 35, 69, 22))
        #width screw dia display
        self.checkbox = QtGui.QCheckBox('Screw display',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(180, 35, 120, 23))
        #dim D
        self.lbl_D = QtGui.QLabel('D[mm]',Dialog)
        self.lbl_D.setGeometry(QtCore.QRect(30, 65, 50, 12))
        self.le_D = QtGui.QLineEdit(Dialog)
        self.le_D.setGeometry(QtCore.QRect(100, 65, 50, 20))
        self.le_D.setAlignment(QtCore.Qt.AlignCenter)
        #dim L
        self.lbl_L = QtGui.QLabel('L[mm]',Dialog)
        self.lbl_L.setGeometry(QtCore.QRect(170, 70, 50, 12))
        self.le_L = QtGui.QLineEdit(Dialog)
        self.le_L.setGeometry(QtCore.QRect(220, 65, 50, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)
        #dim L1
        self.lbl_L1 = QtGui.QLabel('L1[mm]',Dialog)
        self.lbl_L1.setGeometry(QtCore.QRect(30, 100, 50, 12))
        self.le_L1 = QtGui.QLineEdit(Dialog)
        self.le_L1.setGeometry(QtCore.QRect(100, 95, 50, 20))
        self.le_L1.setAlignment(QtCore.Qt.AlignCenter)
        #dim L2
        self.lbl_L2 = QtGui.QLabel('L2[mm]',Dialog)
        self.lbl_L2.setGeometry(QtCore.QRect(170, 100, 50, 12))
        self.le_L2 = QtGui.QLineEdit(Dialog)
        self.le_L2.setGeometry(QtCore.QRect(220, 95, 50, 20))
        self.le_L2.setAlignment(QtCore.Qt.AlignCenter)
        #dim L3
        self.lbl_L3 = QtGui.QLabel('L3[mm]',Dialog)
        self.lbl_L3.setGeometry(QtCore.QRect(30, 125, 50, 12))
        self.le_L3 = QtGui.QLineEdit(Dialog)
        self.le_L3.setGeometry(QtCore.QRect(100, 120, 50, 20))
        self.le_L3.setAlignment(QtCore.Qt.AlignCenter)
        #dim d0
        self.lbl_d0 = QtGui.QLabel('d0[mm]',Dialog)
        self.lbl_d0.setGeometry(QtCore.QRect(170, 125, 50, 12))
        self.le_d0 = QtGui.QLineEdit(Dialog)
        self.le_d0.setGeometry(QtCore.QRect(220, 120, 50, 20))
        self.le_d0.setAlignment(QtCore.Qt.AlignCenter)
        #c_shaped retaining_ring
        self.lbl_c = QtGui.QLabel('C_shaped retaining ring D',Dialog)
        self.lbl_c.setGeometry(QtCore.QRect(30, 150, 150, 12))
        self.combo_c = QtGui.QComboBox(Dialog)
        self.combo_c.setGeometry(QtCore.QRect(170, 145, 50, 22))
        #dim m
        self.lbl_m = QtGui.QLabel('m[mm]',Dialog)
        self.lbl_m.setGeometry(QtCore.QRect(60, 175, 50, 12))
        self.le_m = QtGui.QLineEdit(Dialog)
        self.le_m.setGeometry(QtCore.QRect(100, 170, 50, 20))
        self.le_m.setAlignment(QtCore.Qt.AlignCenter)
        #dim n
        self.lbl_n = QtGui.QLabel('n[mm]',Dialog)
        self.lbl_n.setGeometry(QtCore.QRect(185, 175, 60, 12))
        self.le_n = QtGui.QLineEdit(Dialog)
        self.le_n.setGeometry(QtCore.QRect(220, 170, 50, 20))
        self.le_n.setAlignment(QtCore.Qt.AlignCenter)
        #key_size
        self.lbl_key = QtGui.QLabel('key_size',Dialog)
        self.lbl_key.setGeometry(QtCore.QRect(30, 200, 240, 12))
        #key_display
        self.checkbox2 = QtGui.QCheckBox('with key',Dialog)
        self.checkbox2.setGeometry(QtCore.QRect(180, 200, 195, 23))
        #create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 225, 240, 22))
        #mass
        self.pushButton_2 = QtGui.QPushButton('mass culculation',Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 400, 240, 24))
        self.pushButton_2.setObjectName("pushButton")
        
        self.mtrl = QtGui.QLabel('Specific gravity of material',Dialog)
        self.mtrl.setGeometry(QtCore.QRect(30, 428, 150, 12))
        self.le_mtrl = QtGui.QLineEdit(Dialog)
        self.le_mtrl.setGeometry(QtCore.QRect(180, 425, 50, 20))
        self.le_mtrl.setAlignment(QtCore.Qt.AlignCenter)
        #img
        self.img = QtGui.QLabel(Dialog)
        self.img.setStyleSheet("background-color:#ffffff;");
        self.img.setGeometry(QtCore.QRect(30, 250, 240, 140))
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        
        self.retranslateUi(Dialog)
        self.combo_shape.addItems(ShaftData.shape_type)
        self.combo_sc_dia.addItems(ShaftData.screw_size)
        self.combo_c.addItems(ShaftData.csnap_size)
        self.combo_shape.setCurrentIndex(1)
        self.combo_shape.currentIndexChanged[int].connect(self.on_shape)
        self.combo_shape.currentIndexChanged[int].connect(self.on_key)
        self.combo_shape.setCurrentIndex(0)
        self.combo_c.currentIndexChanged[int].connect(self.on_shape)
        self.le_D.textChanged.connect(self.on_key)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.on_create)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("pressed()"), self.on_mass)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Shaft generator", None))
   
    def on_mass(self):
        doc = App.activeDocument()
        object_list = []
        for obj in doc.Objects:
            if hasattr(obj, "mass"):
                if obj.ViewObject.isVisible():
                    object_list.append([obj.Label, 1, obj.mass,obj.I])

    def on_shape(self):
        global sa
        global m
        global n
        global d2
        #global key
        global key_c
        key=self.combo_shape.currentText()
        pic='shaft_' + key[:2] +'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "shft_data",pic)
        self.img.setPixmap(QtGui.QPixmap(joined_path))
        self.le_D.setText('15')
        self.le_d0.setText('14')
        self.le_L.setText('45')
        self.le_L1.setText('15')
        self.le_L2.setText('15')
        self.le_L3.setText('5')
        self.le_mtrl.setText('7.85')
        if key=='03_C_shape snapring groove' or key=='04_C_shape snapring groove with keyway' :
            key_scr1=self.combo_sc_dia.currentText()
            sa=ShaftData.brg_scr[key_scr1]
            Bn=sa[7]
            t=sa[11]
            L1=Bn+t+1
            self.le_L1.setText(str(L1))
            key_c=self.combo_c.currentText()
            sa=ShaftData.csnap_scr[key_c]
            D=float(sa[1])
            d2=float(sa[2])
            n=float(sa[4])
            m=float(sa[3])
            
            self.le_D.setText(str(D))
            self.le_m.setText(str(m))
            self.le_n.setText(str(n))

        elif key=='12_meterScrew' or key=='13_bothMeterScrew':
            self.combo_sc_dia.clear()
            self.combo_sc_dia.addItems(ShaftData.screwSizeM) 
        else:
            self.combo_sc_dia.clear()
            self.combo_sc_dia.addItems(ShaftData.screw_size)    

       
    def on_key(self):
        key=self.combo_shape.currentText()
        if key=='02_keyway_2' or key=='04_C_shape snapring groove with keyway' or key=='6_Lock nut':
            for i in range(30):
                key1=ShaftData.key_size[i]
                sa=ShaftData.key_scr[key1]
                d=float(sa[3])
                D=float(self.le_D.text()) 
                if d>=D:
                    self.lbl_key.setText(QtGui.QApplication.translate("Dialog", "key_size bxh     "+key1, None))
                    break

    def on_create(self):
        key=self.combo_shape.currentText()
        #print(key)
        #try:
        label=key[3:]
        #obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        #    g0=float(self.le_mtrl.text())
        #    obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
        #except:
        #    pass
        if key=='00_basic':
            D=float(self.le_D.text()) 
            L=float(self.le_L.text())
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            obj.addProperty("App::PropertyFloat", "D",'shaft').D=D
            obj.addProperty("App::PropertyString", "type",'shaft').type=key
            st='d'+str(D)+'x'+str(L)+'L'
            obj.addProperty("App::PropertyString", 'Standard','Standard').Standard=st

            paramShaftBasic.Basic(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 

        elif key=='01_keyway_1':
            #return
            fname='keyway_1.FCStd'
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, 'shft_data',fname) 
            Gui.ActiveDocument.mergeProject(joined_path)

        elif  key=='02_keyway_2' :
            global key1
            D=float(self.le_D.text()) 
            L=float(self.le_L.text())  
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0     
            obj.addProperty("App::PropertyEnumeration", "type",'shaft')
            obj.type=ShaftData.shape_type[1:3]
            i=self.combo_shape.currentIndex()
            obj.type=ShaftData.shape_type[i] 

            obj.addProperty("App::PropertyFloat", "D",'shaft').D=D
            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            L1=float(self.le_L1.text())
            L2=float(self.le_L2.text())
            obj.addProperty("App::PropertyFloat", "L1",'keyway').L1=L1
            if key[3:]=='keyway_2':    
                obj.addProperty("App::PropertyFloat", "L2",'keyway').L2=L2

            if self.checkbox2.isChecked():
                obj.addProperty("App::PropertyBool",'Key','keyway').Key = True
            else:
                obj.addProperty("App::PropertyBool",'Key','keyway').Key = False
             
            paramShaftKeyway.KeyWay(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 
           
        elif key=='03_C_shape snapring groove':
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyEnumeration", "D",'shaft')
            obj.D=ShaftData.csnap_size
            i=self.combo_c.currentIndex()
            obj.D=ShaftData.csnap_size[i]   
            L=float(self.le_L.text())  
            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            m=float(sa[3])
            obj.addProperty("App::PropertyFloat", "m",'shaft').m=m
            n=float(sa[4])
            obj.addProperty("App::PropertyFloat", "n",'shaft').n=n

            paramShaftSnap.CShapeSnpGv(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 
        
        elif key=='04_C_shape snapring groove with keyway':
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyEnumeration", "D",'shaft')
            obj.D=ShaftData.csnap_size
            i=self.combo_c.currentIndex()
            obj.D=ShaftData.csnap_size[i]
            L=float(self.le_L.text()) 
            L1=float(self.le_L1.text())
            L2=float(self.le_L2.text())
            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            obj.addProperty("App::PropertyFloat", "L1",'keyway').L1=L1
            obj.addProperty("App::PropertyFloat", "L2",'keyway').L2=L2
            n=float(sa[4])
            obj.addProperty("App::PropertyFloat", "n",'shaft').n=n

            if self.checkbox2.isChecked():
                obj.addProperty("App::PropertyBool",'Key','keyway').Key = True
            else:
                obj.addProperty("App::PropertyBool",'Key','keyway').Key = False

            paramShaftSnapKey.CShapeSnpKy(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 
        
        elif key=='05_screws for bearing' or key=='07_screws for bearing2':
            dia1=self.combo_sc_dia.currentText()
            D=float(self.le_D.text()) 
            L=float(self.le_L.text()) 
            L1=float(self.le_L1.text())
            L2=float(self.le_L2.text())
            L3=float(self.le_L3.text())
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyString", "type",'shaft').type=key
            
            obj.addProperty("App::PropertyEnumeration", "ScrewDia",label)
            obj.ScrewDia=ShaftData.screw_size
            i=self.combo_sc_dia.currentIndex()
            obj.ScrewDia=ShaftData.screw_size[i]  

            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            obj.addProperty("App::PropertyFloat", "L1",'keyway').L1=L1
            if key=='07_screws for bearing2':
                #print(key)
                obj.addProperty("App::PropertyFloat", "D",'shaft').D=D
                obj.addProperty("App::PropertyFloat", "L2",'keyway').L2=L2


            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool",'thread','screw').thread = True
            else:
                obj.addProperty("App::PropertyBool",'thread','screw').thread = False

            paramShaftBrgNut.ScrBrg5(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute()           
        elif key=='06_Lock nut' :
            dia1=self.combo_sc_dia.currentText()
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyEnumeration", "ScrewDia",label)
            obj.ScrewDia=ShaftData.screw_size
            i=self.combo_sc_dia.currentIndex()
            obj.ScrewDia=ShaftData.screw_size[i]

            L=float(self.le_L.text())
            L1=float(self.le_L1.text())
            L2=float(self.le_L2.text())
            L3=float(self.le_L3.text())

            obj.addProperty("App::PropertyEnumeration", "type",'shaft')
            obj.type=ShaftData.shape_type[5:7]
            i=self.combo_shape.currentIndex()
            obj.type=ShaftData.shape_type[i] 
            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            obj.addProperty("App::PropertyFloat", "L1",'keyway').L1=L1
            obj.addProperty("App::PropertyFloat", "L2",'keyway').L2=L2
            obj.addProperty("App::PropertyFloat", "L3",'keyway').L3=L3
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool",'thread','screw').thread = True
            else:
                obj.addProperty("App::PropertyBool",'thread','screw').thread = False

            if self.checkbox2.isChecked():
                obj.addProperty("App::PropertyBool",'Key','keyway').Key = True
            else:
                obj.addProperty("App::PropertyBool",'Key','keyway').Key = False    
            
            paramShaftLockNut.ScrBrg6(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 
 
        elif key=='08_tube':
            d0=float(self.le_d0.text())
            D=float(self.le_D.text()) 
            L=float(self.le_L.text())
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyFloat", "L",'tube').L=L
            obj.addProperty("App::PropertyFloat", "D",'tube').D=D
            obj.addProperty("App::PropertyFloat", "d0",'tube').d0=d0
            paramShaftTube.Tube(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 
        elif key=='09_keyway_boss':
            D=float(self.le_D.text()) 
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyFloat", "D",'shaft').D=D
            paramShaftKeywayBoss.KeyWayBoss(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute() 
        elif key=='10_Key_1':
            D=float(self.le_D.text()) 
            L1=float(self.le_L1.text())
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyFloat", "D",'Key').D=D
            obj.addProperty("App::PropertyFloat", "L1",'Key').L1=L1
            paramShaftKey.Key(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute()  
        elif key=='11_Key_2':
            D=float(self.le_D.text()) 
            L1=float(self.le_L1.text())
            L2=float(self.le_L2.text())
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyFloat", "D",'Key').D=D
            obj.addProperty("App::PropertyFloat", "L1",'Key').L1=L1
            paramShaftKey_2.Key(obj) 
            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute()  
        elif key=='12_meterScrew' or key=='13_bothMeterScrew':
            dia1=self.combo_sc_dia.currentText()
            D=float(self.le_D.text()) 
            L=float(self.le_L.text()) 
            L1=float(self.le_L1.text())
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            g0=float(self.le_mtrl.text())
            obj.addProperty("App::PropertyFloat", "g0",'shaft').g0=g0
            obj.addProperty("App::PropertyString", "type",'shaft').type=key
            
            obj.addProperty("App::PropertyEnumeration", "ScrewDia",label)
            obj.ScrewDia=ShaftData.screwSizeM
            i=self.combo_sc_dia.currentIndex()
            obj.ScrewDia=ShaftData.screwSizeM[i]  

            obj.addProperty("App::PropertyFloat", "L",'shaft').L=L
            obj.addProperty("App::PropertyFloat", "L1",'shaft').L1=L1

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool",'thread','screw').thread = True
            else:
                obj.addProperty("App::PropertyBool",'thread','screw').thread = False

            if key=='13_bothMeterScrew':
                paramShaftBothMeter.BothMeter(obj) 
            else:    
                paramShaftMeter.Meter(obj) 

            obj.ViewObject.Proxy=0
            App.ActiveDocument.recompute()                
 
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)                    