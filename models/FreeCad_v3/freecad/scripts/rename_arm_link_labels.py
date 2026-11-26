"""Rename Arm part labels to the Link1..Link5 naming convention.

Target documents:
    Arm/Base.FCStd, Arm/UpperArm.FCStd, Arm/LowerArm.FCStd, Arm/Roll.FCStd
    Arm/ArmUnit.FCStd
Target objects:
    The PartDesign body in each part document and the corresponding links in
    ArmUnit. Internal FreeCAD object names are not changed; only Labels are.
Units:
    No geometry or dimensions are changed. Existing FreeCAD length units remain mm.

Expected result:
    Base          -> Link1_BaseYaw
    UpperArm      -> Link2_UpperArm
    LowerArm      -> Link3_Forearm
    Roll          -> Link4_WristRoll
    Roll2/mirrored Roll -> Link5_WristPitch
"""

import os

import FreeCAD as App


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PARTS = {
    "Base.FCStd": "Link1_BaseYaw",
    "UpperArm.FCStd": "Link2_UpperArm",
    "LowerArm.FCStd": "Link3_Forearm",
    "Roll.FCStd": "Link4_WristRoll",
}
ASSEMBLY_LINKS = {
    "Base_Link": "Link1_BaseYaw",
    "UpperArm_Link": "Link2_UpperArm",
    "LowerArm_Link": "Link3_Forearm",
    "Roll_Link": "Link4_WristRoll",
    "Roll_Mirrored_Link": "Link5_WristPitch",
}


def open_or_get(path):
    for document in App.listDocuments().values():
        if os.path.abspath(document.FileName or "") == os.path.abspath(path):
            return document, False
    return App.openDocument(path), True


def rename_parts():
    for filename, label in PARTS.items():
        path = os.path.join(ROOT, "Arm", filename)
        document, opened_here = open_or_get(path)
        document.Label = label
        bodies = [obj for obj in document.Objects if obj.TypeId == "PartDesign::Body"]
        if len(bodies) == 1:
            bodies[0].Label = label
        document.recompute()
        document.save()
        if opened_here:
            App.closeDocument(document.Name)

    assembly_path = os.path.join(ROOT, "Arm", "ArmUnit.FCStd")
    assembly, opened_here = open_or_get(assembly_path)
    for internal_name, label in ASSEMBLY_LINKS.items():
        obj = assembly.getObject(internal_name)
        if obj is None:
            raise RuntimeError("Object not found in ArmUnit: " + internal_name)
        obj.Label = label
    assembly.recompute()
    assembly.save()
    if opened_here:
        App.closeDocument(assembly.Name)

    print("Arm labels renamed. Internal object names and geometry were preserved.")


rename_parts()
