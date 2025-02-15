from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class KeyWayBoss:
    def __init__(self, obj):
        self.Type = 'KeyWayBoss'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        D=App.ActiveDocument.getObject(label).D
        #key1=App.ActiveDocument.getObject(label).key1
        for i in range(30):
            key1=ShaftData.key_size[i]
            sa=ShaftData.key_scr[key1]
            b1=float(sa[0])
            t1=float(sa[1])
            t2=float(sa[2])
            t=t1+t2
            d=sa[3]
            r=b1/2
            if d>=D:
                break
        st=math.asin(b1/D)
        x=D/2*math.sin(st)
        h=D/2*math.cos(st)
        p1=(0,-x,h)
        p2=(0,-x,D/2+t2)
        p3=(0,x,D/2+t2)
        p4=(0,x,h)
        p5=(0,0,-D/2)
        edge1=Part.Arc(Base.Vector(p1),Base.Vector(p5),Base.Vector(p4)).toShape()
        edge2=Part.makeLine(p4,p3)
        edge3=Part.makeLine(p2,p3)
        edge4=Part.makeLine(p1,p2)
        awire=Part.Wire([edge1,edge2,edge3,edge4])
        wface=Part.Face(awire)
        c1=wface
        g=c1.Volume*7850/10**9 
        label='mass[kg]'
        try:
            #obj.addProperty("App::PropertyFloat", "body",label)
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass    
        obj.Shape=c1 