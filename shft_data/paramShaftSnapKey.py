from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class CShapeSnpKy:
    def __init__(self, obj):
        self.Type = 'CShapeSnpKy'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name 
        keyway=App.ActiveDocument.getObject(label).keyway
        D=App.ActiveDocument.getObject(label).D
        #print(D)
        L=App.ActiveDocument.getObject(label).L
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        n=App.ActiveDocument.getObject(label).n
        for i in range(30):
            key1=ShaftData.key_size[i]
            sa1=ShaftData.key_scr[key1]
            b1=sa1[0]
            t1=sa1[1]
            t2=sa1[2]
            t=t1+t2
            d=sa1[3]
            r=b1/2
            L3=L1-2*r
            D=float(D)  
            if d>=D:
                c1= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
                z=D/2-t1
                break
        t=t1+t2
        r=b1/2
        L3=L1-2*r
        z=D/2-t1
        c1= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        D=App.ActiveDocument.getObject(label).D
        for i in range(35):
            try:
                sa=ShaftData.csnap_scr[D]
            except:
                pass
            d1=sa[1]
            d2=sa[2]
            m=sa[3]
            #n=sa[3]
            D=float(D)  
            if d1>=D:
                break
        def keyway2(self):
            global c0
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
            c0=wface.extrude(Base.Vector(0,0,t))

        c1= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        c2= Part.makeCylinder(d2/2,m,Base.Vector(-m,0,0),Base.Vector(1,0,0),360) 
        c1=c1.fuse(c2)
        c2= Part.makeCylinder(D/2,n,Base.Vector(-(m+n),0,0),Base.Vector(1,0,0),360) 
        c1=c1.fuse(c2) 
        #Part.show(c1)
        keyway2(self)  #キー表示 
        c2=c0
        if keyway==True:
            Part.show(c2)

        c1=c1.cut(c2)
        g=c1.Volume*7850/10**9 
        #print(g)
    
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