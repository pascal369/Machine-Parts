from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App

class Tube:
    def __init__(self, obj):
        self.Type = 'ScrBrg'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        def basic(self):
            global c0
            c0= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        label=obj.Name 
        L=App.ActiveDocument.getObject(label).L
        D=App.ActiveDocument.getObject(label).D
        d0=App.ActiveDocument.getObject(label).d0
        basic(self)
        c1=c0
        c2= Part.makeCylinder(d0/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        c1=c1.cut(c2)
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
        I=round(1/8*g*((D/10)**2+(d0/10)**2),4)
        try:
            obj.addProperty("App::PropertyFloat", "I",label)
            obj.I=I
            obj.ViewObject.Proxy=0
        except:
            obj.I=I
            obj.ViewObject.Proxy=0 
        obj.Shape=c1 