#import os
#import sys
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
#import DraftVecUtils
#import Sketcher
#import PartDesign
from math import pi
#import Draft
import FreeCAD as App

class Basic:
    def __init__(self, obj):
        self.Type = 'Basic'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)

    def execute(self, obj):
        label=obj.Name
        L=App.ActiveDocument.getObject(label).L
        D=App.ActiveDocument.getObject(label).D
        type=App.ActiveDocument.getObject(label).type
        g0=App.ActiveDocument.getObject(label).g0
        #gr=gr*1000

        def basic(self):
            global c0
            c0= Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0),360) 
        basic(self)
        #doc = Gui.getDocument()
        #for obj in doc.Objects:
    
        g=c0.Volume*g0*1000/10**9 
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

        obj.Shape=c0   
       
