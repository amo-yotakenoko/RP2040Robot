import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
d=App.openDocument(os.path.join(root,"Arm","ArmUnit.FCStd"),False)
a=d.getObject("Assembly")
print("ROOT",getattr(a,"Visibility","NA"),getattr(getattr(a,"ViewObject",None),"Visibility","NA"),len(a.Group))
for o in a.Group:
    if o.TypeId=="App::Link":
        shape=o.Shape
        bb=shape.BoundBox
        print("LINK",o.Name,"VIS",o.Visibility,getattr(getattr(o,"ViewObject",None),"Visibility","NA"),"NULL",shape.isNull(),"SOLIDS",len(shape.Solids),"VOL",shape.Volume,"BASE",o.Placement.Base,"BB",(bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax))
