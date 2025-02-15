# -*- coding: utf-8 -*-
__version__ = "0.2023.09.30c"
#Animator, 2023, by <TheMarkster>, LGPL2.1 or later
#Credit to Dan Miel for some of the A2Plus-related stuff
DEBUG = False
import FreeCAD, FreeCADGui, Part
import time
import math
import re
from pivy import coin
from PySide import QtCore, QtGui
import os, subprocess, glob
try:
    import a2p_solversystem
    a2p_present = True
except:
    a2p_present = False
    pass
DEFAULT_MACRO_STRING =[\
"#python code goes here",\
"#fp = Animator object",\
"#doc = document containing Animator object",\
"#props = list of properties in Variables",\
"#objs = list of objects in Variables",\
"#con = FreeCAD.Console",\
"#setExpression(idx,string_val) = objs[idx].setExpression(string_val)",\
"#getValue(idx) = get value contained in VariableNNN where NNN is idx-1",\
"#fp.CurrentFrame = current frame in animation loop",\
"#AnimatorLastFrame = True if current frame is last frame in loop",\
"#cam = active view's camera object",\
"#cam.Position -> vector, cam.Position = (x,y,z) or cam.Position = vector",\
"#cam.Orientation -> returns a tuple (axis,angle), or set with cam.Orientation = (axis,angle) or camOrientation = rot (a FreeCAD.Rotation)",\
"#cam.OrientationEuler -> (yaw, pitch, roll), cam.OrientationEuler = (yaw,pitch,roll)",\
"#cam.Height, cam.FocalDistance, cam.AspectRatio, cam.NearDistance, cam.FarDistance, (all floats)",\
"#cam.Placement -> FreeCAD.Placement object",\
]
class Animator:
    def __init__(self, obj):
        animv = "Animator.v"+__version__
        obj.addProperty("App::PropertyBool","FreezeCamera","Camera","Keep camera position each frame").FreezeCamera = False
        obj.addProperty("App::PropertyLink","CamPlacementObject","Camera","Sets cam to this object's placement each frame in the loop")
        obj.addProperty("App::PropertyBool","ReverseCam","Camera","Reverses camera orientation, applicable only if CamPlacementObject is set").ReverseCam = False
        obj.addProperty("App::PropertyBool","MakeGif","AnimatedGif","Make an animated gif using ffmpeg (requires ffmpeg binary be installed)").MakeGif = False
        obj.addProperty("App::PropertyFile","PathToFFMPEG","AnimatedGif","Browse to locate the ffmpeg binary with this property")
        pg = FreeCAD.ParamGet("User parameter:Plugins/Animator_Macro")
        obj.PathToFFMPEG = pg.GetString("PathToFFMPEG","")
        obj.addProperty("App::PropertyIntegerConstraint","GifHeight","AnimatedGif", "Height in pixels of the animated gif to be produced").GifHeight = (480,1,1000000,1)
        obj.addProperty("App::PropertyIntegerConstraint","GifWidth","AnimatedGif","Width in pixels of the animated gif to be produced").GifWidth = (640,1,1000000,1)
        obj.addProperty("App::PropertyIntegerConstraint","GifFrameRate","AnimatedGif","Frame rate in milliseconds (1000 = 1 second)").GifFrameRate = (20,1,10000,1)
        obj.addProperty("App::PropertyPath","PathToGif","AnimatedGif","Folder in which to place frame_NNN.png files and animated gif file (default: macros/Animator/screen_grabs/)")
        obj.PathToGif = pg.GetString("PathToGif","")
        obj.addProperty("App::PropertyString","AnimatedGifFilename","AnimatedGif","Name for animated gif\nReplaces any files of the same name!").AnimatedGifFilename = "Animated.gif"
        obj.addProperty("App::PropertyBool","FitAllEachFrame", "AnimatedGif", \
                        "If True send 'ViewFit' message to active view before taking the screenshot each frame").FitAllEachFrame = True
        obj.addProperty("App::PropertyString","BGColor","AnimatedGif","Color to use for background.  Example: 'Yellow'.  Default: 'Transparent'").BGColor="Transparent"
        obj.addProperty("App::PropertyFloat","ScrapString","RunMacro", "Internal use during loop as a scrap memory register")
        obj.setEditorMode("ScrapString",2)# hidden
        obj.addProperty("App::PropertyBool","RunMacro","RunMacro","Whether to execute code contained in MacroFile each time through loop").RunMacro=True
        obj.addProperty("App::PropertyFile","MacroFile","RunMacro","Macro file to execute each time through the loop")
        obj.addProperty("App::PropertyStringList","MacroString","RunMacro","Quick and Dirty macro string to run each time through the loop").MacroString = DEFAULT_MACRO_STRING
        obj.addProperty("App::PropertyBool","RunMacroString","RunMacro","Whether to execute code contained in MacroString each time through loop").RunMacroString=True
        obj.addProperty("App::PropertyBool","A2PlusSolve","Assemblers","Be sure to open A2Plus workbench first.  Executes solve command each step in the loop").A2PlusSolve = False
        obj.addProperty("App::PropertyStringList","A2PlusConstraints","Assemblers","List of A2Plus constraints to solve, solve all if blank\nPut # in front of those to ignore")
        obj.addProperty("App::PropertyBool","A2PlusRefreshConstraints","Assemblers", \
                        "Refresh A2PlusConstraints will all constraints in document on Refresh, if  True").A2PlusRefreshConstraints=True
        obj.addProperty("App::PropertyBool","Asm3Solve","Assemblers","Be sure to open Assembly 3 workbench first.  Executes solve command each step in the loop").Asm3Solve = False
        obj.addProperty("App::PropertyBool","Asm4Solve","Assemblers","Be sure to open Assembly 4 workbench first.  Executues solve command each step in the loop").Asm4Solve = False
        obj.addProperty("App::PropertyBool","ShowProgress",animv,"Whether to show progress in Description/Label2 column during animation").ShowProgress = True
        obj.addProperty("App::PropertyBool","StartAnimating",animv,"[Trigger] Start animating (or double click Animator in tree)").StartAnimating = False
        obj.addProperty("App::PropertyBool","StopAnimating",animv,"[Trigger] Stop animating (or double click Animator in tree)").StopAnimating = False
        obj.addProperty("App::PropertyBool","ResetAfterAnimation",animv,"Reset animated properties back to initial values after the animation is done\n\
You may use Undo after the animation to manually reset the values if this is False.").ResetAfterAnimation = True
        obj.addProperty("App::PropertyBool","Refresh",animv,"[Trigger] Refreshes Variables property lists, sets self back to False\nUse this if objects/properties have changed")\
