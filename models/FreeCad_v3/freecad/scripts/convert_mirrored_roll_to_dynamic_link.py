"""Replace the baked mirrored Roll file with a dynamic App::Link mirror.

Source: Arm/Roll.FCStd#Body009.
Mirror: App::Link ScaleVector=(-1,1,1), positioned about global X=0.
Changed: Arm/ArmUnit.FCStd link only. Units: mm.
"""
import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
arm=os.path.join(root,"Arm")
roll=App.openDocument(os.path.join(arm,"Roll.FCStd"),False)
asm=App.openDocument(os.path.join(arm,"ArmUnit.FCStd"),False)
link=asm.getObject("Roll_Mirrored_Link")
body=roll.getObject("Body009")
p=body.Placement
link.LinkedObject=body
link.ScaleVector=App.Vector(-1,1,1)
link.Placement=App.Placement(App.Vector(-p.Base.x,p.Base.y,p.Base.z),p.Rotation)
link.Label="Roll (Mirrored, linked to Roll)"
if not hasattr(link,"SourcePart"):
    link.addProperty("App::PropertyString","SourcePart","Mirror")
link.SourcePart="Arm/Roll.FCStd#Body009"
if not hasattr(link,"MirrorPlane"):
    link.addProperty("App::PropertyString","MirrorPlane","Mirror")
link.MirrorPlane="X=0 mm"
link.Visibility=True
asm.getObject("Assembly").Visibility=True
asm.recompute()
b=link.Shape.BoundBox
asm.save()
print("DYNAMIC_MIRROR",link.LinkedObject.Document.FileName,"VOLUME",link.Shape.Volume,"BB",(b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax))
