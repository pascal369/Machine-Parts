# -*- coding: utf-8 -*-
import os
import sys
import string
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

type=['plainBrg','rollingBrg',]
plainBrg=['Ser500SP']
rollingBrg=['60','62','63']
Ser500SP=['06x10','08x12','10x14','12x18','13x19','14x20','15x21','16x22','17x23','18x24',
             '19x26','20x28','20x30','22x32','25x33','25x35','28x38','30x38','30x40','31.5x40',
             '32x42','35x44','35x45','38x48','40x50','40x55','45x55','45x56','45x60',]
rollBrg=['10','12','15','17','20','25','30','35','40','45','50','55','60','65','70','75','80','85',
         '90','95','100',]
nominal=['6','6.3','8','9','10','11.2','12.5','14','16','18']
selFactor=['14','16','18','20','25']


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
        global fname
        global joined_path
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 350)
        Dialog.move(1000, 0)

        #和文
        self.pushButton_la = QtGui.QPushButton('JPN Text',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(10, 10, 30, 22))
        self.le_la = QtGui.QLineEdit('シーブ',Dialog)
        self.le_la.setGeometry(QtCore.QRect(100, 10, 160, 20))
        self.le_la.setAlignment(QtCore.Qt.AlignLeft) 
        #タイプ　Type
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 35, 120, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(130, 35, 100, 22))
        
        #選定係数D/d
        self.label_sel = QtGui.QLabel('SelectionFactor',Dialog)
        self.label_sel.setGeometry(QtCore.QRect(10, 60, 120, 12))
        self.comboBox_sel = QtGui.QComboBox(Dialog)
        self.comboBox_sel.setGeometry(QtCore.QRect(130, 60, 100, 22))
        
        #呼び径　nominal diameter
        self.label_nominal = QtGui.QLabel('Wire nominal Dia',Dialog)
        self.label_nominal.setGeometry(QtCore.QRect(10, 85, 150, 12))
        self.comboBox_nominal = QtGui.QComboBox(Dialog)
        self.comboBox_nominal.setGeometry(QtCore.QRect(130, 85, 100, 22))
        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 113, 200, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 135, 100, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(155, 135, 95, 22))

        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 170, 200, 150))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        

        self.comboBox_type.addItems(type)
        self.comboBox_sel.addItems(selFactor)
        self.comboBox_nominal.addItems(nominal)


        self.comboBox_type.setCurrentIndex(1)
        self.comboBox_type.currentIndexChanged[int].connect(self.onType)
        self.comboBox_type.setCurrentIndex(0)

        self.comboBox_sel.setEditable(True)
        self.comboBox_type.setEditable(True)
        self.comboBox_nominal.setEditable(True)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.readData)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.japan)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Sheave", None))
        
    def japan(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label=obj.Label
        JPN=self.le_la.text()
        try:
            obj.addProperty("App::PropertyString", "JPN",'Base')
            obj.JPN=JPN
        except:
            obj.JPN=JPN

    def readData(self):
        print(self.comboBox_nominal.currentText())
        global spreadsheet_sheave
        global Brg
        global Csnap
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                JPN=obj.JPN
                self.le_la.setText(JPN)
            except:
                pass
        if selection:
            selected_object = selection[0]
            if selected_object.TypeId == "App::Part":
                parts_group = selected_object
                for obj in parts_group.Group:
                    print(obj.Label)
                    if obj.Label[:18]=='spreadsheet_sheave':
                        spreadsheet_sheave=obj
                    elif obj.Label=='Brg'[:3]:
                        Brg=obj     
                    elif obj.Label=='Csnap'[:5]:
                        Csnap=obj
                    self.comboBox_nominal.setCurrentText(spreadsheet_sheave.getContents('A2'))
                    self.comboBox_sel.setCurrentText(spreadsheet_sheave.getContents('M2'))
                    self.comboBox_type.setCurrentText(spreadsheet_sheave.getContents('N2')[1:])
         
    def onType(self):
        key0=self.comboBox_type.currentText()
        if key0=='plainBrg':
            pic='sheave_plain.png'
        elif key0=='rollingBrg':
            pic='sheave_brg.png'
       
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'WireRope',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))
        
    def upDate(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        key0=self.comboBox_type.currentText()
        #print(self.comboBox_nominal.currentText())
        for i in range(16,26):
            d=self.comboBox_nominal.currentText()
            print(d)
            if d==spreadsheet_sheave.getContents('A'+str(i)):
                i0=i
                sf=self.comboBox_sel.currentText()
                for j in range(1,10):
                    if sf==spreadsheet_sheave.getContents(column_list[j]+str(14)):
                        Dp=spreadsheet_sheave.getContents(column_list[j]+str(i))
                        D0=spreadsheet_sheave.getContents(column_list[j+1]+str(i))
                        h=spreadsheet_sheave.getContents(column_list[3]+str(i-13))
                        W=spreadsheet_sheave.getContents(column_list[4]+str(i-13))
                        r=spreadsheet_sheave.getContents(column_list[5]+str(i-13))
                        d0=spreadsheet_sheave.getContents(column_list[6]+str(i-13))
                        Lc=spreadsheet_sheave.getContents(column_list[7]+str(i-13))
                        Dh=spreadsheet_sheave.getContents(column_list[8]+str(i-13))
                        sd3=spreadsheet_sheave.getContents(column_list[14]+str(i-13))
                        st1=spreadsheet_sheave.getContents(column_list[15]+str(i-13))
                        if key0=='plainBrg':
                            Da=spreadsheet_sheave.getContents(column_list[9]+str(i-13))
                            B=spreadsheet_sheave.getContents(column_list[11]+str(i-13))
                        if key0=='rollingBrg':
                            Brg.dia=d0
                            Da=int(Brg.D)
                            Br=Brg.r
                            B=Brg.B
                            print(Br)
                        spreadsheet_sheave.set('A2',d)
                        spreadsheet_sheave.set('B2',Dp)
                        spreadsheet_sheave.set('C2',D0)
                        spreadsheet_sheave.set('D2',h)
                        spreadsheet_sheave.set('E2',W)
                        spreadsheet_sheave.set('F2',r)
                        spreadsheet_sheave.set('G2',d0)
                        spreadsheet_sheave.set('H2',Lc)
                        spreadsheet_sheave.set('I2',Dh)
                        spreadsheet_sheave.set('J2',str(Da))
                        #spreadsheet_sheave.set('K2',str(Br))
                        spreadsheet_sheave.set('L2',str(B))
                        spreadsheet_sheave.set('M2',sf)
                        spreadsheet_sheave.set('O2',sd3)
                        spreadsheet_sheave.set('P2',st1)

                        if key0=='rollingBrg':
                            spreadsheet_sheave.set('K2',str(Br))
                            for m in range(28,36):
                                Da=spreadsheet_sheave.getContents('J2')
                                if Da==spreadsheet_sheave.getContents('A'+str(m)):
                                    cd3=spreadsheet_sheave.getContents('B'+str(m))
                                    ct1=spreadsheet_sheave.getContents('C'+str(m))
                                    cb=spreadsheet_sheave.getContents('D'+str(m))
                                    ca=spreadsheet_sheave.getContents('E'+str(m))
                                    cd0=spreadsheet_sheave.getContents('F'+str(m))
                                    ca5=spreadsheet_sheave.getContents('G'+str(m))
                                    cd1=spreadsheet_sheave.getContents('H'+str(m))
                                    cd2=spreadsheet_sheave.getContents('I'+str(m))
                                    cm1=spreadsheet_sheave.getContents('J'+str(m))
                                    cn=spreadsheet_sheave.getContents('K'+str(m))
                                    
                                    spreadsheet_sheave.set('A27',str(Da))  
                                    #print(Da)
                                    spreadsheet_sheave.set('B27',spreadsheet_sheave.getContents('B'+str(m)))  
                                    spreadsheet_sheave.set('C27',spreadsheet_sheave.getContents('C'+str(m)))  
                                    spreadsheet_sheave.set('D27',spreadsheet_sheave.getContents('D'+str(m)))  
                                    spreadsheet_sheave.set('E27',spreadsheet_sheave.getContents('E'+str(m)))   
                                    spreadsheet_sheave.set('F27',spreadsheet_sheave.getContents('F'+str(m))) 
                                    spreadsheet_sheave.set('G27',spreadsheet_sheave.getContents('G'+str(m))) 
                                    spreadsheet_sheave.set('H27',spreadsheet_sheave.getContents('H'+str(m))) 
                                    spreadsheet_sheave.set('I27',spreadsheet_sheave.getContents('I'+str(m))) 
                                    spreadsheet_sheave.set('J27',spreadsheet_sheave.getContents('J'+str(m))) 
                                    spreadsheet_sheave.set('K27',spreadsheet_sheave.getContents('K'+str(m))) 
                                    break
                        JPN=self.le_la.text()
                        try:
                            obj.addProperty("App::PropertyString", "JPN",'Base')
                            obj.JPN=JPN
                        except:
                            obj.JPN=JPN        
                        App.ActiveDocument.recompute()


                
     
    def create(self): 
        key0=self.comboBox_type.currentText()
        #print(key0)
        d=self.comboBox_nominal.currentText()
        sf=self.comboBox_sel.currentText()
        if key0=='plainBrg':
            if float(sf)<=16:
                fname='sheave_plainBrgA.FCStd'
            else:
                fname='sheave_plainBrgB.FCStd'
                #return    
        elif key0=='rollingBrg':
            d=self.comboBox_nominal.currentText()
            if float(d)<=6.3:
                if float(sf)<=14:
                    fname='sheave_rollingBrgA.FCStd'  
                elif float(sf)>14 :
                    fname='sheave_rollingBrgA1.FCStd'  
            elif float(d)<=9:
                if float(sf)<=14:
                    fname='sheave_rollingBrgA2.FCStd'  
                elif float(sf)<=16:
                    fname='sheave_rollingBrgA21.FCStd'   
                elif float(sf)<=25:
                    fname='sheave_rollingBrgB.FCStd'      
            elif float(d)<=10:
                if float(sf)<=14:
                    fname='sheave_rollingBrgA2.FCStd'  
                elif float(sf)>=16:
                    fname='sheave_rollingBrgB.FCStd'  
            elif float(d)>=11.2:
                if float(sf)<=14:
                    fname='sheave_rollingBrgA2.FCStd'  
                elif float(sf)>=16:
                    fname='sheave_rollingBrgB.FCStd'              
            else:
                pass
                #return
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'prt_data','WireRope',fname) 
        try:
           Gui.ActiveDocument.mergeProject(joined_path)
        except:
           doc=App.newDocument()
           Gui.ActiveDocument.mergeProject(joined_path)

        #Gui.Selection.addSelection('Unnamed','Part')
        #self.readData  
        #App.ActiveDocument.recompute()


        

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint) 
