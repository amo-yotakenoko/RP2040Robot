import FreeCAD as App

path = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
doc = App.openDocument(path)
doc.recompute()

for name in ("Sketch", "Sketch001", "Sketch006", "Sketch007", "Pad003", "Pad004"):
    obj = doc.getObject(name)
    if obj is None:
        print(name, "MISSING")
        continue
    print(name, "State=", obj.State)
    for prop in ("Support", "AttachmentSupport", "MapMode", "Placement"):
        if hasattr(obj, prop):
            try:
                print(" ", prop, "=", getattr(obj, prop))
            except Exception as exc:
                print(" ", prop, "ERROR", exc)

pad = doc.getObject("Pad003")
if pad and not pad.Shape.isNull():
    print("Pad003 faces", len(pad.Shape.Faces))
    for index, face in enumerate(pad.Shape.Faces, 1):
        try:
            print(" Face", index, "center=", face.CenterOfMass, "area=", face.Area)
        except Exception as exc:
            print(" Face", index, "ERROR", exc)

doc.close()
