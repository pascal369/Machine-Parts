from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class KeyWay:
    #print('aaaaaaaaaaaaaaaa')
    def __init__(self, obj):
        self.Type = 'KeyWay'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
        #return
    def execute(self, obj):
        #print('111111111111111111')  
        label=obj.Name
        type=App.ActiveDocument.getObject(label).type
        key=type[3:]
        Key=App.ActiveDocument.getObject(label).Key
        D=App.ActiveDocument.getObject(label).D
        L=App.ActiveDocument.getObject(label).L
        L1=App.ActiveDocument.getObject(label).L1
        #print(key)
        if key=='keyway_2':
            L2=App.ActiveDocument.getObject(label).L2
            #print(L2)
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
                    c1= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
                    z=D/2-t1
                    break
        if key=='keyway_1':
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
            c1=c1.cut(c2)
            if Key==True:
                #Part.show(c2)
                c1=c1.fuse(c2)
            #Part.show(c1)    
        elif key=='keyway_2':
            L3=L1-2*r
            p1=(L2+r,r,z)
            p2=(L2+r+L3,r,z)
            p3=(L2+L1,0,z)
            p4=(L2+r+L3,-r,z)
            p5=(L2+r,-r,z)
            p6=(L2,0,z)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
            edge3=Part.makeLine(p4,p5)
            edge4=Part.Arc(Base.Vector(p5),Base.Vector(p6),Base.Vector(p1)).toShape()
            awire=Part.Wire([edge1,edge2,edge3,edge4])
            wface=Part.Face(awire)
            c2=wface.extrude(Base.Vector(0,0,t))
            c1=c1.cut(c2)
            if Key==True:
                #Part.show(c2)
                c1=c1.fuse(c2)

            
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