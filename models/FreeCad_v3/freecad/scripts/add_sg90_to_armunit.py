"""Add the six positioned SG90 components to Arm/ArmUnit.FCStd.

Inputs: Arm/ArmUnit.FCStd, sg90.FCStd, and arm_v4.FCStd placements.
Changed object: ArmUnit Assembly links only; geometry and part files are not
modified. Units: mm. The six SG90 links use the original Link placements.
"""
import FreeCAD as App
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
armunit = App.openDocument(os.path.join(ROOT, "Arm", "ArmUnit.FCStd"), False)
source = App.openDocument(os.path.join(ROOT, "arm_v4.FCStd"), False)
servo_doc = App.openDocument(os.path.join(ROOT, "Reference", "sg90.FCStd"), False)
assembly = armunit.getObject("Assembly")
servo_body = servo_doc.getObject("Body002")
if assembly is None or servo_body is None:
    raise RuntimeError("ArmUnit Assembly or sg90 Body002 is missing")

for source_name in ("Link", "Link001", "Link002", "Link003", "Link004", "Link005"):
    source_link = source.getObject(source_name)
    link_name = "SG90_" + source_name + "_Link"
    link = armunit.getObject(link_name)
    if link is None:
        link = assembly.newObject("App::Link", link_name)
    link.Label = "SG90 — " + source_link.Label
    link.LinkedObject = servo_body
    link.Placement = source_link.Placement
    if not hasattr(link, "ComponentType"):
        link.addProperty("App::PropertyString", "ComponentType", "Assembly")
    link.ComponentType = "Servo motor / SG90"
    link.Visibility = True

assembly.Label = "ArmUnit (arm + 6x SG90)"
armunit.recompute()
armunit.save()
print("SG90_ADDED", armunit.FileName)
