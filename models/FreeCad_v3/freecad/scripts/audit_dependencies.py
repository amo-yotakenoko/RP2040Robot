"""Read-only dependency report for the final Arm directory."""
import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
arm=os.path.join(root,"Arm")
parts=["ServoHorn_Master_Single","Base","ServoHorn_Master_Cross","UpperArm","LowerArm","Roll"]
part_dir={"ServoHorn_Master_Single":os.path.join(root,"Reference"),"ServoHorn_Master_Cross":os.path.join(root,"Reference")}
for name in ("Base","UpperArm","LowerArm","Roll"):
 part_dir[name]=arm
for name in parts:
 d=App.openDocument(os.path.join(part_dir[name],name+".FCStd"),False)
 print("PART",name)
 for o in d.Objects:
  if "SubShapeBinder" in o.TypeId:
   for target,subs in o.Support:
    print(" BINDER",o.Name,"->",target.Document.FileName,"#",target.Name,"SUB",repr(subs))
a=App.openDocument(os.path.join(arm,"ArmUnit.FCStd"),False)
print("ASSEMBLY")
for o in a.getObject("Assembly").Group:
 if o.TypeId=="App::Link":
  print(" LINK",o.Name,"->",o.LinkedObject.Document.FileName,"#",o.LinkedObject.Name)
