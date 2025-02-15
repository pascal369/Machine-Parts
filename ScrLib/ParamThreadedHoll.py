from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ScrData
class ThreadedHoll:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        dia=App.ActiveDocument.getObject(label).dia
        st=App.ActiveDocument.getObject(label).st
        Thread=App.ActiveDocument.getObject(label).Thread
        L2=App.ActiveDocument.getObject(label).L2
        #L1=App.ActiveDocument.getObject(label).L1
        L1=L2+0.1
        def bolt_screw(self):
            global c00
            sa=ScrData.regular[dia]
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
            db=sa[12]
            z=p/2
            #print(z)
            H0=0.86625*p
            x=H1+H0/8
            y=x*math.tan(math.pi/6)
            r0=D0/2+H0/8
            a=p/2-y
            #ボルト部
            cb= Part.makeCylinder(D0/2,L1,Base.Vector(0,0,0),Base.Vector(0,0,1),360)#ボルト部
            c00=cb
            p1=(-D0/2,0,0)
            p2=(-(D0/2-z),0,-z)
            p3=(0,0,-z)
            p4=(0,0,0)
            plist=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c0=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)#ボルト先端カット    
            #c0.Placement=App.Placement(App.Vector(0,0,p),App.Rotation(App.Vector(0,1,0),180))#ボルト先端カット
            c00=c00.fuse(c0)
             #下穴
            z=db/(1.732*2)
            z2=L1*0.2
            p1=(-db/2,0,0)
            p2=(-db/2,0,-z2)
            p3=(0,0,-(z+z2))
            p4=(0,0,0)
            plist=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)#ボルト先端カット
            c00=c00.fuse(c1)
            #ねじ断面
            if Thread==True:
                p1=(D1/2,0,-a)
                p2=(D1/2,0,a)
                p3=(r0,0,p/2)
                p4=(r0,0,-p/2)
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeLine(p2,p3)
                edge3 = Part.makeLine(p3,p4)
                edge4 = Part.makeLine(p4,p1)
                #らせん_sweep
                helix=Part.makeHelix(p,L2,D0/2,0,False)
                cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
                makeSolid=True
                isFrenet=True
                pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
                c00=c00.cut(pipe)

        bolt_screw(self)        
        c1=c00
        
        
        
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
       # Gui.runCommand('Draft_Move',0) 
        obj.Shape=c1