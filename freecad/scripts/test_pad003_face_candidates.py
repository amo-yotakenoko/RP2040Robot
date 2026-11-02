import FreeCAD as App

source = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\sg90.FCStd"

for face_number in range(1, 23):
    doc = App.openDocument(source)
    first = doc.getObject("Sketch")
    origin = doc.getObject("Origin005")
    first.AttachmentSupport = [(origin, ("YZ_Plane002",))]
    doc.recompute()
    top = doc.getObject("Sketch007")
    pad = doc.getObject("Pad003")
    top.AttachmentSupport = [(pad, ("Face{}".format(face_number),))]
    while True:
        try:
            top.delExternal(0)
        except Exception:
            break
    doc.recompute()
    pad004 = doc.getObject("Pad004")
    placement = top.Placement.Base
    print(face_number, "sketch", top.State, "pad004", pad004.State, "pos", placement, "vol", round(pad004.Shape.Volume, 3))
    App.closeDocument(doc.Name)
