import FreeCAD as App

source = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
test_output = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.api-repair-test.FCStd"

doc = App.openDocument(source)
pad = doc.getObject("Pad003")
sketch = doc.getObject("Sketch007")

if pad is None or sketch is None:
    raise RuntimeError("Pad003 または Sketch007 が見つかりません")

repairs = [
    ("Sketch007", "Pad003", "Face11"),
]
for sketch_name, support_name, face_name in repairs:
    current = doc.getObject(sketch_name)
    support = doc.getObject(support_name)
    print("before", sketch_name, current.State, current.AttachmentSupport)
    current.AttachmentSupport = [(support, (face_name,))]
    while True:
        try:
            current.delExternal(0)
        except Exception:
            break
doc.recompute()
for sketch_name, _, _ in repairs:
    current = doc.getObject(sketch_name)
    print("after", sketch_name, current.State, current.AttachmentSupport)
print("pad004", doc.getObject("Pad004").State)
doc.saveAs(test_output)
print("saved", test_output)
