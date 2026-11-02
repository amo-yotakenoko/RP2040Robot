import FreeCAD as App

source = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"
output = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.face17-test.FCStd"
doc = App.openDocument(source)
first = doc.getObject("Sketch")
origin = doc.getObject("Origin005")
first.AttachmentSupport = [(origin, ("YZ_Plane002",))]
doc.recompute()
top = doc.getObject("Sketch007")
pad = doc.getObject("Pad003")
top.AttachmentSupport = [(pad, ("Face17",))]
while True:
    try:
        top.delExternal(0)
    except Exception:
        break
doc.recompute()
print("first", first.State, first.AttachmentSupport)
print("top", top.State, top.AttachmentSupport)
print("pad003", pad.State, "pad004", doc.getObject("Pad004").State)
doc.saveAs(output)
