from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class CShapeSnpGv:
    def __init__(self, obj):
        self.Type = 'CShapeSnpGv'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name 
        L=App.ActiveDocument.getObject(label).L
        D=App.ActiveDocument.getObject(label).D
        n=App.ActiveDocument.getObject(label).n
        m=App.ActiveDocument.getObject(label).m
        for i in range(35):
            try:
                sa=ShaftData.csnap_scr[D]
            except:
                pass

            D=float(D)   

            d1=sa[1]
            d2=sa[2]
            m=sa[3]
            n=sa[4]
            if d1>=D:
                break
        
        #c1= Part.makeCylinder(D/2,L-(m+n),Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        #c2= Part.makeCylinder(d2/2,m,Base.Vector(-m,0,0),Base.Vector(1,0,0),360) 
        c1= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        c2= Part.makeCylinder(d2/2,m,Base.Vector(-m,0,0),Base.Vector(1,0,0),360) 
        c1=c1.fuse(c2)
        #c2= Part.makeCylinder(D/2,n,Base.Vector(-(m+n),0,0),Base.Vector(1,0,0),360) 
        c2= Part.makeCylinder(D/2,n,Base.Vector(-(m+n),0,0),Base.Vector(1,0,0),360) 
        c1=c1.fuse(c2)
        #c1.Placement=App.Placement(App.Vector(-L+m+n,0,),App.Rotation(App.Vector(1,0,0),0))
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
