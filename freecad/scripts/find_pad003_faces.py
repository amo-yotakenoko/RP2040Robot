import FreeCAD as App

path = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.first-sketch-test.FCStd"
doc = App.openDocument(path)
doc.recompute()
pad = doc.getObject("Pad003")
print("Pad003", pad.State, "faces", len(pad.Shape.Faces))
for i, face in enumerate(pad.Shape.Faces, 1):
    if i <= 30:
        try:
            print(i, "center", face.CenterOfMass, "area", round(face.Area, 4), "normal", face.normalAt(0, 0))
        except Exception as exc:
            print(i, "ERROR", exc)
