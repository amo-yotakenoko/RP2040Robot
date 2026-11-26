import os
import FreeCAD as App

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
path = os.path.join(root, "Arm", "ArmUnit.FCStd")
doc = App.openDocument(path)
root_obj = doc.getObject("Assembly")
print("ASSEMBLY",
      "visible=", getattr(root_obj, "Visibility", None),
      "view_visible=", getattr(getattr(root_obj, "ViewObject", None), "Visibility", None))
names = ["Base_Link", "UpperArm_Link", "LowerArm_Link", "Roll_Link", "Roll_Mirrored_Link"]
for name in names:
    obj = doc.getObject(name)
    target = getattr(obj, "LinkedObject", None) if obj else None
    print("LINK", name,
          "label=", getattr(obj, "Label", None),
          "visible=", getattr(obj, "Visibility", None),
          "view_visible=", getattr(getattr(obj, "ViewObject", None), "Visibility", None),
          "target=", getattr(target, "Name", None),
          "target_visible=", getattr(target, "Visibility", None),
          "target_tip_visible=", getattr(getattr(target, "Tip", None), "Visibility", None),
          "target_doc=", getattr(getattr(target, "Document", None), "FileName", None))
App.closeDocument(doc.Name)
