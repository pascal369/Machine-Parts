import os
from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD as App
# D,      dia3,   thick_t0, width_b,     dia4,     dia0,    length_a,        length_a1,    length_c
CDim={
'10':(    9.30,      1.0,    1.6,        11.70,     1.2,       3.0,            1.50,         0.40),
'12':(   11.10,      1.0,    1.8,        13.80,     1.5,       3.2,            1.60,         0.45),
'14':(   12.90,      1.0,    2.0,        15.90,     1.7,       3.4,            1.70,         0.50),
'15':(   13.80,      1.0,    2.1,        16.95,     1.7,       3.5,            1.75,         0.52),
'16':(   14.70,      1.0,    2.2,        18.00,     1.7,       3.6,            1.80,         0.55),
'17':(   15.70,      1.0,    2.2,        19.00,     1.7,       3.7,            1.85,         0.55),
'18':(   16.50,      1.0,    2.6,        20.40,     1.7,       3.8,            1.90,         0.65),
'20':(   18.50,      1.2,    2.7,        22.55,     2.0,       3.9,            1.95,         0.67),
'22':(   20.50,      1.2,    2.7,        24.55,     2.0,       4.1,            2.05,         0.67),
'25':(   23.20,      1.2,    3.1,        27.85,     2.0,       4.3,            2.15,         0.77),
'28':(   25.90,      1.6,    3.1,        30.55,     2.0,       4.6,            2.30,         0.78),
'30':(   27.90,      1.6,    3.5,        33.15,     2.0,       4.8,            2.40,         0.88),
'32':(   29.60,      1.6,    3.5,        34.85,     2.5,       5.0,            2.50,         0.88),
'35':(   32.20,      1.6,    4.0,        38.20,     2.5,       5.4,            2.70,         1.00),
'40':(   37.00,      1.8,    4.5,        43.75,     2.5,       5.8,            2.90,         1.13),
'45':(   41.50,      1.8,    4.8,        48.70,     2.5,       6.3,            3.15,         1.20),
'50':(   45.80,      2.0,    5.0,        53.30,     2.5,       6.7,            3.35,         1.25),
'55':(   50.80,      2.0,    5.0,        58.30,     2.5,       7.03,           3.50,         1.25),
'60':(   55.80,      2.0,    5.5,        64.05,     2.5,       7.2,            3.60,         1.38),
'65':(   60.80,      2.5,    6.4,        70.40,     3.0,       7.4,            3.70,         1.60),
'70':(   65.50,      2.5,    6.4,        75.10,     3.0,       7.8,            3.90,         1.60),
'75':(   70.50,      2.5,    7.0,        81.00,     3.0,       7.9,            3.95,         1.75),
'80':(   74.50,      2.5,    7.4,        85.60,     3.0,       8.2,            4.10,         1.85),
'85':(   79.50,      2.5,    8.0,        91.50,     3.0,       8.4,            4.20,         2.00),
'90':(   84.50,      3.0,    8.0,        96.50,     3.0,       8.7,            4.35,         2.00),
'95':(   89.50,      3.0,    8.6,       102.40,     3.0,       9.1,            4.55,         2.15),
'100':(  94.50,      3.0,    9.0,       108.00,     3.0,       9.5,            4.75,         2.25),
       }
class CSnap2:
    def __init__(self, obj):
        self.Type = 'CSnap'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)

    def execute(self, obj):
        label='CSnap'
        key=App.ActiveDocument.getObject(label).key
        sa=CDim
        dia0=sa[5]
        dia3=sa[0]
        dia4=sa[4]
        thick_t0=sa[1]
        width_b=sa[2]
        length_a=sa[5]
        length_a1=sa[6]
        length_c=sa[7]
        '''
        global joined_path
        fname='CSnapring.FCStd'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'prt_data','CSnap_data',fname)  
        try:
            Gui.ActiveDocument.mergeProject(joined_path)
        except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)

        label=obj.Name
        CDia=int(App.ActiveDocument.getObject(label).CDia)
        sa=CDim[CDia]
        print(sa)
        #dia3=sa[1]


       # print(sa)
       '''