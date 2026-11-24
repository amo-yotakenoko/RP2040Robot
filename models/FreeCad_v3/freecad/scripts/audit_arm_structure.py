"""Read-only audit of the final Arm directory and ArmUnit links."""
import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
armdir=os.path.join(root,"Arm")
asm=App.openDocument(os.path.join(armdir,"ArmUnit.FCStd"),False)
a=asm.getObject("Assembly")
print("ASSEMBLY",a.TypeId,a.Label)
for o in a.Group:
    if o.TypeId=="App::Link":
        linked=o.LinkedObject
        path=linked.Document.FileName if linked else "MISSING"
        print("LINK",o.Name,"VISIBLE",o.Visibility,"TARGET",linked.Name if linked else "MISSING","FILE_EXISTS",os.path.exists(path) if linked else False,"FILE",path)
print("ASSEMBLY_BAD",[(o.Name,list(getattr(o,"State",[]))) for o in asm.Objects if any(x not in ("Up-to-date","Touched") for x in getattr(o,"State",[]))])
parts=[("ServoHorn_Master_Single","Body003"),("Base","Body006"),("ServoHorn_Master_Cross","Body007"),("UpperArm","Body"),("LowerArm","Body008"),("Roll","Body009")]
part_dir={"ServoHorn_Master_Single":os.path.join(root,"Reference"),"ServoHorn_Master_Cross":os.path.join(root,"Reference")}
for name in ("Base","UpperArm","LowerArm","Roll"):
    part_dir[name]=armdir
for name,body_name in parts:
    d=App.openDocument(os.path.join(part_dir[name],name+".FCStd"),False)
    bodies=[o.Name for o in d.Objects if o.TypeId=="PartDesign::Body"]
    broken=[]
    for s in d.Objects:
        if hasattr(s,"ExternalGeometry"):
            for obj,subs in s.ExternalGeometry:
                if obj is None or not obj.Shape: broken.append(s.Name)
    bad=[o.Name for o in d.Objects if any(x not in ("Up-to-date","Touched") for x in getattr(o,"State",[]))]
    print("PART",name,"BODIES",bodies,"BROKEN_EXT",sorted(set(broken)),"BAD",bad)
