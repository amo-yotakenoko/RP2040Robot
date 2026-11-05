"""Rotate SG002 around its local W axis and repair joint2's face support.

Target document: models/FreeCad_v3/arm_v3.FCStd
Target objects: Link002 (label SG002), Sketch014 in Body004 (label joint2)
Units: FreeCAD lengths are mm; rotation is 180 degrees.

The source FCStd is opened read-only from the user's point of view and is
never overwritten.  The result is saved as a new FCStd beside the source.
Run this from FreeCAD's Python console or macro editor.
"""

import os

import FreeCAD as App


SOURCE = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\arm_v3.FCStd"
OUTPUT = r"C:\Users\taken\projects\RP2040Robot\models\FreeCad_v3\arm_v3.sg002-w180-joint2-repaired.FCStd"


def require(doc, name):
    obj = doc.getObject(name)
    if obj is None:
        raise RuntimeError("Required object is missing: {}".format(name))
    return obj


def face_normal(face):
    # A planar face has a stable normal at its parameter midpoint.
    u0, u1, v0, v1 = face.ParameterRange
    return face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)


def opposite_planar_face(feature, current_name):
    """Return the face opposite current_name, preferring equal-area faces."""
    current_index = int(current_name[4:]) - 1
    current = feature.Shape.Faces[current_index]
    current_normal = face_normal(current)
    candidates = []
    for index, candidate in enumerate(feature.Shape.Faces, 1):
        name = "Face{}".format(index)
        if name == current_name:
            continue
        normal = face_normal(candidate)
        if current_normal.dot(normal) > -0.999:
            continue
        area_error = abs(candidate.Area - current.Area)
        center_distance = (candidate.CenterOfMass - current.CenterOfMass).Length
        candidates.append((area_error, center_distance, name))
    if not candidates:
        raise RuntimeError(
            "Could not find the opposite planar face of {}. "
            "Inspect Pocket004 faces before changing the script.".format(current_name)
        )
    candidates.sort()
    return candidates[0][2], candidates


doc = App.openDocument(SOURCE)
try:
    sg002 = require(doc, "Link002")
    pocket004 = require(doc, "Pocket004")
    joint2_sketch = require(doc, "Sketch014")

    # In FreeCAD placement terms, local W is the local Z direction.  Compose
    # the 180-degree turn in local coordinates so SG002's insertion point is
    # unchanged while its orientation is flipped around W.
    before = sg002.Placement
    local_w_turn = App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 180))
    sg002.Placement = before.multiply(local_w_turn)

    # Sketch014 currently references Pocket004.Face6.  After the SG002 turn,
    # attach it to the geometrically opposite face of the same feature.
    old_support = "Face6"
    new_support, candidates = opposite_planar_face(pocket004, old_support)
    print("joint2 Sketch014 support: {} -> {}".format(old_support, new_support))
    print("opposite-face candidates:", candidates)
    joint2_sketch.AttachmentSupport = [(pocket004, (new_support,))]

    # External geometry can retain stale references after support changes.
    while True:
        try:
            joint2_sketch.delExternal(0)
        except Exception:
            break

    doc.recompute()
    print("SG002 placement:", sg002.Placement)
    print("Sketch014 state:", joint2_sketch.State)
    print("Pocket004 state:", pocket004.State)

    if os.path.abspath(SOURCE).lower() == os.path.abspath(OUTPUT).lower():
        raise RuntimeError("Refusing to overwrite the source FCStd")
    doc.saveAs(OUTPUT)
    print("saved:", OUTPUT)
finally:
    App.closeDocument(doc.Name)
