import os

import FreeCAD as App
import FreeCADGui as Gui

Gui.showMainWindow()


root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
arm_dir = os.path.join(root, "Arm")
components = [
    ("BaseYaw.FCStd", "Body006"),
    ("UpperArm.FCStd", "Body"),
    ("Forearm.FCStd", "Body008"),
    ("WristRoll.FCStd", "Body009"),
]


def open_doc(path):
    return App.openDocument(path)


for filename, body_name in components:
    doc = open_doc(os.path.join(arm_dir, filename))
    body = doc.getObject(body_name)
    Gui.activeDocument().getObject(body.Name).Visibility = True
    if body.Tip is not None:
        Gui.activeDocument().getObject(body.Tip.Name).Visibility = True
    doc.recompute()
    doc.save()
    App.closeDocument(doc.Name)

assembly = open_doc(os.path.join(arm_dir, "ArmUnit.FCStd"))
for name in ["Assembly", "Base_Link", "UpperArm_Link", "LowerArm_Link", "Roll_Link", "Roll_Mirrored_Link"]:
    obj = assembly.getObject(name)
    if obj is not None:
        Gui.activeDocument().getObject(obj.Name).Visibility = True
assembly.recompute()
Gui.activeDocument().activeView().fitAll()
assembly.save()
App.closeDocument(assembly.Name)

print("GUI visibility state saved for Arm components and ArmUnit.")
