
import Part 
import math
from FreeCAD import Base
import FreeCAD as App
import FreeCADGui as Gui
#import BearingData
from BallBrg_data import BearingData
class BallBrg:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)#
    def execute(self, obj):   
        label=obj.Name 
        dia=App.ActiveDocument.getObject(label).dia
        modelNo=App.ActiveDocument.getObject(label).modelNo
        series=App.ActiveDocument.getObject(label).series
        #print(series)
        if series=='60':
            Bdim=BearingData.Bdim60
        elif series=='62':
            Bdim=BearingData.Bdim62  
            
        sa=[]     
        sa=Bdim[dia]
        d=sa[0]
        D=sa[1]
        B=sa[2]
        r=sa[3]
        n=sa[4]
        g0=sa[6]
        t=(D-d)/6
        #VALUES#
        R1=d/2 #(radius of shaft/inner radius of inner ring)
        R2=R1+t #(outer radius of inner ring)
        R3=R1+2*t #(inner radius of outer ring)
        R4=D/2 #(outer radius of outer ring)
        TH=B #(thickness of bearing)
        NBall=n #(number of balls)
        RBall=t*1.2 #(radius of ball)
        RR=r  #(rounding radius for fillets)    
        CBall=((R3-R2)/2)+R2  #first coordinate of center of ball
        PBall=TH/2 #second coordinate of center of ball
        #Inner Ring#
        B1=Part.makeCylinder(R1,TH)
        B2=Part.makeCylinder(R2,TH)
        IR=B2.cut(B1)
        #get edges and apply fillets
        Bedges=IR.Edges
        try:
           IRF=IR.makeFillet(RR,Bedges)
        except:
            return
        #create groove and show shape
        T1=Part.makeTorus(CBall,RBall)
        T1.translate(Base.Vector(0,0,TH/2))
        try:
            InnerRing=IRF.cut(T1)
            #Part.show(InnerRing)
            c00=InnerRing
        except:
            return

        #
        #Outer Ring#
        B3=Part.makeCylinder(R3,TH)
        B4=Part.makeCylinder(R4,TH)
        OR=B4.cut(B3)
        #get edges and apply fillets
        Bedges=OR.Edges
        try:
             ORF=OR.makeFillet(RR,Bedges)
             #create groove and show shape
             T2=Part.makeTorus(CBall,RBall)
             T2.translate(Base.Vector(0,0,TH/2))
             OuterRing=ORF.cut(T2)
             #Part.show(OuterRing)
             c00=c00.fuse(OuterRing)
        except:
             return
        #Part.show(c00)
        #
        #Balls#
        for i in range(NBall):
            #Ball=Part.makeSphere(RBall)
            Alpha=(i*2*math.pi)/NBall
            #BV=(CBall*math.cos(Alpha),CBall*math.sin(Alpha),TH/2)
            Ball=Part.makeSphere(RBall*0.99,Base.Vector(CBall*math.cos(Alpha),CBall*math.sin(Alpha),TH/2))
            try:
                c00=c00.fuse(Ball)
                obj.Shape=c00  
            except:
                pass
                #return 
        obj.modelNo=sa[5]        
        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g0
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g0
            obj.ViewObject.Proxy=0
            pass  
        print(g0)  
        obj.Shape=c00    
            
        


        