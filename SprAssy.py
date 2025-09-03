# -*- coding: utf-8 -*-
#from curses import keyname
from ast import Delete
import os
from pickle import TRUE
import sys
import string
from tkinter.tix import ComboBox
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
from prt_data.CSnap_data import paramCSnap

sprType=['ANSI25','ANSI35','ANSI40','ANSI50','ANSI60','ANSI80','ANSI100','ANSI120',
           'ANSI140','ANSI160','ANSI180','ANSI200','ANSI240',]
sprType2=['ANSI50','ANSI60','ANSI80','ANSI100','ANSI120']
sprShape=['1B_1B','2B_2B','1B_1C','2B_2C','1B_1A']
sprTeeth=[i for i in range(9,75)]
string_list = [str(element) for element in sprTeeth]
sprTeeth=string_list
# 画面を並べて表示する
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
        Dialog.resize(250, 400)
        Dialog.move(1000, 0)
        
        #タイプ
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(10, 13, 90, 12))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(110, 10, 90, 22))
        
        #形状
        self.label_shape = QtGui.QLabel('Shape',Dialog)
        self.label_shape.setGeometry(QtCore.QRect(10, 42, 90, 12))
        self.comboBox_shape = QtGui.QComboBox(Dialog)
        self.comboBox_shape.setGeometry(QtCore.QRect(110, 35, 90, 22))
        
        #歯数
        self.label_N1 = QtGui.QLabel('No1',Dialog)
        self.label_N1.setGeometry(QtCore.QRect(110, 63, 50, 12))
        self.label_N2 = QtGui.QLabel('No2',Dialog)
        self.label_N2.setGeometry(QtCore.QRect(160, 63, 50, 12))
        self.label_N = QtGui.QLabel('No of Teeth',Dialog)
        self.label_N.setGeometry(QtCore.QRect(10, 88, 100, 12))
        self.comboBox_N1 = QtGui.QComboBox(Dialog)
        self.comboBox_N1.setGeometry(QtCore.QRect(110, 85, 40, 22))
        self.comboBox_N2 = QtGui.QComboBox(Dialog)
        self.comboBox_N2.setGeometry(QtCore.QRect(160, 85, 40, 22))

        #中心距離
        self.label_L1 = QtGui.QLabel('Plan',Dialog)
        self.label_L1.setGeometry(QtCore.QRect(110, 110, 100, 22))
        self.label_L2 = QtGui.QLabel('Judge',Dialog)
        self.label_L2.setGeometry(QtCore.QRect(160, 110, 100, 22))
        self.label_L = QtGui.QLabel('Center Distance',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 135, 100, 22))
        self.le_L1 = QtGui.QLineEdit('300',Dialog)
        self.le_L1.setGeometry(QtCore.QRect(110, 135, 40, 20))
        self.le_L1.setAlignment(QtCore.Qt.AlignCenter)
        self.le_L2 = QtGui.QLineEdit(Dialog)
        self.le_L2.setGeometry(QtCore.QRect(160, 135, 40, 20))
        self.le_L2.setAlignment(QtCore.Qt.AlignCenter)
        #リンク数
        self.label_Link = QtGui.QLabel('No of Links',Dialog)
        self.label_Link.setGeometry(QtCore.QRect(10, 160, 100, 22))
        self.le_Link1 = QtGui.QLineEdit(Dialog)
        self.le_Link1.setGeometry(QtCore.QRect(110, 160, 40, 20))
        self.le_Link1.setAlignment(QtCore.Qt.AlignCenter)
        self.le_Link2 = QtGui.QLineEdit(Dialog)
        self.le_Link2.setGeometry(QtCore.QRect(160, 160, 40, 20))
        self.le_Link2.setAlignment(QtCore.Qt.AlignCenter)


        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 185, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(140, 185, 60, 22))
        #データ読み込み
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(50, 210, 150, 22))
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 235, 200, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.comboBox_type.addItems(sprType)
        self.comboBox_type.setEditable(True)
        self.comboBox_shape.addItems(sprShape)
        self.comboBox_shape.setEditable(True)
        self.comboBox_N1.setEditable(True)
        self.comboBox_N2.setEditable(True)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.onType)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.read_data)
        #QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)

        #self.comboBox_shape.currentIndexChanged[int].connect(self.onType)
        self.comboBox_N1.currentIndexChanged[int].connect(self.onType)
        
        key2= '1B_1B'#self.comboBox_shape.currentText()''
        #print(key2)
        fname=key2+'.png'
        #fname='1B_1B'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spro_data','sprAssy_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path)) 
        print(joined_path)


        self.retranslateUi(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "SprocketAssy", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onType(self):
        return
        global N_Lst
        #print('ontype000000000000000000')
        key=self.comboBox_shape.currentText()
        N0=self.comboBox_N.currentText()
        fname='Sprocket_'+key+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "prt_data",'Spro_data',fname)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))  
        #selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
        selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj

                         key3=spreadsheet.getContents('I2')
                         #print(key,key3)
                         if key!=key3[1:]:
                             return

                         type=self.comboBox_type.currentText()
                         spreadsheet.set('A2',type)

                         N_Lst=[]
                         #タイプを選択
                         for j in range(0,116):
                             type3=spreadsheet.getContents(column_list[j]+str('18'))[1:]
                             #print(type,type3,j)
                             if type==type3:
                                 break
                         col_type=j  
                         #print(col_type,'coltype')
                         #D0 形状を選択 
                         for s in range(col_type+1,col_type+4):
                             if key=='1B':
                                 sx=s-2
                             elif key=='2B':
                                 sx=s-1
                             elif key=='1C':
                                 sx=s
                             elif key=='2C':
                                 sx=s+1    
                             elif key=='1A':
                                 sx=s-2

                             key2=spreadsheet.getContents(column_list[sx]+str('20'))[1:]
                             if key==key2: 
                                break
                            
                         col_shp=sx 
                         #print(key,key2,col_shp)
                         #歯数を設定 
                         for i in range(21,57):
                             shp_cell=spreadsheet.getContents(column_list[col_shp]+str(i))
                             #print(shp_cell,col_shp)
                             if shp_cell!='':
                                 break
                         col_N=i 

                         N_Lst=[] 
                         for i in range(col_N,57):
                             N_cell=spreadsheet.getContents(column_list[col_type]+str(i))
                             N_Lst.append(N_cell)

                         string_list = [str(element) for element in N_Lst]
                         N_Lst=string_list
                         self.comboBox_N.clear()
                         self.comboBox_N.addItems(N_Lst)
                         #print(N_Lst)

                         if self.comboBox_shape.currentText=='2B' or self.comboBox_shape.setCurrentText=='2C':
                             self.comboBox_type.clear()
                             self.comboBox_type.addItems[sprType2]
                         elif self.comboBox_shape.setCurrentText=='1C':
                             self.comboBox_type.clear()
                             self.comboBox_type.addItems[sprType[2:]]
                          
                                 

                         self.comboBox_N.setCurrentText(spreadsheet.getContents('E2'))
                         
                        
        
    def read_data(self):
         print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj

                         self.comboBox_type.setCurrentText(spreadsheet.getContents('Type')[1:])
                         print('aaaaaaaaaaaaaaaaaa')
                         self.comboBox_shape.setCurrentText(spreadsheet.getContents('Shape')[1:])
                         self.comboBox_N1.setCurrentText(spreadsheet.getContents('sprN1'))
                         self.comboBox_N2.setCurrentText(spreadsheet.getContents('sprN2'))  
                         self.le_L1.setText(spreadsheet.getContents('cd0')) 

                         key2= self.comboBox_shape.currentText()
                         fname=key2+'.png'
                         base=os.path.dirname(os.path.abspath(__file__))
                         joined_path = os.path.join(base, "prt_data",'Spro_data','sprAssy_data',fname)
                         self.label_6.setPixmap(QtGui.QPixmap(joined_path))  
    def update(self):
         global key
         global type
         global N0
         global row_N
         global col_type
         global col_shp
         print('777777777777')
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 # Partsグループが選択されている場合の処理
                 parts_group = selected_object
                 # Partsグループ内のオブジェクトを走査してスプレッドシートを探す
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         # スプレッドシートが見つかった場合の処理
                         spreadsheet = obj
                         
                         # 選択したスプレッドシートを取得
                         type=self.comboBox_type.currentText()
                         key=self.comboBox_shape.currentText()#
                         key3=spreadsheet.getContents('Shape')#shape
                         if key!=key3[1:]:
                             return
                         N1=self.comboBox_N1.currentText()
                         N2=self.comboBox_N2.currentText()
                         Pitch=parts_group.getObject('SPRO_1.Pitch')
                         #Pitch=parts_group.getObject('SPRO_1').Pitch

                         #Pitch=Gui.Selection.addSelection('sprAssy','Part002','Part001.Cut001.Fusion001.Body001.Pad001.Sprocket001.Pitch')
                         print(Pitch)
                         
                         spreadsheet.set('Type',type)
                         spreadsheet.set('B5',N1)
                         spreadsheet.set('B6',N2)
                         

                         App.ActiveDocument.recompute() 
                                
                         return

    def create(self): 
         shp=self.comboBox_shape.currentText()
         fname='Sprocket_'+shp+'.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'prt_data','Spro_data',fname) 
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
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            