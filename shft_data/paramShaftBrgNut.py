from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import FreeCAD as App
from . import ShaftData
class ScrBrg5:
    def __init__(self, obj):
        self.Type = 'ScrBrg'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name 
        ScrewDia=App.ActiveDocument.getObject(label).ScrewDia
        dia=ScrewDia
        type=App.ActiveDocument.getObject(label).type
        key=type[:2]
        #print(type,key,'aaaaaaaaaaaaaaa')

        L=App.ActiveDocument.getObject(label).L
        #D=App.ActiveDocument.getObject(label).D
        thread=App.ActiveDocument.getObject(label).thread
        L1=App.ActiveDocument.getObject(label).L1
        if key=='06':
            L2=App.ActiveDocument.getObject(label).L2
            L3=App.ActiveDocument.getObject(label).L3
        elif key=='07':
            D=App.ActiveDocument.getObject(label).D
            L2=App.ActiveDocument.getObject(label).L2

        g0=App.ActiveDocument.getObject(label).g0

        #for i in range(34):
        #dia=ShaftData.screw_size[i]
        sa2=ShaftData.fine_screw[dia]
        p=float(sa2[0])
        z=p/2
        H1=sa2[1]
        D0=float(sa2[2])
        D1=float(sa2[4])
        sa=ShaftData.brg_scr[dia]
        Bn=float(sa[7])
        k=float(sa[6])
        s=float(sa[8])
        t=float(sa[11])
        #L1=int(Bn+t+1)
        #if D0>=D:
        #    break

        def hexagon_bolt(self):
            global c00
            global sa2
            global p
            global H1
            #global D0
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
            
            #Part.show(c01)
            cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c00=cb
            #print(key)
            
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
                #try:
                if  D0==45.0 or D0==50.0 or D0==80.0 :
                    cutProfile.Placement=App.Placement(App.Vector(0,0,-2.0*p),App.Rotation(App.Vector(0,0,1),0))
                    #print(D0,'aaaaaaaaaaaaaaaaaaaaaaaa')
                elif  D0==110.0 or D0==115.0 or D0==130.0 or D0==150.0 :
                    cutProfile.Placement=App.Placement(App.Vector(0,0,0.5*p),App.Rotation(App.Vector(0,0,1),0))
                    #print(D0,'aaaaaaaaaaaaaaaaaaaaaaaa')   
                elif D0==40.0 or D0==155.0:
                    cutProfile.Placement=App.Placement(App.Vector(0,0,-1.0*p),App.Rotation(App.Vector(0,0,1),0))    
                elif D0==160.0 or D0==180.0:
                    cutProfile.Placement=App.Placement(App.Vector(0,0,-0.25*p),App.Rotation(App.Vector(0,0,1),0))         
                else:
                    cutProfile.Placement=App.Placement(App.Vector(0,0,-1.5*p),App.Rotation(App.Vector(0,0,1),0))
                    #print(D0,'cccccccccccccccccccccccccc')
                #except:
                #    pass
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c00=c00.cut(pipe)
            c00=c00.cut(c0)
            if key=='7':
                c01= Part.makeCylinder(D/2,L2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c00=c00.fuse(c01)
                #Part.show(c01)    
        sa=ShaftData.brg_scr[dia]    
        #L2=L1    
        hexagon_bolt(self)
        c2=c00
        c1=c2
        #print(key)
        if key=='05':
            c2= Part.makeCylinder(D0/2,L-L1,Base.Vector(0,0,L1),Base.Vector(0,0,1),360)
            c1=c1.fuse(c2)
        
        elif key=='07':
            #print(L,L1,L2,D)
            c2= Part.makeCylinder(D0/2,L-(L1+L2),Base.Vector(0,0,L1),Base.Vector(0,0,1),360)
            c1=c1.fuse(c2)
            c3=Part.makeCylinder(D/2,L2,Base.Vector(0,0,-L2),Base.Vector(0,0,1),360)
            
            c1=c1.fuse(c3)
            
            #Part.show(c2)
            #Part.show(c1)
        
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
        #edge1 = Part.makeLine(p1,p2)
        edge1=Part.Arc(Base.Vector(p1),Base.Vector(p6),Base.Vector(p2)).toShape()
        edge2 = Part.makeLine(p2,p3)
        edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
        edge4 = Part.makeLine(p5,p1)
        edge5=Part.Arc(Base.Vector(p1),Base.Vector(p6),Base.Vector(p2)).toShape()
        w10=Part.Wire([edge1,edge2,edge3,edge4])
        wface=Part.Face(w10)
        c2=wface.extrude(Base.Vector(0,0,d))
        c1=c1.cut(c2)
        g=c1.Volume*g0*1000/10**9 
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
        
        d=float(ScrewDia[1:3])
        R2=d/20
        
        if key=='07':
            R1=D/(20)
            w1=math.pi*(D/2)**2*L2*g0*1000/10**9
            I1=round(1/2*w1*R1**2,4)
            w2=math.pi*(d/2)**2*(L-L2)*g0*1000/10**9
            I2=round(1/2*w2*R2**2,4)
            I=I1+I2
            try:
                obj.addProperty("App::PropertyFloat", "I",label)
                obj.I=I
                obj.ViewObject.Proxy=0
            except:
                obj.I=I
                obj.ViewObject.Proxy=0  

        elif key=='05'or key=='06':
            L2=0
            w2=math.pi/4*d**2*L*g0*1000/10**9
            I=round(1/2*w2*R2**2,4)
            
            try:
                obj.addProperty("App::PropertyFloat", "I",label)
                obj.I=I
                obj.ViewObject.Proxy=0
            except:
                obj.I=I
                obj.ViewObject.Proxy=0  

        obj.Shape=c1