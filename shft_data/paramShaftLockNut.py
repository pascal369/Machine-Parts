from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class ScrBrg6:
    def __init__(self, obj):
        self.Type = 'ScrBrg'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name 
        ScrewDia=App.ActiveDocument.getObject(label).ScrewDia
        dia=ScrewDia
        L=App.ActiveDocument.getObject(label).L
        #D=App.ActiveDocument.getObject(label).D
        type=App.ActiveDocument.getObject(label).type
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        L3=App.ActiveDocument.getObject(label).L3
        thread=App.ActiveDocument.getObject(label).thread
        keyway=App.ActiveDocument.getObject(label).keyway
        print(keyway)
        #for i in range(34):
        #dia=ShaftData.screw_size[i]
        sa2=ShaftData.fine_screw[dia]
        p=float(sa2[0])
        z=p/2
        H1=sa2[1]
        D0=float(sa2[2])
        #print(D0)
        D1=float(sa2[4])
        sa=ShaftData.brg_scr[dia]
        Bn=float(sa[7])
        k=float(sa[6])
        s=float(sa[8])
        t=float(sa[11])
        #L1=int(Bn+t+1)
        #if D0>=D:
        #    break
        #IsChecked=App.ActiveDocument.getObject(label).IsChecked
        def hexagon_bolt(self):
            global c00
            
            global sa2
            global p
            global H1
            global D0
            global s
            global k
            
            sa2=ShaftData.fine_screw[dia]
            p=sa2[0]
            z=p/2
            H1=sa2[1]
            D0=sa2[2]
            D1=sa2[4]
            k=sa[6]
            s=sa[8]
            H0=0.86625*p
            x=H1+H0/8
            y=x*math.tan(math.pi/6)
            r0=D0/2+H0/8
            a=p/2-y
            z=p/2
            #ボルト部
            cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c00=cb
            p1=(-D0/2,0,0)
            p2=(-D0/2,0,z)
            p3=(-D0/2+z,0,0)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0.0,0.0,1.0),360)#面取り
            #ねじ断面
            if thread==True:
                p1=(D1/2,0,-a)
                p2=(D1/2-a/2,0,0)
                p3=(D1/2,0,a)
                p4=(r0,0,p/2)
                p5=(r0,0,-p/2)
                edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
                edge2 = Part.makeLine(p3,p4)
                edge3 = Part.makeLine(p4,p5)
                edge4 = Part.makeLine(p5,p1)
                #らせん_sweep
                helix=Part.makeHelix(p,p+L1,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                try:
                    cutProfile.Placement=App.Placement(App.Vector(0,0,-1.5*p),App.Rotation(App.Vector(0,0,1),0))
                except:
                    pass
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c00=c00.cut(pipe)
            c00=c00.cut(c0)
            #Part.show(c00)
        #L2=L1    
        hexagon_bolt(self)
        c2=c00
        c1=c2
        c2= Part.makeCylinder(D0/2,L-L1,Base.Vector(0,0,L1),Base.Vector(0,0,1),360)
        c1=c1.fuse(c2)
        c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
        #座金溝
        a=s
        r=a/2
        b=(D0-k)+0.5
        c=k-D0/2
        d=b*2
        p1=(0,-a/2,c)
        p2=(0,a/2,c)
        p3=(L1,a/2,c)
        p4=(L1+r,0,c)
        p5=(L1,-a/2,c)
        p6=(-r,0,c)
        edge1 = Part.makeLine(p1,p2)
        edge2 = Part.makeLine(p2,p3)
        edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
        edge4 = Part.makeLine(p5,p1)
        edge5=Part.Arc(Base.Vector(p1),Base.Vector(p6),Base.Vector(p2)).toShape()
        w10=Part.Wire([edge1,edge2,edge3,edge4])
        wface=Part.Face(w10)
        c2=wface.extrude(Base.Vector(0,0,d))
        c1=c1.cut(c2)

        for i in range(30):
            key1=ShaftData.key_size[i]
            sa=ShaftData.key_scr[key1]
            b1=sa[0]
            t1=sa[1]
            t2=sa[2]
            d=sa[3]
            if d>=D0:
                break
        t=t1+t2
        r=b1/2
        z=D0/2-t1
        print(b1)
        def keyway2(self):
            global c0
            #L2=App.ActiveDocument.getObject(label).L2
            #L2=float(L2)
            #L2=L1
            p1=(L1+L3+r,r,z)
            p2=(L1+L2+L3-r,r,z)
            p3=(L1+L2+L3,0,z)
            p4=(L1+L2+L3-r,-r,z)
            p5=(L1+L3+r,-r,z)
            p6=(L1+L3,0,z)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.Arc(Base.Vector(p2),Base.Vector(p3),Base.Vector(p4)).toShape()
            edge3=Part.makeLine(p4,p5)
            edge4=Part.Arc(Base.Vector(p5),Base.Vector(p6),Base.Vector(p1)).toShape()
            awire=Part.Wire([edge1,edge2,edge3,edge4])
            #Part.show(awire)
            wface=Part.Face(awire)
            c0=wface.extrude(Base.Vector(0,0,t))
            #Part.show(c0)
      
        keyway2(self)
        c2=c0
        c2.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),180)
        if keyway==True:
            Part.show(c2)
        c1=c1.cut(c2)
        g=c0.Volume*7850/10**9 
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
        obj.Shape=c1 