import FreeCAD as App
import os
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
files=[(os.path.join(root,"Reference","ServoHorn_Master_Single.FCStd"),"Body003"),(os.path.join(root,"Reference","ServoHorn_Master_Cross.FCStd"),"Body007"),(os.path.join(root,"Reference","sg90.FCStd"),"Body002"),(os.path.join(root,"Arm","Base.FCStd"),"Body006"),(os.path.join(root,"Arm","UpperArm.FCStd"),"Body"),(os.path.join(root,"Arm","LowerArm.FCStd"),"Body008"),(os.path.join(root,"Arm","Roll.FCStd"),"Body009")]
for path,body_name in files:
 d=App.openDocument(path,False)
 b=d.getObject(body_name)
 print("PART",os.path.basename(path),"BODY",b.Visibility if b else "MISSING","TIP",b.Tip.Name+":"+str(b.Tip.Visibility) if b and b.Tip else "MISSING")
a=App.openDocument(os.path.join(root,"Arm","ArmUnit.FCStd"),False)
asm=a.getObject("Assembly")
print("ASSEMBLY",asm.Visibility,[(o.Name,o.Visibility) for o in asm.Group if o.TypeId=="App::Link"])
