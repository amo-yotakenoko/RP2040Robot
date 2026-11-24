import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
parts=[("ServoHorn_Master_Single","Body003"),("Base","Body006"),("ServoHorn_Master_Cross","Body007"),("UpperArm","Body"),("LowerArm","Body008"),("Roll","Body009")]
for name,body_name in parts:
 d=App.openDocument(os.path.join(root,"Arm",name+".FCStd"),False)
 bodies=[o for o in d.Objects if o.TypeId=="PartDesign::Body"]
 b=d.getObject(body_name)
 broken=[]
 for s in d.Objects:
  if hasattr(s,"ExternalGeometry"):
   for obj, subs in s.ExternalGeometry:
    if obj is None or not obj.Shape:
     broken.append(s.Name)
 bad=[o.Name for o in d.Objects if any(x not in ("Up-to-date","Touched") for x in getattr(o,"State",[]))]
 print(name,"BODIES",[o.Name for o in bodies],"OBJECTS",len(d.Objects),"VOLUME",b.Shape.Volume if b else "MISSING","BROKEN",sorted(set(broken)),"BAD",bad)
a=App.openDocument(os.path.join(root,"Arm","ArmUnit.FCStd"),False)
asm=a.getObject("Assembly")
print("ASSEMBLY",[(x.Name,x.TypeId) for x in asm.Group] if asm else "MISSING")