.Refresh = False
        obj.addProperty("App::PropertyInteger","Frames",animv,"Number of frames / iterations per loop").Frames = 100
        obj.addProperty("App::PropertyInteger","CurrentFrame",animv,"Current frame in loop")
        obj.setEditorMode("CurrentFrame",2) #hidden
        obj.addProperty("App::PropertyFloatConstraint","Sleep",animv,"Optional sleep time (in seconds) per frame / iteration").Sleep = (0,0,float("inf"),.1)
        obj.addProperty("App::PropertyFloatConstraint","InitialDelay",animv,"Initial delay (in seconds) before animation starts").InitialDelay = (0,-.045,60,.1)
        obj.addProperty("App::PropertyIntegerConstraint","VariableCount",animv,"Number of variables to use\nIncrease for more VariableNNN properties").VariableCount = (3,0,100,1)
        obj.addProperty("App::PropertyStringList","BlacklistedObjects","SettingsAdvanced","Object types not to include in Properties").BlacklistedObjects =\
["App::Origin","App::Line","App::Plane"]
        obj.addProperty("App::PropertyStringList","Supported","SettingsAdvanced","Supported property types")
        obj.Supported = ["App::PropertyInteger","App::PropertyIntegerConstraint","App::PropertyFloat","App::PropertyFloatConstraint",
"App::PropertyLength","App::PropertyAngle","App::PropertyArea","App::PropertyDistance","App::PropertyPercent","App::PropertyQuantity",
"App::PropertyQuantityConstraint","App::PropertySpeed","App::PropertyVolume","App::PropertyPlacement","App::PropertyVector",
"App::PropertyMatrix","Sketcher::PropertyConstraintList"]
        self.properties = []
        self.fpName = obj.Name
        self.isAnimating = False
        self.expressionDict = {} #to hold objects' initial ExpressionEngine before animation
        self.stringToRun = "" #from macro file
        self.stringToRunFromMacroString = ""
        self.macroPermissions = 0 #you have to giver permission at least once each session
        self.cameraPosition = "" #used if FreezeCamera = True
        obj.Proxy = self

    def getSubProperties(self,prop,typeId,obj):
        if not "Placement" in typeId and not "Vector" in typeId and not "Matrix" in typeId and not "ConstraintList" in typeId \
                                                          and not "Spreadsheet::Sheet" in typeId and not "Rotation" in typeId:
            return [prop]
        elif "Rotation" in typeId:
            return [prop+".Angle",prop+".Axis.x",prop+".Axis.y",prop+".Axis.z",prop+".Roll",prop+".Pitch",prop+".Yaw"]
        elif "Placement" in typeId:
            return [prop+".Rotation.Angle",prop+".Rotation.Axis.x",prop+".Rotation.Axis.y",prop+\
                   ".Rotation.Axis.z",prop+".Rotation.Pitch",prop+".Rotation.Yaw",prop+\
                   ".Rotation.Roll",prop+".Base.x",prop+".Base.y",prop+".Base.z"]
        elif "Vector" in typeId:
            return [prop+".x",prop+".y",prop+".z"]
        elif "Matrix" in typeId:
            return [prop+".A11",prop+".A12",prop+".A13",prop+".A14",prop+".A21",prop+".A22",prop+".A23",prop+\
                   ".A24",prop+".A31",prop+".A32",prop+".A33",prop+".A34",
prop+".A41",prop+".A42",prop+".A43",prop+".A44"]
        elif "ConstraintList" in typeId:
            conlist = getattr(obj,prop)
            names = [prop + "." + con.Name for con in conlist if con.Name]
            return names
        elif "Spreadsheet::Sheet" in typeId:
            FreeCAD.Console.PrintMessage("Spreadsheet aliases\n")
            ignore = ["columnWidths","rowHeights"]
            aliases = [prop + "." + pl for pl in obj.PropertiesList if pl not in ignore]
            FreeCAD.Console.PrintMessage(str(aliases)+"\n")
            return aliases

    def onDocumentRestored(self, obj):
        self.macroPermissions = 0 #require permission at least once per session

    def onChanged(self, fp, prop):
        if prop == "Refresh" and fp.Refresh:
            fp.Refresh = False
            self.setupVariables(fp) #calls refresh()
            if hasattr(fp,"A2PlusRefreshConstraints") and fp.A2PlusRefreshConstraints:
                self.setupA2PlusConstraints(fp)
        elif prop == "VariableCount":
            self.setupVariables(fp)
        elif prop == "StartAnimating" and fp.StartAnimating:
            fp.StartAnimating = False
            t = QtCore.QTimer()
            t.singleShot(50+fp.InitialDelay*1000, self.startAnimating) #avoid warning message about selection changing while committing data
        elif "Variable" in prop and not bool("Count" in prop or "Nth" in prop or "Start" in prop or "Step" in prop):
            self.checkAndWarnAliases(fp,prop)
        elif "MacroFile" in prop and fp.MacroFile:
            self.readMacroFile(fp)
        elif "MacroString" in prop and fp.MacroString != DEFAULT_MACRO_STRING:
            self.readMacroString(fp)
        elif "PathToFFMPEG" in prop and hasattr(fp,"PathToFFMPEG"):
            pg = FreeCAD.ParamGet("User parameter:Plugins/Animator_Macro")
            pg.SetString("PathToFFMPEG",fp.PathToFFMPEG)
        elif "PathToGif" in prop and hasattr(fp,"PathToGif"):
            pg = FreeCAD.ParamGet("User parameter:Plugins/Animator_Macro")
            pg.SetString("PathToGif",fp.PathToGif)

    def setupGifFolder(self,fp):
        """cleans up folder of any existing PNG and GIF files, creates folder if necessary"""
        if not hasattr(fp,"MakeGif") or not fp.MakeGif:
            return
        if not fp.PathToFFMPEG:
            pg = FreeCAD.ParamGet("User parameter:Plugins/Animator_Macro")
            fp.PathToFFMPEG = pg.GetString("PathToFFMPEG","")
            if not fp.PathToFFMPEG:
                FreeCAD.Console.PrintError("You must set the path to FFMPEG in order to make the animated gif\n")
                return False
        if not fp.PathToGif:
            macro_path = FreeCAD.getUserMacroDir(True)
            subfolder = "Animator/screen_grabs"
            fp.PathToGif = os.path.join(macro_path,subfolder)
        if not os.path.exists(fp.PathToGif):
            os.makedirs(fp.PathToGif)
        existing_pngs = glob.glob(os.path.join(fp.PathToGif,"*.png"))
        for file_path in existing_pngs:
            os.remove(file_path)
        if not fp.AnimatedGifFilename:
            FreeCAD.Console.PrintError("You must provide a name for the new animated gif file in the AnimatedGifFilename property\n")
            return False
        return True #success

    def makeGifFrame(self,fp, frame):
        """called during animation loop.  Makes the screen shot for the current frame"""
        if not hasattr(fp,"MakeGif") or not fp.MakeGif:
            return
        screenshot_file = os.path.join(fp.PathToGif,f"frame_{frame:03d}.png")
        if fp.FitAllEachFrame:
            FreeCADGui.SendMsgToActiveView("ViewFit")
        if os.path.exists(screenshot_file):
            os.remove(screenshot_file)
        FreeCADGui.ActiveDocument.ActiveView.saveImage(screenshot_file, fp.GifWidth, fp.GifHeight, fp.BGColor)

    def makeGif(self,fp):
        """make the final animated gif from all the screen shot frames"""
        output_gif = os.path.join(fp.PathToGif,fp.AnimatedGifFilename)
        if os.path.exists(output_gif):
            os.remove(output_gif)
        frame_duration = fp.GifFrameRate / 1000.0
        path_to_ffmpeg = fp.PathToFFMPEG
        ffmpeg_command = [
           path_to_ffmpeg,
           "-framerate", f"1/{frame_duration}",
           "-i", os.path.join(fp.PathToGif, "frame_%03d.png"),
           "-y", #overwrite output_gif if it exits
           output_gif
        ]
        subprocess.run(ffmpeg_command)
        FreeCAD.Console.PrintMessage(f"{output_gif} created.\n")


    def getCameraPosition(self):
        v = FreeCADGui.activeView()
        self.cameraPosition = v.getCamera()

    def restoreCameraPosition(self):
        v = FreeCADGui.activeView()
        v.setCamera(self.cameraPosition)

    def readMacroFile(self,fp):
        if DEBUG:
            print("reading macro file")
        import os
        if not fp.MacroFile:
            self.stringToRun = ""
            return
        fin = open(fp.MacroFile, 'r')
        self.stringToRun = fin.read()
        fin.close()

    def readMacroString(self,fp):
        if DEBUG:
            print("reading macro string")
        self.stringToRunFromMacroString = "\n".join(fp.MacroString)

    def runString(self, lastFrame = False, bRunMacroString=False):
        if DEBUG:
            print ("running macro file...")
        macro_string = self.stringToRun if not bRunMacroString else self.stringToRunFromMacroString
        import FreeCAD, FreeCADGui
        fp = FreeCAD.ActiveDocument.getObject(self.fpName)
        import sys, importlib
        my_name = 'my_macro'
        my_spec = importlib.util.spec_from_loader(my_name, loader=None)
        my_macro = importlib.util.module_from_spec(my_spec)
        my_macro.FreeCAD = FreeCAD
        my_macro.App = FreeCAD
        my_macro.Gui = FreeCADGui
        my_macro.FreeCADGui = FreeCADGui
        my_macro.AnimatorLastFrame = lastFrame
        my_macro.doc = fp.Document
        my_macro.Animator = fp
        my_macro.con = FreeCAD.Console
        my_macro.fp = fp
        my_macro.cam = Camera()
        my_macro.props = [getattr(fp,p) for p in fp.PropertiesList if "Enumeration" in fp.getTypeIdOfProperty(p) if getattr(fp,p) != 'Select Property']
        my_macro.objs = [fp.Document.getObject(p.split(".")[0]) for p in my_macro.props]
        my_macro.props = [p[p.index(".")+1:] for p in my_macro.props]
        def setExpression(idx,expr):
            my_macro.objs[idx].setExpression(my_macro.props[idx],expr)
            my_macro.doc.recompute()
        my_macro.setExpression = lambda idx,expr: setExpression(idx,expr)
        def getValue(idx):
              cur_obj = my_macro.objs[idx]
              cur_prop = my_macro.props[idx]
              fp.setExpression("ScrapString",f"{cur_obj.Name}.{cur_prop}")
              return round(float(fp.ScrapString),6)
        my_macro.getValue = lambda idx: getValue(idx)
        def setStep(idx,val):
            setattr(fp,f"Variable{format(idx+1,'03')}Step",val)
        my_macro.setStep = lambda idx,val:setStep(idx,val)
        try:
            exec(macro_string, my_macro.__dict__)
        except Exception as e:
            FreeCAD.Console.PrintError(f"Animator: error running script: {e}\n")
            self.isAnimating = False
            raise

    def getPermissionFromUser(self,fp,bRunMacroString=False):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Animator Macro Security Warning")
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        if not bRunMacroString:
            msgBox.setText("Warning: The following file will be executed: " + fp.MacroFile)
            info = "Do you want to execute the contents of this file?\n\n"
        else:
            msgBox.setText("Warning: Contents of property Macro String will be executed as python code")
            info = "Do you want to execute the contents of this string?\n\n"
        info += "DO NOT ALLOW IF YOU GOT THIS FILE FROM AN UNTRUSTED SOURCE!!!\n\n"
        msgBox.setInformativeText(info)
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Help)
        yesBtn = msgBox.button(QtGui.QMessageBox.StandardButton.Yes)
        noBtn = msgBox.button(QtGui.QMessageBox.StandardButton.No)
        helpBtn = msgBox.button(QtGui.QMessageBox.StandardButton.Help)
        helpBtn.setText("Show me the code, but do not run")
        yesBtn.setText("Yes, run python code")
        noBtn.setText("No, do not run python code")
        ret = msgBox.exec()
        if ret == QtGui.QMessageBox.Yes:
            self.macroPermissions += 1
            return True
        elif ret == QtGui.QMessageBox.No: #permission denied
            self.macroPermissions = 0
            return False
        elif ret == QtGui.QMessageBox.Help: #show code
            msgBox2 = QtGui.QDialog()
            layout = QtGui.QVBoxLayout()
            text_browser = QtGui.QTextBrowser()
            if bRunMacroString:
                text_browser.setPlainText(self.stringToRunFromMacroString)
            else:
                text_browser.setPlainText(self.stringToRun)
            layout.addWidget(text_browser)
            ok = QtGui.QPushButton("OK")
            msgBox2.setWindowTitle("Animator: Code to run:")
            ok.clicked.connect(msgBox2.accept)
            msgBox2.setLayout(layout)
            ret = msgBox2.exec_()
            return False

    def startAnimating(self, skip_permission = False):
        self.isAnimating = True
        fp = FreeCAD.ActiveDocument.getObject(self.fpName)
        cam = None
        camObj = None
        if hasattr(fp,"CamPlacementObject") and fp.CamPlacementObject:
            camObj = fp.CamPlacementObject
            if not hasattr(camObj,"Placement"):
                FreeCAD.Console.PrintError("Cam Placement Object has no Placement property!\n")
            else:
                cam = Camera()
                cam.Placement = camObj.Placement
        animated = 0 #check if there is any animation work to do
        if hasattr(fp,"RunMacro") and fp.RunMacro and fp.MacroFile:
            self.readMacroFile(fp)
            animated += 1
            if not skip_permission or self.macroPermissions == 0:
                if not self.getPermissionFromUser(fp):
                    FreeCAD.Console.PrintWarning("Animator: Animation was canceled by user.\n")
                    self.isAnimating = False
                    return
        if hasattr(fp,"RunMacroString") and fp.RunMacroString and fp.MacroString != DEFAULT_MACRO_STRING:
            self.readMacroString(fp)
            animated += 1
            if not skip_permission or self.macroPermissions == 0:
                if not self.getPermissionFromUser(fp,bRunMacroString=True):
                    FreeCAD.Console.PrintWarning("Animator: Animation was canceled by user.\n")
                    self.isAnimating = False
                    return
        variables = {} #tuple ii:(prop,start,step)

        for ii in range(1,fp.VariableCount+1):
            variables[ii] = (getattr(fp,"Variable"+format(ii,'03')),getattr(fp,"Variable"+format(ii,'03')+"Start"),\
                             getattr(fp,"Variable"+format(ii,'03')+"Step"),getattr(fp,"Variable"+format(ii,'03')+"Nth"))
            if getattr(fp,"Variable"+format(ii,'03')) != "Select Property":
                animated += 1
        if animated == 0:
            FreeCAD.Console.PrintError("No properties to animate.  Select some properties and try again.\n")
            self.isAnimating = False
            return
        else:
            for k,v in variables.items(): #save obj.ExpressionEngine for each obj in self.expressionsDict
                prop = v[0]
                objname = prop.split(".")[0]
                obj = FreeCAD.ActiveDocument.getObject(objname)
                self.saveExpressions(fp,obj)
        counter = 1
        oldLabel2 = fp.Label2
        if hasattr(fp,"A2PlusConstraints") and fp.A2PlusSolve:
            uncommented = [con for con in fp.A2PlusConstraints if con[0] != "#"]
            runlist = [fp.Document.getObject(con) for con in uncommented]
            FreeCAD.Console.PrintMessage(f"Animator: using these constraints: {uncommented}"+chr(10))
        if hasattr(fp,"CurrentFrame"):
            fp.CurrentFrame = 0 #use this to ensure we have undone everything later
        if hasattr(fp, "MakeGif") and fp.MakeGif:
            if not self.setupGifFolder(fp): #returns false if some animated gif properties are not properly configured
                FreeCAD.Console.PrintError("Error setting up animation folder.\n")
                return
        if hasattr(fp,"FreezeCamera") and fp.FreezeCamera:
            self.getCameraPosition()
        fp.Document.openTransaction("Reset animated objects")
        while (counter <= fp.Frames and not fp.StopAnimating):
            if hasattr(fp,"CurrentFrame"):
                fp.CurrentFrame = counter
            QtGui.QApplication.instance().processEvents()
            if cam and camObj:
                if not fp.ReverseCam:
                    cam.Placement = camObj.Placement
                else:
                    plm = camObj.Placement
                    plm.Rotation = plm.Rotation * (FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                    cam.Placement = plm
            for jj in range(1,fp.VariableCount+1):
                if variables[jj][0] != "Select Property":
                    nth = counter % variables[jj][3] #remainder of dividing counter by Nth property
                    step = getattr(fp,"Variable"+format(jj,'03')+"Step")
                    if nth == 0 and step != 0.0: #set step to 0 to not animate this property
                        self.setProperty(fp,variables[jj][0],variables[jj][1] + step * counter)
            if fp.ShowProgress:
                fp.Label2 = str(counter)+"/"+str(fp.Frames)
            if fp.A2PlusSolve:
                if not hasattr(fp,"A2PlusConstraints") or len(fp.A2PlusConstraints) == 0:
                    FreeCADGui.runCommand('a2p_SolverCommand',0)
                else: #run only selected constraints
                    if a2p_present:
                        a2p_solversystem.solveConstraints(fp.Document, None, False, matelist = runlist, showFailMessage=False)
            if fp.Asm3Solve:
                FreeCADGui.runCommand('asm3CmdSolve',0)
            if fp.Asm4Solve:
                FreeCADGui.runCommand('Asm4_updateAssembly',0)
            if fp.RunMacro and self.stringToRun:
                self.runString(counter == fp.Frames)
            if hasattr(fp,"RunMacroString") and fp.RunMacroString and fp.MacroString != DEFAULT_MACRO_STRING:
                self.runString(counter == fp.Frames, bRunMacroString=True)
            if hasattr(fp,"MakeGif") and fp.MakeGif:
                self.makeGifFrame(fp,counter) #make the current frame
                if counter == fp.Frames:
                    self.makeGif(fp) #make animated gif
            FreeCADGui.updateGui()
            if hasattr(fp,"FreezeCamera") and fp.FreezeCamera:
                self.restoreCameraPosition()
            time.sleep(fp.Sleep)
            counter += 1
        fp.Document.commitTransaction()
        if hasattr(fp,"ResetAfterAnimation") and fp.ResetAfterAnimation:
            fp.Document.undo()
            if hasattr(fp,"CurrentFrame") and fp.CurrentFrame != 0:
                while fp.CurrentFrame != 0:
                    fp.Document.undo()
        fp.StopAnimating = False
        self.isAnimating = False
        self.restoreExpressions(fp)
        fp.Label2 = oldLabel2
        FreeCAD.ActiveDocument.recompute()

    def setupA2PlusConstraints(self,fp):
        if not a2p_present:
            return
        constraints = [obj.Name for obj in fp.Document.Objects if "ConstraintInfo" in obj.Content and not "mirror" in obj.Name]
        fp.A2PlusConstraints = constraints

    def setupVariables(self,fp):
        self.refresh(fp)
        ii = fp.VariableCount+1
        while hasattr(fp,"Variable"+format(ii,'03')):
            fp.removeProperty("Variable"+format(ii,'03'))
            fp.removeProperty("Variable"+format(ii,'03')+"Start")
            fp.removeProperty("Variable"+format(ii,'03')+"Step")
            fp.removeProperty("Variable"+format(ii,'03')+"Nth")
            ii += 1
        for ii in range(1,fp.VariableCount+1):
            baseName = "Variable"+format(ii,'03')
            if not hasattr(fp,baseName):
                fp.addProperty("App::PropertyEnumeration",baseName,"AnimatorVariables","Object.Property to use for this variable")
                setattr(fp,baseName,self.properties)
            else:
                saved = getattr(fp,baseName)
                setattr(fp,baseName,self.properties)
                if saved in self.properties:
                    setattr(fp,baseName,saved)
            if not hasattr(fp,baseName+"Start"):
                fp.addProperty("App::PropertyFloat",baseName+"Start","AnimatorVariables","Starting value for this variable")
                setattr(fp,baseName+"Start",0)
            if not hasattr(fp,baseName+"Step"):
                fp.addProperty("App::PropertyFloat",baseName+"Step","AnimatorVariables","Step -- amount by which this variable is incremented (or decremented if negative) each frame.")
                setattr(fp,baseName+"Step",1)
            if not hasattr(fp,baseName+"Nth"):
               fp.addProperty("App::PropertyIntegerConstraint",baseName+"Nth","AnimatorVariables","If other than 1, only increment/decrement every nth frame.")
               setattr(fp,baseName+"Nth",(1,1,10000,1))

    def isSupportedType(self,fp,typeId):
        '''returns False if not supported, else True'''
        if typeId not in fp.Supported:
            return False
        else:
            return True

    def editMacroString(self):
        fp = FreeCAD.ActiveDocument.getObject(self.fpName)
        dlg = MacroStringEditor(fp)
        dlg.exec_()

    def getProperties(self,fp,obj):
        '''get the supported properties of obj'''
        if obj.TypeId != "Spreadsheet::Sheet":
            props = [prop for prop in obj.PropertiesList if self.isSupportedType(fp,obj.getTypeIdOfProperty(prop)) \
                     and  bool(obj.getEditorMode(prop) == [] or prop == "AttachmentOffset" or prop == "Placement")]
        else:
            props = [prop for prop in obj.PropertiesList if self.isSupportedType(fp,obj.getTypeIdOfProperty(prop))]
        return props

    def saveExpressions(self,fp,obj):
        '''saves expression engine property of obj the first time setProperty() is called for obj'''
        if not obj in self.expressionDict.keys() and hasattr(obj,"ExpressionEngine"):
            self.expressionDict[obj.Name] = obj.ExpressionEngine

    def restoreExpressions(self,fp):
        for k,v in self.expressionDict.items():
            obj = FreeCAD.ActiveDocument.getObject(k)
            for expr in v:
                obj.setExpression(expr[0],expr[1])
        self.expressionDict = {}

    def checkAndWarnAliases(self,fp,prop):
        '''if user has selected an alias, then warn'''
        objname = getattr(fp,prop).split(".")[0]
        obj = FreeCAD.ActiveDocument.getObject(objname)
        if hasattr(obj,"TypeId") and obj.TypeId == "Spreadsheet::Sheet":
            FreeCAD.Console.PrintWarning("Warning: Spreadsheet aliases containing expressions will not be restored after animation is complete.\n")

    def setProperty(self,fp,prop,val):
        '''prop is in form "objectname.property.subproperty.subproperty" ,e.g. "Box.Placement.Base.x"'''
        objname = prop.split(".")[0]
        obj = FreeCAD.ActiveDocument.getObject(objname)
        if obj.TypeId != "Spreadsheet::Sheet":
            obj.setExpression(prop[len(objname)+1:],str(val))
            FreeCAD.ActiveDocument.recompute()
            obj.setExpression(prop[len(objname)+1:],None)
        else:
            obj.set(prop[len(objname)+1:],str(val))
            FreeCAD.ActiveDocument.recompute()

    def refresh(self,fp):
        '''setup Properties enumeration to contain each property of the objects supported objectname.propertyname format'''
        doc = FreeCAD.ActiveDocument
        objects = [obj for obj in doc.Objects if obj != fp and not obj.TypeId in fp.BlacklistedObjects]
        self.properties = []
        for obj in objects:
            props = self.getProperties(fp,obj)
            if props:
                for prop in props:
                    subprops = self.getSubProperties(prop,obj.getTypeIdOfProperty(prop),obj)
                    for sub in subprops:
                        self.properties.extend([obj.Name+"."+sub])
        self.properties.sort()
        self.properties = ["Select Property"] + self.properties


class PythonSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        variable_format = QtGui.QTextCharFormat()
        variable_format.setForeground(QtGui.QColor(255, 170, 0))  # Yellow color for variables
        variable_format.setFontWeight(QtGui.QFont.Bold)
        self.highlighting_rules.append((r'\b\w+\b', variable_format))

        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor(0, 0, 255))  # Blue color for keywords
        keyword_format.setFontWeight(QtGui.QFont.Bold)
        self.highlighting_rules.append((r'\b(?:import|from|def|class|if|else|for|while|return|break|continue)\b',\
                                          keyword_format))

        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor(0, 170, 0))  # Green color for comments
        self.highlighting_rules.append((r'#.*$', comment_format))

        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor(255,0,0))  # red color for strings
        self.highlighting_rules.append((r'".*?"', string_format))

        numeral_format = QtGui.QTextCharFormat()
        numeral_format.setForeground(QtGui.QColor(0,0,255))  # Blue color for numerals
        self.highlighting_rules.append((r'\b\d+\b', numeral_format))

        operator_format = QtGui.QTextCharFormat()
        operator_format.setForeground(QtGui.QColor(160, 160, 164))  # Color for operators
        self.highlighting_rules.append((r'[-+,:*/%=<>&|!^]', operator_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            regex = re.compile(pattern)
            for match in regex.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), char_format)


