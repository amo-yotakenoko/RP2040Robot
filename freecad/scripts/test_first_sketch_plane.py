import FreeCAD as App

source = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
output = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.first-sketch-test.FCStd"

doc = App.openDocument(source)
sketch = doc.getObject("Sketch")
origin = doc.getObject("Origin005")
plane = doc.getObject("YZ_Plane002")
print("origin", origin, "plane", plane)
print("before", sketch.State, sketch.AttachmentSupport, sketch.Placement)

# Match the healthy servo.FCStd model: the first sketch belongs to the body YZ plane.
sketch.AttachmentSupport = [(origin, ("YZ_Plane002",))]
top_sketch = doc.getObject("Sketch007")
pad003 = doc.getObject("Pad003")
top_sketch.AttachmentSupport = [(pad003, ("Face17",))]
while True:
    try:
        top_sketch.delExternal(0)
    except Exception:
        break
doc.recompute()
print("after origin support", sketch.State, sketch.AttachmentSupport, sketch.Placement)
print("Pad", doc.getObject("Pad").State, "Pad003", pad003.State, "Sketch007", top_sketch.State, "Pad004", doc.getObject("Pad004").State, "Body", doc.getObject("Body002").State)
doc.saveAs(output)
print("saved", output)
