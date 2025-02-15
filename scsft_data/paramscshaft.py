import FreeCAD, Part, math
import FreeCADGui as Gui
import FreeCAD as App
from FreeCAD import Base
class ScSft:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
        #return
    def execute(self, obj):
        label=obj.Name
        key=App.ActiveDocument.getObject(label).key
        RightHandThread=App.ActiveDocument.getObject(label).RightHandThread
        pitch=App.ActiveDocument.getObject(label).pitch
        L=App.ActiveDocument.getObject(label).L
        L1=App.ActiveDocument.getObject(label).L1
        L2=App.ActiveDocument.getObject(label).L2
        D1=App.ActiveDocument.getObject(label).D1
        D=App.ActiveDocument.getObject(label).D
        d0=App.ActiveDocument.getObject(label).d0
        d1=App.ActiveDocument.getObject(label).d1
        l=App.ActiveDocument.getObject(label).l
        t=App.ActiveDocument.getObject(label).t
        #print(key)
        def shaft(self):
            global c00
            
            h=(D1-D)/2

            c00= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c01= Part.makeCylinder(d0/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c00=c00.cut(c01)
            c01= Part.makeCylinder(d1/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c00=c00.cut(c01)
            c01= Part.makeCylinder(d1/2,l,Base.Vector(L-l,0,0),Base.Vector(1,0,0),360)
            c00=c00.cut(c01)
        def blade(self):
            global c00
            h=(D1-D)/2
            p1=(L2,0,-D/2)
            p2=(L2,0,-(h+D/2))
            p3=(L2+t,0,-(h+D/2))
            p4=(L2+t,0,-D/2)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeLine(p4,p1)
            profile=Part.Wire([edge1,edge2,edge3,edge4])
            #らせん_sweep
            if RightHandThread==True:
                scd=False#右ねじ
            else:
                scd=True  
            helix=Part.makeHelix(pitch,L1,D1/2,0,scd)
            helix.Placement=App.Placement(App.Vector(L2,0,0),App.Rotation(App.Vector(0,1,0),90))
            makeSolid=True
            isFrenet=True
            c00=Part.Wire(helix).makePipeShell([profile],makeSolid,isFrenet)

        if key=='0':
            label='shaft'
            shaft(self)
            c1=c00
            #obj.Shape=c1
        elif key=='1':    
            label='blade'
            blade(self)
            c1=c00   
            #obj.Shape=c1
        #c1=c1.fuse(c2)
        #doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)
        obj.Shape=c1
        