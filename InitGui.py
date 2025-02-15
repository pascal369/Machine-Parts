#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class MachinePartsShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join(module_path, "icons", "MachineParts.svg"),
          'MenuText': "MachineParts",
          'ToolTip': "Show/Hide MachineParts"}

    def IsActive(self):
        import MachineParts
        MachineParts
        return True

    def Activated(self):
        try:
          import MachineParts
          MachineParts.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import MachineParts
        return not FreeCAD.ActiveDocument is None

class MachinePartsWB(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "MachineParts.svg")
        self.__class__.MenuText = "MachineParts"
        self.__class__.ToolTip = "MachineParts by Pascal"

    def Initialize(self):
        self.commandList = ["MachineParts_Show"]
        self.appendToolbar("&MachineParts", self.commandList)
        self.appendMenu("&MachineParts", self.commandList)

    def Activated(self):
        import MachineParts
        MachineParts
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
    
FreeCADGui.addWorkbench(MachinePartsWB())
FreeCADGui.addCommand("MachineParts_Show", MachinePartsShowCommand())    
