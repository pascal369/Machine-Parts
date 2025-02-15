# Properties of Shapes
# Show ShapeType, Number of SubShapes, Area, Volume and Center of gravity,
# Calcurate Mass and Center of mass of Selected-Objects
# Shapes should be grouped into a single object.
import os
import sys
import csv
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import Draft

def total_mass(shape, a=0):
    """ Calcurate Mass and Center of mass of argument shape """
    M = 0
    xx = FreeCAD.Vector(0, 0, 0)
    for i in range(len(shape.SubShapes)):
        st = shape.SubShapes[i].ShapeType
        ms = shape.SubShapes[i].Mass
        cm = shape.SubShapes[i].CenterOfMass
        M += ms
        xx += ms*cm
        if a: # a != 0 -> output breakdown of total mass
            FreeCAD.Console.PrintMessage("%d, %s, %f, %f, %f, %f\n" % (i, st, ms, cm.x, cm.y, cm.z))
    CoM = xx/M
    return M, CoM


def plot_point(vector_a):
    """ Plot point from argument vector """ 
    point = Draft.make_point(vector_a)
    Draft.autogroup(point) # Not required after version 0.19?


# Get Selected-Objects to obj
obj = Gui.Selection.getSelection()

if len(obj):
    shp = obj[0].Shape # Get shp as shape from obj
    
    FreeCAD.Console.PrintMessage("-------- Properties of Shapes  --------\n")
    
    # Show ShapeType of shp
    FreeCAD.Console.PrintMessage("ShapeType = %s\n" % shp.ShapeType)
    
    # Show Number of faces, shells, solids and subshapes in shp
    FreeCAD.Console.PrintMessage("Number of faces, shells, solids, subshapes = %d, %d, %d, %d\n" \
                        % (len(shp.Faces), len(shp.Shells), len(shp.Solids), len(shp.SubShapes)))
    
    # Show Area of shp
    FreeCAD.Console.PrintMessage("Area = %f\n" % shp.Area)
    
    # Show Volume of shp
    FreeCAD.Console.PrintMessage("Volume = %f\n" % shp.Volume)
    
    # Show Center of gravity of shp
    CoG = shp.CenterOfGravity
    FreeCAD.Console.PrintMessage("Center of gravity = (%f, %f, %f)\n" % (CoG.x, CoG.y, CoG.z))
    
    # Calcurate Mass and Center of mass
    M, CoM = total_mass(shp)
    FreeCAD.Console.PrintMessage("Mass = %f\n" % M)
    FreeCAD.Console.PrintMessage("Center of mass = (%f, %f, %f)\n" % (CoM.x, CoM.y, CoM.z))
    
    # Plot point as Center of gravity
    plot_point(CoG)
    FreeCAD.ActiveDocument.Point.Label = "center_of_gravity"
    
    # Plot point as Center of mass
    plot_point(CoM)
    FreeCAD.ActiveDocument.Point001.Label = "center_of_mass"
    
    FreeCAD.ActiveDocument.recompute()
    
else:
    FreeCAD.Console.PrintMessage("-------- No valid setected objects! --------\n")