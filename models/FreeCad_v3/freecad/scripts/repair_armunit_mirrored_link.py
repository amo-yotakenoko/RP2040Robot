import os
import FreeCAD as App

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
arm_dir = os.path.join(root, "Arm")
assembly = App.openDocument(os.path.join(arm_dir, "ArmUnit.FCStd"))
roll = App.openDocument(os.path.join(arm_dir, "WristRoll.FCStd"))
link = assembly.getObject("Roll_Mirrored_Link")
body = roll.getObject("Body009")
if link is None or body is None:
    raise RuntimeError("WristPitch link or WristRoll Body009 not found")

scale = link.ScaleVector
placement = link.Placement
link.LinkedObject = body
link.ScaleVector = scale
link.Placement = placement
link.Label = "WristPitch"
link.Visibility = True
assembly.recompute()
assembly.save()
App.closeDocument(roll.Name)
App.closeDocument(assembly.Name)

check = App.openDocument(os.path.join(arm_dir, "ArmUnit.FCStd"))
check_link = check.getObject("Roll_Mirrored_Link")
if check_link is None or check_link.LinkedObject is None:
    raise RuntimeError("WristPitch link is still broken after reopen")
print("WristPitch linked to", check_link.LinkedObject.Document.FileName)
print("ScaleVector", check_link.ScaleVector)
App.closeDocument(check.Name)
