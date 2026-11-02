import FreeCAD as App

path = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
doc = App.openDocument(path)
doc.recompute()

for name in ("Sketch", "Pad", "Pad005", "PolarPattern", "Body002"):
    obj = doc.getObject(name)
    if obj is None:
        print(name, "MISSING")
        continue
    print(name, "State", obj.State)
    for prop in ("AttachmentSupport", "MapMode", "Placement", "Profile", "BaseFeature"):
        if hasattr(obj, prop):
            print(" ", prop, getattr(obj, prop))
    if hasattr(obj, "Shape") and not obj.Shape.isNull():
        print(" shape bbox", obj.Shape.BoundBox)
        print(" shape center", obj.Shape.CenterOfMass)
    if name == "Sketch":
        print(" geometry count", obj.GeometryCount)
        for i in range(obj.GeometryCount):
            try:
                g = obj.Geometry[i]
                print(" geometry", i, g)
            except Exception as exc:
                print(" geometry", i, "ERROR", exc)

pattern = doc.getObject("PolarPattern")
if pattern and not pattern.Shape.isNull():
    print("PolarPattern faces", len(pattern.Shape.Faces))
    for i, face in enumerate(pattern.Shape.Faces, 1):
        if i <= 12:
            print(" face", i, "center", face.CenterOfMass, "area", face.Area)
