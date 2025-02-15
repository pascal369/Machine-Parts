from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class Key:
    def __init__(self, obj):
        self.Type = 'Key'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        D=App.ActiveDocument.getObject(label).D
        L1=App.ActiveDocument.getObject(label).L1
        for i in range(30):
                key1=ShaftData.key_size[i]
                sa=ShaftData.key_scr[key1]
                b1=sa[0]
                t1=sa[1]
                t2=sa[2]
                t=t1+t2
                d=sa[3]
                r=b1/2
                if d>=D:
                    z=D/2-t1
                    break
        L3=L1-r
        p1=(0,r,z)
        p2=(L3,r,z)
        p3=(L3+r,0,z)
        p4=(L3,-r,z)
        p5=(0,-r,z)
        edge1=Part.makeLine(p1,p2)
        edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
        edge3=Part.makeLine(p4,p5)
        edge4=Part.makeLine(p5,p1)
        awire=Part.Wire([edge1,edge2,edge3,edge4])
        wface=Part.Face(awire)
        c2=wface.extrude(Base.Vector(0,0,t))
        c1=c2
        g=c1.Volume*7850/10**9 
        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass  
        label='Inertia[kg-cm2]'  
        R=D/(20)
        I=round(1/2*g*R**2,5)
        try:
            obj.addProperty("App::PropertyFloat", "I",label)
            obj.I=I
            obj.ViewObject.Proxy=0
        except:
            obj.I=I
            obj.ViewObject.Proxy=0
        obj.Shape=c1