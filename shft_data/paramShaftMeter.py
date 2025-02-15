from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class Meter:
    def __init__(self, obj):
        self.Type = 'ScrBrg'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name 
        ScrewDia=App.ActiveDocument.getObject(label).ScrewDia
        dia=ScrewDia
        L=App.ActiveDocument.getObject(label).L
        type=App.ActiveDocument.getObject(label).type
        L1=App.ActiveDocument.getObject(label).L1
        thread=App.ActiveDocument.getObject(label).thread
        sa2=ShaftData.regular[dia]
        p=float(sa2[0])
        z=p/2
        H1=sa2[1]
        D0=float(sa2[2])
        D1=float(sa2[4])

        def hexagon_bolt(self):
            global c0
            global c00
            sa=ShaftData.regular[dia]
            p=sa[0]
            H1=sa[1]
            m=sa[6]
            m1=sa[7]
            s0=sa[8]
            e0=sa[9]
            D0=sa[2]
            D2=sa[3]
            D1=sa[4]
            dk=sa[5]
            n=sa[11]
            z=p/2
            H0=0.86625*p
            x=H1+H0/8
            y=x*math.tan(math.pi/6)
            r0=D0/2+H0/8
            a=p/2-y
            #ボルト部
            c00= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(1,0,0),360)#ボルト部
            p1=(0,D0/2,0)
            p2=(0,D0/2-z,0)
            p3=(z,D0/2,0)
            p4=(-z,D0/2,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)#ボルト先端カット
            plist=[p1,p2,p4,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c01=wface.revolve(Base.Vector(L1,0,0),Base.Vector(1,0,0),360)#ボルト先端カット
            c00=c00.cut(c0)
            c00=c00.cut(c01)
            #Part.show(c00)
            #Part.show(c00)
            #ねじ断面
            if thread==True:
                p1=(-a,D1/2,0)
                p2=(a,D1/2,0)
                p3=(p/2,r0,0)
                p4=(-p/2,r0,0)
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeLine(p2,p3)
                edge3 = Part.makeLine(p3,p4)
                edge4 = Part.makeLine(p4,p1)
                #らせん_sweep

                if ScrewDia=='M12':
                    helix=Part.makeHelix(p,p+L1,D0/2,0,False)
                else:
                    helix=Part.makeHelix(p,L1,D0/2,0,False)

                helix.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                #Part.show(helix)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c00=c00.cut(pipe)
                #Part.show(c00)
                #Part.show(pipe)
                
       
        hexagon_bolt(self)
        c1=c00
        c2= Part.makeCylinder(D0/2,L-L1,Base.Vector(L1,0,0),Base.Vector(1,0,0),360)
        c1=c1.fuse(c2)
        #c1=c1.cut(c0)
        #Part.show(c1)
        #Part.show(c2)
        

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
        R=D0/(20)
        I=round(1/2*g*R**2,5)
        try:
            obj.addProperty("App::PropertyFloat", "I",label)
            obj.I=I
            obj.ViewObject.Proxy=0
        except:
            obj.I=I
            obj.ViewObject.Proxy=0 
        #c1.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))  
        #c1.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))  
        obj.Shape=c1 