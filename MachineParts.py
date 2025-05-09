import os
import sys
import csv
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi

buhin=['Wire rope','Rolling bearing','Plain bearing','GearAssy','driveChainAssy','Chain','Screws','Pins','Shaft','Snap Ring',
       'Oil seal','Gland Packing','Spring','End Plate','Key Plate','Joint','Shaped Steel','Planar shape','One-touch window'
       ,'Handle',]

chain=['Roller Chain','Water treatment chain','Link Chains']
spro=['Drive Chains',]
snapring=['for shafts','for holes']
spring=['Tensile coil spring','Compression coil springs']
bearing=['Ball Bearings受','Double-row outward tapered roller bearing']
shaft=['Shaft','Screw shaft']
joint=['Tube Split Joint',]
Gear=['Helical gears','Worm Gear','Bevel gear','Planetary gears',]
GlandP=['Gland Packing Assy',]
pin=['Cotter Pin']
Wire=['Shackle','Thimble','Wire Clip','Shackle Assembly','Sheave']

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 200)
        Dialog.move(1000, 0)
        #部品
        self.comboBox_buhin = QtGui.QComboBox(Dialog)
        self.comboBox_buhin.setGeometry(QtCore.QRect(80, 11, 130, 20))
        self.label_buhin = QtGui.QLabel('Parts',Dialog)
        self.label_buhin.setGeometry(QtCore.QRect(11, 11, 61, 16))
        #部品2
        self.comboBox_buhin2 = QtGui.QComboBox(Dialog)
        self.comboBox_buhin2.setGeometry(QtCore.QRect(80, 36, 130, 20))
        self.label_buhin2 = QtGui.QLabel('Parts2',Dialog)
        self.label_buhin2.setGeometry(QtCore.QRect(11, 36, 61, 16))
        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(80, 60, 100, 23))
        self.pushButton_m.setObjectName("pushButton") 
        #質量集計
        self.pushButton_m20 = QtGui.QPushButton('massTally_csv',Dialog)
        self.pushButton_m20.setGeometry(QtCore.QRect(180, 60, 150, 23))
        self.pushButton_m2 = QtGui.QPushButton('massTally_SpreadSheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(180, 85, 150, 23))
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(80, 110, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(180, 110, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(80, 135, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(180, 135, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')
        #実行
        self.pushButton = QtGui.QPushButton('Execution',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 160, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_buhin.addItems(buhin)
        self.comboBox_buhin.setCurrentIndex(1)
        self.comboBox_buhin.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_buhin.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m20, QtCore.SIGNAL("pressed()"), self.massTally2)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'Machine_Parts(JIS_Standard)', None))
        
    def massImput(self):
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g
         
    def massCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        g=obj.Shape.Volume*g0*1000/10**9  
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            
        except:
            pass

    def massTally2(self):#csv
        doc = App.ActiveDocument
        objects = doc.Objects
        mass_list = []
        for obj in objects:
            if Gui.ActiveDocument.getObject(obj.Name).Visibility:
                if obj.isDerivedFrom("Part::Feature"):
                    if hasattr(obj, "mass"):
                        try:
                            mass_list.append([obj.Label, obj.dia,'1', obj.mass])
                        except:
                            mass_list.append([obj.Label, '','1', obj.mass])    

                else:
                     pass
        doc_path = doc.FileName
        csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_counts_and_masses.csv"
        csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name",'Standard','Count', "Mass[kg]"])
            writer.writerows(mass_list) 
    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        # 新しいスプレッドシートを作成
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "PartList")
        spreadsheet.Label = "Parts List"
        
        # ヘッダー行を記入
        headers = ['No',"Name",'Standard', 'Count','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            try:
                spreadsheet.set(f"E{row}", f"{obj.mass:.2f}")  # mass
                s=obj.mass+s
                if hasattr(obj, "Shape") and obj.Shape.Volume > 0:
                    try:
                        spreadsheet.set(f"A{row}", str(row-1))  # No
                        spreadsheet.set(f"B{row}", obj.Label) 
                        try:
                            spreadsheet.set(f"C{row}", obj.dia)
                        except:
                            pass
                        spreadsheet.set(f"D{row}", '1')   # count
                        row += 1
                    except:
                        pass    
            except:
                pass
            spreadsheet.set(f'E{row}',s)
        App.ActiveDocument.recompute()
        Gui.activeDocument().activeView().viewAxometric()

    def onSpec(self):
        global buhin
        global pic
        buhin=self.comboBox_buhin.currentText()
        self.comboBox_buhin2.clear()
        self.comboBox_buhin2.show()
        if buhin=='Wire rope':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(Wire)
            return
        elif buhin=='Pins':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(pin)
        elif buhin=='Rolling bearing':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Plain bearing':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Screws':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Shaft':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(shaft)
            return
        elif buhin=='Chain':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(chain)
            return
        elif buhin=='Snap Ring':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(snapring)
            return
        elif buhin=='Oil seal':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Gland Packing':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(GlandP)
            return
        elif buhin=='Spring':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(spring)
            return
        elif buhin=='End Plate':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Key Plate':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Joint':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(joint)
            return
        elif buhin=='Planar shape':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Shaped Steel':
            self.comboBox_buhin2.hide()
        elif buhin=='One-touch window':
            self.comboBox_buhin2.hide()    
            return
        elif buhin=='GearAssy':
            self.comboBox_buhin2.show()  
            self.comboBox_buhin2.addItems(Gear)  
        elif buhin=='driveChainAssy':
            self.comboBox_buhin2.hide() 
        elif buhin=='Handle':
            self.comboBox_buhin2.hide()       
        
    def create(self):
         buhin=self.comboBox_buhin.currentText()
         buhin2=self.comboBox_buhin2.currentText()
         if buhin=='Wire rope':
           if buhin2=='Shackle':
               import Shackle 
           elif buhin2=='Thimble' :
               import Thimble
           elif buhin2=='Wire Clip' :
               import WireClip
           elif buhin2=='Shackle Assembly':
               fname='shackleAssy.FCStd'  
               base=os.path.dirname(os.path.abspath(__file__))
               joined_path = os.path.join(base,'prt_data','WireRope',fname) 
               try:
                  Gui.ActiveDocument.mergeProject(joined_path)
               except:
                  doc=App.newDocument()
                  Gui.ActiveDocument.mergeProject(joined_path)  
           elif buhin2=='Sheave':
             import sheave
         elif buhin=='Pins':
             if buhin2=='Cotter Pin':
                 import CotterPin
                   
         elif buhin=='Rolling bearing':
            import RollingBearing   
         elif buhin=='Plain bearing':
            import plainBrg   
         elif buhin=='Screws':
             import Screws
         elif buhin=='Shaft':
           if buhin2=='Shaft':
               import Shaft 
           elif buhin2=='Screw shaft' :
               import ScrewShaft   
         elif buhin=='Chain':
           if buhin2=='Roller Chain':
               import RollerChain
           elif buhin2=='Water treatment chain':    
               import SewageChainWB  
           elif buhin2=='Link Chains':    
               import LinkChain 
         elif buhin=='Snap Ring':
           if buhin2=='for shafts':
               import CSnapring
           elif buhin2=='for holes':    
               import CSnapring_hole   
         elif buhin=='Oil seal':
             import OilSeal
         elif buhin=='Gland Packing':
             if buhin2=='Gland Packing Assy':
                 import GlandpackingAssy 
             #elif buhin2=='Gland Packing':
             #    import Glandpacking   
             #elif buhin2=='Lantern Ring':
             #    import Lanternring 
             #elif buhin2=='Ground presser':
             #    import GlandPresser 
             #elif buhin2=='Stuffing Box':
             #    import StuffingBox     
         elif buhin=='One-touch window':
             import OneTouchWindow  
             return
         elif buhin=='Spring':
           if buhin2=='Tensile coil spring':
               import TensionCoilSpring
           elif buhin2=='Compression coil springs':    
               import CompressionCoilSpring
               #return  
         elif buhin=='End Plate':
               import EndPlate    
         elif buhin=='Key Plate':
               import KeyPlate              
         elif buhin=='Joint':
           if buhin2=='Tube Split Joint':
               import SplitTubeJoint   
         elif buhin=='Planar shape':
              import Pln_shape  
         elif buhin=='Shaped Steel':
              import Shaped_steel   
         elif buhin=='GearAssy':
           if buhin2=='Spur gears':
              import sperGear
           elif buhin2=='Helical gears':
               import helicalGear   
           elif buhin2=='Worm Gear':
               import wormGear  
           elif buhin2=='Bevel gear':
               import bevelGear  
           elif buhin2=='Planetary gears':
               import planetaryGears   
           elif buhin2=='Hypocycloidal gear':
               import hypoCycloidGears  
         elif buhin=='driveChainAssy':
             import Sprocket  
         elif buhin=='Handle':
             import Handle

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()


        
