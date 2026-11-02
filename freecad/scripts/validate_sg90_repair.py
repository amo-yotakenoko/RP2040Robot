import FreeCAD as App

path = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
doc = App.openDocument(path)
doc.recompute()
for name in ("Sketch007", "Pad004", "Pad005", "PolarPattern"):
    obj = doc.getObject(name)
    print(name, obj.State if obj else "MISSING")
    if obj and hasattr(obj, "AttachmentSupport"):
        print(" support", obj.AttachmentSupport)
print("non-up-to-date")
for obj in doc.Objects:
    if "Up-to-date" not in obj.State:
        print(obj.Name, obj.State)
