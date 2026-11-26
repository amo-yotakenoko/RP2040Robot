"""Rename Arm files/labels and verify visibility after saving.

Targets (mm model, geometry unchanged):
    Base.FCStd      -> BaseYaw.FCStd      / BaseYaw
    UpperArm.FCStd  -> UpperArm.FCStd     / UpperArm
    LowerArm.FCStd  -> Forearm.FCStd      / Forearm
    Roll.FCStd      -> WristRoll.FCStd    / WristRoll
    Roll_Mirrored_Link (link to Roll with ScaleVector X=-1)
                    -> WristPitch         (link and mirror preserved)

The script saves new component files, updates ArmUnit links, reopens all files,
checks Body/Tip/link visibility, and only then removes the old component files.
Internal FreeCAD object names are preserved.
"""

import os

import FreeCAD as App


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ARM_DIR = os.path.join(ROOT, "Arm")
COMPONENTS = [
    ("Base.FCStd", "BaseYaw.FCStd", "Base_Link", "BaseYaw", "Body006"),
    ("UpperArm.FCStd", "UpperArm.FCStd", "UpperArm_Link", "UpperArm", "Body"),
    ("LowerArm.FCStd", "Forearm.FCStd", "LowerArm_Link", "Forearm", "Body008"),
    ("Roll.FCStd", "WristRoll.FCStd", "Roll_Link", "WristRoll", "Body009"),
]
PITCH_LINK = ("Roll_Mirrored_Link", "WristPitch")


def close_if_open(document):
    if document is not None:
        App.closeDocument(document.Name)


def open_doc(path):
    return App.openDocument(path)


def set_component_visibility(document, body):
    for obj in document.Objects:
        if hasattr(obj, "Visibility"):
            obj.Visibility = False
    body.Visibility = True
    if body.Tip is not None:
        body.Tip.Visibility = True


def rename_components():
    for old_name, new_name, _link_name, label, body_name in COMPONENTS:
        old_path = os.path.join(ARM_DIR, old_name)
        new_path = os.path.join(ARM_DIR, new_name)
        if not os.path.exists(old_path):
            raise RuntimeError("Missing component: " + old_path)
        if old_path != new_path and os.path.exists(new_path):
            raise RuntimeError("Refusing to overwrite existing file: " + new_path)
        document = open_doc(old_path)
        body = document.getObject(body_name)
        if body is None:
            raise RuntimeError("Body not found: " + body_name)
        document.Label = label
        body.Label = label
        set_component_visibility(document, body)
        document.recompute()
        document.saveAs(new_path)
        close_if_open(document)


def update_assembly():
    assembly_path = os.path.join(ARM_DIR, "ArmUnit.FCStd")
    assembly = open_doc(assembly_path)
    link_labels = {}
    for _old_name, _new_name, link_name, label, body_name in COMPONENTS:
        link = assembly.getObject(link_name)
        if link is None:
            raise RuntimeError("Assembly link not found: " + link_name)
        new_doc = open_doc(os.path.join(ARM_DIR, _new_name))
        body = new_doc.getObject(body_name)
        if body is None:
            raise RuntimeError("New body not found: " + body_name)
        link.Label = label
        link.LinkedObject = body
        link.Visibility = True
        link_labels[link_name] = label
        close_if_open(new_doc)

    pitch_link = assembly.getObject(PITCH_LINK[0])
    if pitch_link is None:
        raise RuntimeError("Assembly link not found: " + PITCH_LINK[0])
    pitch_link.Label = PITCH_LINK[1]
    pitch_link.Visibility = True

    root = assembly.getObject("Assembly")
    if root is not None and hasattr(root, "Visibility"):
        root.Visibility = True
    assembly.recompute()
    assembly.save()
    close_if_open(assembly)


def verify():
    for _old_name, new_name, _link_name, label, body_name in COMPONENTS:
        document = open_doc(os.path.join(ARM_DIR, new_name))
        body = document.getObject(body_name)
        if body is None or body.Label != label or not body.Visibility:
            raise RuntimeError("Component visibility/label check failed: " + new_name)
        if body.Tip is not None and not body.Tip.Visibility:
            raise RuntimeError("Component Tip is hidden: " + new_name)
        close_if_open(document)

    assembly = open_doc(os.path.join(ARM_DIR, "ArmUnit.FCStd"))
    for link_name, label in list((item[2], item[3]) for item in COMPONENTS) + [PITCH_LINK]:
        link = assembly.getObject(link_name)
        if link is None or link.Label != label or link.LinkedObject is None or not link.Visibility:
            raise RuntimeError("Assembly link check failed: " + link_name)
    close_if_open(assembly)


def remove_old_names():
    for old_name, new_name, _link_name, _label, _body_name in COMPONENTS:
        if old_name != new_name:
            old_path = os.path.join(ARM_DIR, old_name)
            if os.path.exists(old_path):
                os.remove(old_path)


rename_components()
update_assembly()
verify()
remove_old_names()
print("Arm file/label rename complete; visibility and Tip/link checks passed.")
