# -*- coding: utf-8 -*-
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
       ,'Handle','Chute','DumpCar']
buhin_jpn=['ワイヤロープ','転がり軸受','すべり軸受','ギヤアセンブリ','駆動チェンアセンブリ','チェン','ねじ類','ピン類','軸','止め輪',
       'オイルシール','グランドパッキン','ばね','エンドプレート','キープレート','軸継手','形鋼','平面形状','ワンタッチ窓'
       ,'ハンドル','シュート','ダンプカー']
chain=['Roller Chain','Water treatment chain','Link Chains']
chain_jpn=['ローラーチェン','水処理用チェン','リンクチェン']
spro=['Drive Chains',]
spro_jpn=['ドライブチェンアッセンブリ']
snapring=['for shafts','for holes']
snapring_jpn=['軸用止め輪','穴用止め輪']
spring=['Tensile coil spring','Compression coil springs']
spring_jpn=['引張コイルバネ','圧縮コイルバネ']
bearing=['単列深溝形玉軸受','複列円錐ころ軸受_外向']
shaft=['Shaft','Screw shaft']
shaft_jpn=['軸','スクリュー軸']
joint=['Tube Split Joint',]
joint_jpn=['筒割形軸継手',]
Gear=['Helical gears','Worm Gear','Bevel gear','Planetary gears','Hypocycloidal gear']
Gear_jpn=['ヘリカルギヤ','ウオームギヤ','ベベルギヤ','プラネタリーギヤ','ハイポサイクロイドギヤ']
GlandP=['Gland Packing Assy',]
GlandP_jpn=['グランドパッキンアセンブリ',]
pin=['Cotter Pin']
pin_jpn=['コッターピン']
Wire=['Shackle','Thimble','Wire Clip','Shackle Assembly','Sheave']
Wire_jpn=['シャックル','シンブル','ワイヤークリップ','シャックルアセンブリ','シーブ']
lang=['English','Japanese']
mater=['SS41','SUS304','S45C','PVC','Neoprene rubber']
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 275)
        Dialog.move(1000, 0)
        #部品
        self.comboBox_buhin = QtGui.QComboBox(Dialog)
        self.comboBox_buhin.setGeometry(QtCore.QRect(80, 11, 130, 20))
        self.label_buhin = QtGui.QLabel('Parts',Dialog)
        self.label_buhin.setGeometry(QtCore.QRect(11, 11, 61, 16))
        #言語
        self.pushButton_la=QtGui.QPushButton('language',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(210, 10, 130, 23))
        self.comboBox_lan = QtGui.QComboBox(Dialog)
        self.comboBox_lan.setGeometry(QtCore.QRect(210, 35, 130, 22))
        self.comboBox_lan.setEditable(True)
        self.comboBox_lan.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        #部品2
        self.comboBox_buhin2 = QtGui.QComboBox(Dialog)
        self.comboBox_buhin2.setGeometry(QtCore.QRect(80, 36, 130, 20))
        self.label_buhin2 = QtGui.QLabel('Parts2',Dialog)
        self.label_buhin2.setGeometry(QtCore.QRect(11, 36, 61, 16))

        #jpn text
        self.pushButton_jpn = QtGui.QPushButton('Jpn Text',Dialog)
        self.pushButton_jpn.setGeometry(QtCore.QRect(80, 60, 50, 23))
        self.le_jpn = QtGui.QLineEdit(Dialog)
        self.le_jpn.setGeometry(QtCore.QRect(170, 63, 170, 20))
        self.le_jpn.setAlignment(QtCore.Qt.AlignCenter)  

        #standard
        self.pushButton_st = QtGui.QPushButton('Standard',Dialog)
        self.pushButton_st.setGeometry(QtCore.QRect(80, 85, 50, 23))
        self.le_st = QtGui.QLineEdit(Dialog)
        self.le_st.setGeometry(QtCore.QRect(170, 88, 170, 20))
        self.le_st.setAlignment(QtCore.Qt.AlignCenter) 

        #material
        self.pushButton_mt = QtGui.QPushButton('Material',Dialog)
        self.pushButton_mt.setGeometry(QtCore.QRect(80, 110, 50, 23))
        self.comboBox_mt = QtGui.QComboBox(Dialog)
        self.comboBox_mt.setGeometry(QtCore.QRect(170, 110, 170, 22))
        self.comboBox_mt.setEditable(True)
        self.comboBox_mt.lineEdit().setAlignment(QtCore.Qt.AlignCenter)


        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(80, 135, 130, 23))
        self.pushButton_m.setObjectName("pushButton") 
        #質量集計
        self.pushButton_m2 = QtGui.QPushButton('massTally_SpreadSheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(210, 135, 130, 23))
        #count
        self.pushButton_ct = QtGui.QPushButton('Count',Dialog)
        self.pushButton_ct.setGeometry(QtCore.QRect(80, 160, 100, 23))
        self.le_ct = QtGui.QLineEdit(Dialog)
        self.le_ct.setGeometry(QtCore.QRect(180, 160, 50, 20))
        self.le_ct.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_ct.setText('1')
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(80, 185, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(180, 185, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(80, 210, 80, 12))
        self.lbl_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(180, 210, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        #sketchLength
        self.pushButtonS = QtGui.QPushButton('SketchLength',Dialog)
        self.pushButtonS.setGeometry(QtCore.QRect(180, 235, 75, 23))
        self.pushButtonS.setObjectName("pushButton")

        #実行S
        self.pushButton = QtGui.QPushButton('Execution',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 235, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_buhin.addItems(buhin)

        self.comboBox_buhin.setCurrentIndex(1)
        self.comboBox_buhin.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_buhin.setCurrentIndex(0)

        self.comboBox_lan.addItems(lang)
        self.comboBox_mt.addItems(mater)

        #QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.language)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_ct, QtCore.SIGNAL("pressed()"), self.countCulc)
        QtCore.QObject.connect(self.pushButton_jpn, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QObject.connect(self.pushButton_st, QtCore.SIGNAL("pressed()"), self.standard)
        QtCore.QObject.connect(self.pushButton_mt, QtCore.SIGNAL("pressed()"), self.material)
        QtCore.QObject.connect(self.pushButtonS, QtCore.SIGNAL("pressed()"), self.sketchLength)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'Machine_Parts(JIS_Standard)', None))
        
    def japan(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label=obj.Label
        JPN=self.le_jpn.text()
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN

    def standard(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        #label=obj.Label
        Standard=self.le_st.text()
        try:
            obj.addProperty("App::PropertyString", "Standard",'Standard')
            obj.Standard=Standard
        except:
            obj.Standard=Standard      
    def material(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        #label=obj.Label
        material=self.comboBox_mt.currentText()
        print(material)
        try:
            obj.addProperty("App::PropertyString", 'material','material')
            obj.material=material
        except:
            obj.material=material      


    def language(self):
        doc = App.activeDocument()
        if doc:
            group_names = []
            for obj in doc.Objects:
                try:
                    gengo=self.comboBox_lan.currentText()
                    label2=obj.JPN
                    label=self.comboBox_buhin.currentText()
                    if gengo=='Japanese':
                       obj.Label=label2
                    else:
                       obj.Label=label 
                except:
                    pass     
    def countCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        count=int(self.le_ct.text())
        try:
            obj.addProperty("App::PropertyFloat", "count",label)
            obj.count=count
        except:
            obj.count=count 

    def sketchLength(self):
        obj = Gui.Selection.getSelection()[0]  # 選択されたオブジェクトを取得
        if obj is None or obj.TypeId != "Sketcher::SketchObject":
            FreeCAD.Console.PrintError("スケッチを選択してください\n")
        else:
            total_length = 0.0
            for geo in obj.Geometry:
                if isinstance(geo, (Part.LineSegment, Part.ArcOfCircle )):
                           total_length += geo.length()
            FreeCAD.Console.PrintMessage(f"スケッチ '{obj.Label}' の合計エッジ長: {total_length} mm\n")

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
            obj.mass=g
            pass
    
    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        spreadsheet = doc.getObject("Parts_List") 
        if spreadsheet is None:
            spreadsheet = doc.addObject("Spreadsheet::Sheet", "Parts_List")
        
        # ヘッダー行を記入
        gengo=self.comboBox_lan.currentText()
        if gengo=='Japanese':
            headers = ['No','名称','材質','規格', '数量','単重[kg]','重量[kg]']
        elif gengo=='English':
            headers = ['No','Name','Material','Standard', 'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            spreadsheet.set(f"F{1}", headers[5])
            spreadsheet.set(f"G{1}", headers[6])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if hasattr(obj, "count") and obj.count > 0:
                try:
                    spreadsheet.set(f"A{row}", str(row-1))  # No
                    if gengo=='English':
                        n=obj.count
                        spreadsheet.set(f'B{row}',obj.Label)    
                    elif gengo=='Japanese':
                        #
                        n=obj.count
                        try:
                            spreadsheet.set(f"B{row}", obj.JPN) 
                        except:
                            spreadsheet.set(f"B{row}", obj.Base_JPN)  
                    try:
                        spreadsheet.set(f"C{row}", obj.material)
                    except:
                        pass
                    try:
                        spreadsheet.set(f"D{row}", obj.Standard)
                    except:
                        pass
                    
                    spreadsheet.set(f"E{row}", f"{n:.2f}")   # count
                    spreadsheet.set(f"F{row}", f"{obj.mass:.2f}")  # unit
                    spreadsheet.set(f"G{row}", f"{obj.mass*n:.2f}")  # mass
                except:
                    pass    
                s=obj.mass*n+s
                row += 1
                
            spreadsheet.set(f'G{row}',str(s))
        App.ActiveDocument.recompute()

    def onSpec(self):
        global buhin
        global pic
        
        buhin=self.comboBox_buhin.currentText()
        i=self.comboBox_buhin.currentIndex()
        self.comboBox_buhin2.clear()
        self.comboBox_buhin2.show()
        if buhin=='Wire rope':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(Wire)
            #self.le_jpn.text(buhin[i])
            #return
        elif buhin=='Pins':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(pin)
        elif buhin=='Rolling bearing':
            self.comboBox_buhin2.hide()
            #return
        elif buhin=='Plain bearing':
            self.comboBox_buhin2.hide()
            #return
        elif buhin=='Screws':
            self.comboBox_buhin2.hide()
            #return
        elif buhin=='Shaft':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(shaft)
            #return
        elif buhin=='Chain':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(chain)
            #return
        elif buhin=='Snap Ring':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(snapring)
            #return
        elif buhin=='Oil seal':
            self.comboBox_buhin2.hide()
            #return
        elif buhin=='Gland Packing':
            self.comboBox_buhin2.show()
            self.comboBox_buhin2.addItems(GlandP)
            #return
        elif buhin=='Spring':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(spring)
            #return
        elif buhin=='End Plate':
            self.comboBox_buhin2.hide()
            return
        elif buhin=='Key Plate':
            self.comboBox_buhin2.hide()
            #return
        elif buhin=='Joint':
            self.comboBox_buhin2.clear()
            self.comboBox_buhin2.addItems(joint)
            #return
        elif buhin=='Planar shape':
            self.comboBox_buhin2.hide()
            #return
        elif buhin=='Shaped Steel':
            self.comboBox_buhin2.hide()
        elif buhin=='One-touch window':
            self.comboBox_buhin2.hide()    
            #return
        elif buhin=='GearAssy':
            self.comboBox_buhin2.show()  
            self.comboBox_buhin2.addItems(Gear)  
        elif buhin=='driveChainAssy':
            self.comboBox_buhin2.hide() 
        elif buhin=='Handle' or buhin=='DumpCar':
            self.comboBox_buhin2.hide()  
        jpn=buhin_jpn[i]
        print(jpn)
        self.le_jpn.setText(jpn)   
        
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
            RollingBearing 
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

         elif buhin=='One-touch window':
             import OneTouchWindow  
             return
         elif buhin=='Spring':
           if buhin2=='Tensile coil spring':
               import TensionCoilSpring
           elif buhin2=='Compression coil springs':    
               import CompressionCoilSpring

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
         elif buhin=='Chute':
             import chute  
         elif buhin=='DumpCar':
             import DumpCar      

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()


        