class MacroStringEditor(QtGui.QDialog):
    def __init__(self,fp,parent=FreeCADGui.getMainWindow()):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)
        self.fp = fp
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        self.editor = QtGui.QPlainTextEdit()
        self.editor.setPlainText("\n".join(fp.MacroString))
        self.editor.setMinimumWidth(600)
        self.editor.setMinimumHeight(600)
        highlighter = PythonSyntaxHighlighter(self.editor.document())
        layout.addWidget(self.editor)
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        self.fp.MacroString = self.editor.toPlainText().splitlines()
        self.fp.Document.recompute()
        super().accept()

    def reject(self):
        print("rejected")
        super().reject()



class Camera:
    def __init__(self):
        # Get the active view and camera
        self.view = FreeCADGui.activeView()
        self.camera = self.view.getCamera()
        self.height = ""
        self.orientation = ""
        self.position = ""
        self.header = ""
        self.cam_type = ""
        self.nearDistance = ""
        self.farDistance = ""
        self.aspectRatioStr = ""
        self.aspectRatio = ""
        self.focalDistance = ""
        self.mappingStr = ""
        self.posStr = ""
        self.orientationStr = ""
        self.heightStr = ""
        self.focalDistanceStr = ""
        self.parse()

    def __repr__(self):
        self.refresh()
        return self.camera

    def refresh(self):
        """refresh some internal variables"""
        self.camera = self.view.getCamera()
        self.parse()

    def getHeader(self):
        """returns the version of Open Inventor"""
        self.refresh()
        return self.header

    def getType(self):
        """returns Orthographic or Perspective"""
        self.refresh()
        return self.cam_type

    @property
    def NearDistance(self):
        """nearDistance sets clipping plane for near objects"""
        self.refresh()
        return float(self.nearDistance)

    @property
    def FarDistance(self):
        """farDistance sets clipping plane for far objects"""
        self.refresh()
        return float(self.farDistance)

    @NearDistance.setter
    def NearDistance(self,val):
        """nearDistance sets clipping plane for near objects"""
        self.refresh()
        self.nearDistance = str(val)
        self.unParse()

    @FarDistance.setter
    def FarDistance(self,val):
        """farDistance sets clipping plane for far objects"""
        self.refresh()
        self.farDistance = str(val)
        self.unParse()

    @property
    def AspectRatio(self):
        """width to height ratio"""
        self.refresh()
        return float(self.aspectRatio)

    @AspectRatio.setter
    def AspectRatio(self, val):
        """width to height ratio, must be greater than 0"""
        self.refresh()
        self.aspectRatio = str(val)
        self.unParse()

    @property
    def FocalDistance(self):
        """distance form viewpoint to point of focus, usually ignored"""
        self.refresh()
        return float(self.focalDistance)

    @FocalDistance.setter
    def FocalDistance(self,val):
        """distance form viewpoint to point of focus, usually ignored"""
        self.refresh()
        self.focalDistance = str(val)
        self.unParse()

    def parse(self):
        """parse camera string into separate self.values, called by refresh()"""
        d = self.camera.split()
        try:
            self.header = d[0]+' '+d[1] + ' '+d[2] # '#Inventor v2.1 ascii'
            self.cam_type = d[3] #'OrthographicCamera' #d[4] = '{'
            self.mappingStr = d[5] #viewportMapping
            self.mapping = d[6] #ADJUST_CAMERA
            self.posStr = d[7] #'position'
            self.position = d[8] + ' '+d[9]+' ' + d[10]
            self.orientationStr = d[11] #'orientation'
            self.orientation = d[12]+' '+d[13]+' '+d[14]+'  '+d[15]
            self.nearDistanceStr = d[16]#'nearDistance'
            self.nearDistance = d[17]
            self.farDistanceStr = d[18]#'farDistance'
            self.farDistance = d[19] #13.163915
            self.aspectRatioStr = d[20]#'aspectRatio'
            self.aspectRatio = d[21] #1
            self.focalDistanceStr = d[22] #'focalDistance'
            self.focalDistance = d[23]
            self.heightStr = d[24]
            self.height = d[25]
        except:
            FreeCAD.Console.PrintError("Failed to parse camera data\n")

    def unParse(self):
        """write the self.values into the camera string, set camera to it"""
        new_cam = self.header + '\n' + self.cam_type + '{\n' + self.mappingStr+' '+self.mapping+'\n'\
        + self.posStr + ' ' + self.position + '\n' \
        + self.orientationStr + ' ' + self.orientation + '\n'\
        + self.nearDistanceStr + ' ' + self.nearDistance + '\n'\
        + self.farDistanceStr + ' ' + self.farDistance + '\n'\
        + self.aspectRatioStr + ' ' + self.aspectRatio + '\n'\
        + self.focalDistanceStr + ' ' + self.focalDistance + '\n'\
        + self.heightStr + ' ' + self.height + '\n'\
        + '}\n'
        self.camera = new_cam
        self.view.setCamera(self.camera)

    @property
    def Height(self):
        """height of the camera above scene"""
        self.refresh()
        height = float(self.height)
        return height

    @Height.setter
    def Height(self, height):
        """height of camera above scene"""
        self.refresh()
        self.height = str(height)
        self.unParse()

    @property
    def Position(self):
        """returns a vector of the current camera position"""
        self.refresh()
        position_str = self.position
        position_values = [float(val) for val in position_str.split()]
        position = FreeCAD.Vector(*position_values)
        return position

    @Position.setter
    def Position(self, vector):
        """set camera position, vector can be FreeCAD.Vector or (x,y,z) tuple"""
        self.refresh()
        new_position_str = ' '.join([str(val) for val in vector])
        self.position = new_position_str
        self.unParse()

    @property
    def Orientation(self):
        """returns the orientation as a tuple containing (axis,angle) which is (vector, float in degrees)"""
        self.refresh()
        orientation_str = self.orientation
        vals = [float(val) for val in orientation_str.split()]
        axis = FreeCAD.Vector(vals[0],vals[1],vals[2])
        angle = math.degrees(vals[3])
        return (axis,angle)

    @property
    def OrientationEuler(self):
        """cam orientation returns (yaw,pitch,roll)"""
        self.refresh()
        axis,angle = self.Orientation
        rot = FreeCAD.Rotation(axis, angle)
        euler_angles = rot.getYawPitchRoll()
        return euler_angles

    @Orientation.setter
    def Orientation(self, orientation_data):
        """sets orientation, Orientation = (axis, angle), which is (vector, float in degrees) or Orientation = Rotation"""
        isRotation = isinstance(orientation_data,FreeCAD.Rotation)
        if not isRotation and len(orientation_data) != 2:
            raise ValueError("Orientation must be a tuple or list containing (axis, angle), or a FreeCAD.Rotation")

        axis, angle = orientation_data
        self.refresh()
        if not isRotation:
            self.orientation = f"{axis.x} {axis.y} {axis.z} {math.radians(angle)}"
        else:
            self.orientation = f"{axis.x} {axis.y} {axis.z} {angle}" #angle in radians already if from a FreeCAD.Rotation object.
        self.unParse()

    @OrientationEuler.setter
    def OrientationEuler(self, ypr_tuple):
        """OrientationEuler = (yaw,pitch,roll) (3 floats)"""
        self.refresh()
        if not len(ypr_tuple) == 3:
            raise ValueError("Use a tuple of floats to set OrientationEuler, e.g. cam.OrientationEuler = (yaw,pitch,roll)")
        yaw,pitch,roll = ypr_tuple
        rotation = FreeCAD.Rotation(float(yaw), float(pitch), float(roll))
        self.Orientation = (rotation.Axis, math.degrees(rotation.Angle))

    @property
    def Placement(self):
        rot = FreeCAD.Rotation(self.Orientation)
        pos = self.Position
        plm = FreeCAD.Placement(pos,rot)
        return plm

    @Placement.setter
    def Placement(self,plm):
        rot = plm.Rotation
        pos = plm.Base
        axis = rot.Axis
        angle = math.degrees(rot.Angle)
        self.Orientation = axis,angle
        self.Position = pos



