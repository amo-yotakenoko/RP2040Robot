"""Normalize visibility in the final Arm directory.

Changed only ViewObject.Visibility; geometry, links, and placements are not
modified. Primary bodies and Assembly links are made visible;
construction planes, axes, sketches, and Binders are hidden.
"""
import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
parts=[("ServoHorn_Master_Single","Body003"),("Base","Body006"),("ServoHorn_Master_Cross","Body007"),("UpperArm","Body"),("LowerArm","Body008"),("Roll","Body009")]
for name, body_name in parts:
    d=App.openDocument(os.path.join(root,"Arm",name+".FCStd"),False)
    body=d.getObject(body_name)
    for obj in d.Objects:
        if hasattr(obj,"Visibility"):
            obj.Visibility=False
    body.Visibility=True
    if body.Tip:
        body.Tip.Visibility=True
    d.recompute()
    d.save()

asm=App.openDocument(os.path.join(root,"Arm","ArmUnit.FCStd"),False)
for obj in asm.Objects:
    if hasattr(obj,"Visibility"):
        obj.Visibility=False
for obj in asm.getObject("Assembly").Group:
    if obj.TypeId=="App::Link":
        obj.Visibility=True
asm.recompute()
asm.save()

print("VISIBILITY_FIXED", os.path.join(root,"Arm"))
