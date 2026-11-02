import FreeCAD as App

path = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
doc = App.openDocument(path)
body = doc.getObject("Body002")
print("body group", [obj.Name for obj in body.Group])
print("body tip", body.Tip)
for name in ("Sketch", "Sketch001", "Sketch004", "Sketch006", "Sketch007"):
    obj = doc.getObject(name)
    print(name, "support", getattr(obj, "AttachmentSupport", None), "map", getattr(obj, "MapMode", None), "placement", obj.Placement)
origin = doc.getObject("Origin005")
print("origin features", getattr(origin, "OriginFeatures", None))