class AnimatorVP:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self

    def doubleClicked(self,vobj):
        if vobj.Object.Proxy.isAnimating:
            vobj.Object.StopAnimating = True
        else:
            vobj.Object.StartAnimating = True

    def attach(self,vobj):
        self.Object = vobj.Object
        self.standard = coin.SoGroup()
        vobj.addDisplayMode(self.standard,"Standard")

    def onDelete(self, vobj, subelements):
        return True

    def setupContextMenu(self, vobj, menu):
         text = {True:"Unrefresh %1",False:"Refresh properties for %1"}
         action = menu.addAction(text[vobj.Object.Refresh].replace("%1",vobj.Object.Label))
         action.triggered.connect(lambda: setattr(vobj.Object,"Refresh",True))
         text = {True:"Stop Animating %1",False:"Start Animating %1"}
         action = menu.addAction(text[vobj.Object.StartAnimating].replace("%1",vobj.Object.Label))
         action.triggered.connect(lambda: setattr(vobj.Object,"StartAnimating",True))
         text = {True:"Start Animating %1",False:"Stop Animating %1"}
         action = menu.addAction(text[vobj.Object.StopAnimating].replace("%1",vobj.Object.Label))
         action.triggered.connect(lambda: setattr(vobj.Object,"StopAnimating",True))
         text = "Edit Macro String"
         action = menu.addAction(text)
         action.triggered.connect(vobj.Object.Proxy.editMacroString)

    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        if prop == "StartAnimating" or prop == "StopAnimating":
            fp.ViewObject.signalChangeIcon()

    def getDisplayModes(self,obj):
        '''Return a list of display modes.'''
        modes=["Standard"]
        return modes

    def claimChildren(self):
        return[]

    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Standard"

    def setDisplayMode(self,mode):
        '''Map the display mode defined in attach with those defined in getDisplayModes.\
                Since they have the same names nothing needs to be done. This method is optional'''
        return mode

    def onChanged(self, vp, prop):
        '''Here we can do something when a single property got changed'''
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        pass

    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
                optional and if not defined a default icon is shown.'''
        iconAnimating = """
/* XPM */
static char *_635391677201[] = {
/* columns rows colors chars-per-pixel */
"64 64 4 1 ",
"  c black",
". c #FFFF7F7F2727",
"X c #FFFFF2F20000",
"o c None",
/* pixels */
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
};"""
        iconNormal = """
/* XPM */
static char *_635391677201[] = {
/* columns rows colors chars-per-pixel */
"64 64 4 1 ",
"  c black",
". c #FFFF7F7F2727",
"X c #FFFFF2F20000",
"o c None",
/* pixels */
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooooooooooooooooooooooooooooooooooooooooooXXX   XXX   XXX    ooo",
"ooooooooooooooooooooooooooooooooooooooooooXXX   XXX   XXX    ooo",
"ooooooooooooooooooooooooooooooooooooooooooXXX   XXX   XXX    ooo",
"ooooooooooooooooooooooooooooooooooooooooooXXX   XXX   XXX    ooo",
"ooooooooooooooooooooooooXXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooooooooooooooooooooooooXXX   XXX   XXX   XXXooooooooooooooooooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXXooooooooooooooooooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXXooooooooooooooooooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXXooooooooooooooooooo",
"ooo   XXX   XXX   XXX   oooooooooooooooooooooooooooooooooooooooo",
"ooo   XXX   XXX   XXX   oooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXXooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"ooo   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX   XXX    ooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo     ................................................     ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"ooo                                                          ooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",
"oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
};"""
        if self.Object.Proxy.isAnimating:
            return iconAnimating
        else:
            return iconNormal

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None

    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None
#######################################
